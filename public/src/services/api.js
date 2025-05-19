import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: `${API_URL}/api/v1`,
});

// 请求拦截器添加token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    const tokenType = localStorage.getItem("token_type");
    if (token) {
      config.headers["Authorization"] = `${tokenType} ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器处理错误
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // 未授权，清除token并重定向到登录页
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// 认证相关API
export const authApi = {
  login: (username, password) => {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);
    formData.append("grant_type", "password");
    formData.append("client_id", "password");
    formData.append("client_secret", "password");

    return apiClient.post("/auth/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
  },
  // 发送邮箱验证码
  sendEmailCode: (email) => 
    apiClient.post(`/auth/send-email-code?email=${encodeURIComponent(email)}`),
  
  // 邮箱验证码登录
  loginEmailCode: (email, code) => {
    const formData = new URLSearchParams();
    formData.append("email", email);
    formData.append("code", code);
    
    return apiClient.post("/auth/login-email-code", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
  },
  register: (userData) => apiClient.post("/auth/register", userData),
  registerOrganization: (data) =>
    apiClient.post("/auth/register-o-convener", data),
  registerOrganizationMultipart: (formData) =>
    apiClient.post("/auth/register-o-convener", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),
  resetPassword: (email) => apiClient.post("/auth/password-reset", email),
};

// 论文相关API
export const papersApi = {
  
};

// 学生验证相关API
export const studentApi = {
  verifyStudent: (data) => apiClient.post("/students/verify", data),
  getGPARecords: (data) => apiClient.post("/students/gpa", data),
  uploadVerificationBatch: (file) => {
    const formData = new FormData();
    formData.append("file", file);
    return apiClient.post("/students/verify/batch", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
};

// 课程相关API
export const coursesApi = {
  // 获取课程列表（所有用户可访问）
  getCourses: (params) => apiClient.get("/courses", { params }),
  
  // 获取当前用户创建的课程列表
  getMyCourses: (params) => apiClient.get("/courses/my-courses", { params }),
  
  // 获取单个课程详情
  getCourse: (id) => apiClient.get(`/courses/${id}`),
  
  // 创建新课程（需要O-Convener权限或PermissionLevel为3）
  createCourse: async (data) => {
    try {
      const response = await apiClient.post("/courses", data);
      return response.data;
    } catch (error) {
      console.error("Error creating course:", error);
      throw error;
    }
  },
  
  // 更新课程信息（需要O-Convener权限或是课程创建者）
  updateCourse: async (id, data) => {
    try {
      const response = await apiClient.put(`/courses/${id}`, data);
      return response.data;
    } catch (error) {
      console.error("Error updating course:", error);
      throw error;
    }
  },
  
  // 删除课程（需要O-Convener权限或是课程创建者）
  deleteCourse: async (id) => {
    try {
      const response = await apiClient.delete(`/courses/${id}`);
      return response.data;
    } catch (error) {
      console.error("Error deleting course:", error);
      throw error;
    }
  },
  
  // 搜索课程（支持关键词和组织ID搜索）
  searchCourses: async (params) => {
    try {
      const response = await apiClient.get("/courses/search/", { params });
      return response.data;
    } catch (error) {
      console.error("Error searching courses:", error);
      throw error;
    }
  },
};

// 用户管理相关API
export const usersApi = {
  getUsers: (params) => apiClient.get("/users", { params }),
  getUserById: (id) => apiClient.get(`/users/${id}`),
  createUser: (data) => apiClient.post("/users", data),
  updateUser: (id, data) => apiClient.put(`/users/${id}`, data),
  deleteUser: (id) => apiClient.delete(`/users/${id}`),
  getCurrentUser: () => apiClient.get("/users/me"),
  updateCurrentUser: (data) => apiClient.put("/users/me", data),
  addQuota: (userId, amount) =>
    apiClient.post(`/users/add-quota/${userId}`, { amount }),
  editBalance: (userId, amount) =>
    apiClient.post(`/users/${userId}/edit_balance`, amount, {
      headers: { "Content-Type": "application/json" }
    }),
  searchUsers: (params) => apiClient.get("/users/search", { params }),
  batchCreateUsers: (formData) =>
    apiClient.post("/users/batch_create", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),
};

// 组织管理相关接口
export const organizationApi = {
  // 获取组织列表
  getOrganizations: (params) => apiClient.get("/organizations", { params }),

  // 获取单个组织信息
  getOrganization: (id) => apiClient.get(`/organizations/${id}`),

  // 更新组织信息
  updateOrganization: (id, data) => apiClient.put(`/organizations/${id}`, data),

  // 获取组织成员
  getOrganizationMembers: (id, params) =>
    apiClient.get(`/organizations/${id}/members`, { params }),

  // 上传验证文件
  uploadVerificationDocument: (id, file) => {
    const formData = new FormData();
    formData.append("file", file);
    return apiClient.post(
      `/organizations/${id}/upload-verification`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
  },
};

// 验证管理相关接口
export const verificationApi = {
  // 获取组织的验证状态
  getVerificationStatus: (organizationId) =>
    apiClient.get(`/verification/${organizationId}`),

  // E-Admin 审核
  eAdminReview: (organizationId, data) =>
    apiClient.post(`/verification/${organizationId}/e-admin-review`, data),

  // Senior E-Admin 审核
  seniorReview: (organizationId, data) =>
    apiClient.post(`/verification/${organizationId}/senior-review`, data),

  // T-Admin 审核
  tAdminReview: (organizationId, data) =>
    apiClient.post(`/verification/${organizationId}/t-admin-review`, data),

  // 根据 e_admin_approved 状态获取审核记录
  getByEAdminStatus: (params) =>
    apiClient.get("/verification/by-e-admin-status", { params }),

  // 根据 senior_approved 状态获取审核记录
  getBySeniorStatus: (params) =>
    apiClient.get("/verification/by-senior-status", { params }),

  // 获取（灵活筛选）验证列表
  getVerificationsByStatus: (params) =>
    apiClient.get("/verification/by-status", { params }),
};

export const logApi = {
  // 1. 获取系统日志（需要E-Admin权限）
  getLogs: (params) => apiClient.get("/logs/", { params }),
  // 2. 获取当前用户日志（O-Convener或普通用户）
  getMyLogs: (params) => apiClient.get("/logs/my-logs", { params }),
  // 3. 获取指定组织日志（E-Admin/O-Convener 等）
  getOrganizationLogs: (organizationId, params) =>
    apiClient.get(`/logs/organization/${organizationId}`, { params }),
};

export const helpApi = {
  getQuestions: (params) => apiClient.get("/help/questions", { params }),
  createQuestion: (data) => apiClient.post("/help/questions", data),
  getQuestion: (id) => apiClient.get(`/help/questions/${id}`),
  createResponse: (questionId, data) =>
    apiClient.post(`/help/questions/${questionId}/responses`, data),
  getResponses: (questionId) =>
    apiClient.get(`/help/questions/${questionId}/responses`),
};

// 政策管理相关API
export const policiesApi = {
  // 获取政策列表
  getPolicies: (params) => apiClient.get("/policies/", { params }),
  // 获取单个政策
  getPolicy: (id) => apiClient.get(`/policies/${id}`),
  // 创建政策（支持文件上传）
  createPolicy: (formData) => {
    // 确保使用正确的 Content-Type
    return apiClient.post("/policies/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  // 更新政策（支持文件上传）
  updatePolicy: (id, formData) => {
    // 确保使用正确的 Content-Type
    return apiClient.post(`/policies/${id}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  

  deletePolicy: (id) => apiClient.delete(`/policies/${id}`),
  // 下载政策文件
  downloadPolicyFile: (id) =>
    apiClient.get(`/policies/${id}/download`, {
      responseType: "blob",
      headers: {
        Accept: "application/pdf",
      },
    }),
};

// 银行相关API
export const bankApi = {
  // 银行账户认证
  auth: (data) => apiClient.post("/bank/auth", data),
  // 银行转账
  transfer: (data) => apiClient.post("/bank/transfer", data),
  // O-Convener 设置银行账户
  setupBankAccount: (data) => apiClient.post("/bank/setup-bank-account", data),
  // 获取当前组织 payment 账户信息
  getPaymentAccount: () => apiClient.get("/bank/get-payment-account"),
  // 更新银行账户信息
  updateBankAccount: (data) => apiClient.post("/bank/update-bank-account", data),
  // 组织间转账
  transferByOrg: (data) => apiClient.post("/bank/transfer-by-org", data),
};

// 服务管理相关API
export const servicesApi = {
  // 获取服务列表
  getServices: (params) => apiClient.get("/services", { params }),
  // 获取当前组织的服务列表
  getOrganizationServices: (params) => apiClient.get("/services/org-services", { params }),
  // 获取单个服务详情
  getService: (id) => apiClient.get(`/services/${id}`),
  // 创建新服务
  createService: (data) => {
    const organization_id = localStorage.getItem('organization_id')
    if (!organization_id) {
      return Promise.reject(new Error('Organization ID not found'))
    }
    return apiClient.post("/services", { ...data, organization_id })
  },
  // 更新服务信息
  updateService: (id, data) => apiClient.put(`/services/${id}`, data),
  // 删除服务
  deleteService: (id) => apiClient.delete(`/services/${id}`),
};

export default {
  auth: authApi,
  papers: papersApi,
  students: studentApi,
  courses: coursesApi,
  users: usersApi,
  organization: organizationApi,
  verification: verificationApi,
  help: helpApi,
  policies: policiesApi,
  bank: bankApi,
  services: servicesApi,
};
