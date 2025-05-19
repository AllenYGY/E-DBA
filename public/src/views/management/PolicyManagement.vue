<template>
  <div class="policy-management">
    <div class="table-operations">
      <a-button type="primary" @click="showAddModal">Add Policy</a-button>
    </div>
    <a-table :columns="columns" :data-source="policies" :loading="loading" row-key="id">
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'action'">
          <a-space>
            <a-button type="link" @click="showEditModal(record)">Edit</a-button>
            <a-button type="link" danger @click="deletePolicy(record)">Delete</a-button>
            <a-button type="link" @click="downloadFile(record)">Download</a-button>
          </a-space>
        </template>
      </template>
    </a-table>
    <a-modal :open="modalVisible" :title="modalTitle" @ok="handleSubmit" @cancel="handleCancel">
      <a-form :model="form" layout="vertical">
        <a-form-item label="Policy Title" name="title">
          <a-input v-model:value="form.title" placeholder="Enter policy title" />
        </a-form-item>
        <a-form-item label="Description" name="description">
          <a-textarea v-model:value="form.description" placeholder="Enter description" :rows="3" />
        </a-form-item>
        <a-form-item label="Policy Document" name="file">
          <a-upload :file-list="fileList" :before-upload="beforeUpload" @remove="handleFileRemove"
            :show-upload-list="false">
            <a-button>
              <upload-outlined /> Select File
            </a-button>
          </a-upload>
          <!-- 自定义文件列表 -->
          <div v-if="fileList.length > 0" class="custom-file-list">
            <div v-for="file in fileList" :key="file.uid" class="custom-file-item">
              <div class="file-info">
                <a href="javascript:void(0);" class="file-name-link" @click="downloadFileByFile(file)">
                  {{ file.name }}
                </a>
                <a-space>
                  <a-button type="link" size="small" @click="downloadFileByFile(file)">
                    <download-outlined /> Download
                  </a-button>
                  <a-button type="text" size="small" @click="() => handleFileRemove(file)" class="file-remove-btn">
                    ×
                  </a-button>
                </a-space>
              </div>
            </div>
          </div>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message, Upload } from 'ant-design-vue';
import { policiesApi } from '../../services/api';
import { UploadOutlined, DownloadOutlined } from '@ant-design/icons-vue';

// API基础URL配置
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''; // 使用环境变量或空字符串(相对路径)

const loading = ref(false);
const policies = ref([]);
const modalVisible = ref(false);
const modalTitle = ref('Add Policy');
const form = reactive({ id: null, title: '', description: '', originalHadFile: false });
const fileList = ref([]);
const uploadFile = ref(null);

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id' },
  { title: 'Policy Title', dataIndex: 'title', key: 'title' },
  { title: 'Description', dataIndex: 'description', key: 'description' },
  { title: 'Created By', dataIndex: 'created_by_email', key: 'created_by_email' },
  { title: 'Created At', dataIndex: 'created_at', key: 'created_at' },
  { title: 'Action', key: 'action' },
];

const fetchPolicies = async () => {
  loading.value = true;
  try {
    const res = await policiesApi.getPolicies();
    console.log('policiesApi.getPolicies 返回：', res.data);
    policies.value = res.data.items;
    console.log('policies.value:', policies.value);
  } catch (e) {
    let errorMsg = 'Failed to fetch policies';
    if (e.response) {
      errorMsg += `: ${e.response.status} ${e.response.statusText}`;
    } else if (e.message) {
      errorMsg += `: ${e.message}`;
    }
    message.error(errorMsg);
    console.error('Fetch policies error:', e);
  } finally {
    loading.value = false;
  }
};

const beforeUpload = (file) => {
  // 定义允许的文件类型 (例如: PDF, Word, Excel等)
  const allowedTypes = ['application/pdf', 'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/plain']; // 添加txt文件支持

  const isAllowedType = allowedTypes.includes(file.type);
  if (!isAllowedType) {
    message.error('Only PDF, Office documents and text files are allowed');
    return Upload.LIST_IGNORE;
  }

  // 限制文件大小为10MB
  const isLt10M = file.size / 1024 / 1024 < 10;
  if (!isLt10M) {
    message.error('File must be smaller than 10MB');
    return Upload.LIST_IGNORE;
  }

  uploadFile.value = file;
  fileList.value = [{
    uid: file.uid,
    name: file.name,
    status: 'done',
    originFileObj: file
  }];
  return false; // 阻止自动上传
};

const handleFileRemove = (file) => {
  uploadFile.value = null;
  fileList.value = [];
  console.log('File removed:', file?.name || 'all files');
};

const showAddModal = () => {
  modalTitle.value = 'Add Policy';
  form.id = null;
  form.title = '';
  form.description = '';
  form.originalHadFile = false;
  uploadFile.value = null;
  fileList.value = [];
  modalVisible.value = true;
};

const showEditModal = async (record) => {
  modalTitle.value = 'Edit Policy';
  form.id = record.id;
  form.title = record.title;
  form.description = record.description;
  form.originalHadFile = false; // 先假设没有

  uploadFile.value = null;
  fileList.value = [];

  // 直接尝试请求 download 接口
  try {
    const response = await policiesApi.downloadPolicyFile(record.id);
    // 获取文件名
    let fileName = `policy_${record.id}.pdf`;
    const contentDisposition = response.headers['content-disposition'];
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['\"]).*?\2|[^;\n]*)/);
      if (filenameMatch && filenameMatch[1]) {
        fileName = filenameMatch[1].replace(/['"]/g, '');
      }
    }
    // 有文件就显示
    fileList.value = [{
      uid: '-1',
      name: fileName,
      status: 'done',
      url: `${API_BASE_URL}/api/v1/policies/${record.id}/download`
    }];
    form.originalHadFile = true;
  } catch (e) {
    // 没有文件就不显示
    fileList.value = [];
    form.originalHadFile = false;
  }

  modalVisible.value = true;
};

const handleSubmit = async () => {
  try {
    if (!form.title) {
      message.warning('请输入政策标题');
      return;
    }

    // 创建FormData
    const formData = new FormData();
    formData.append('title', form.title);
    formData.append('description', form.description || '');
    formData.append('is_active', 'true'); // 添加is_active字段
    
    console.log('表单提交 - 模式:', form.id ? '更新' : '创建');
    
    // 处理文件
    if (form.id) { // 更新模式
      if (uploadFile.value) {
        console.log('上传新文件:', uploadFile.value.name, '大小:', uploadFile.value.size);
        
        // 确保使用原始File对象
        formData.append('file', uploadFile.value, uploadFile.value.name);
        
        // 不要在上传新文件时设置remove_file
        console.log('添加新文件 - 不设置remove_file');
      } 
      else if (form.originalHadFile && fileList.value.length === 0) {
        // 只有当原来有文件且现在列表为空时才移除文件
        console.log('设置remove_file=true');
        formData.append('remove_file', 'true');
      }
      
      // 调试信息：检查FormData内容
      for (const pair of formData.entries()) {
        console.log(`FormData字段: ${pair[0]} = ${pair[1] instanceof File ? `[文件: ${pair[1].name}, 大小: ${pair[1].size}]` : pair[1]}`);
      }
      
      const loadingMsg = message.loading('正在更新政策...', 0);
      const response = await policiesApi.updatePolicy(form.id, formData);
      loadingMsg();
      
      console.log('更新响应:', response);
      message.success('政策更新成功');
    } else {
      // 创建模式
      if (uploadFile.value) {
        console.log('添加文件到新政策:', uploadFile.value.name);
        formData.append('file', uploadFile.value, uploadFile.value.name);
      }
      
      const loadingMsg = message.loading('正在创建政策...', 0);
      await policiesApi.createPolicy(formData);
      loadingMsg();
      
      message.success('政策创建成功');
    }
    
    modalVisible.value = false;
    fetchPolicies();
  } catch (e) {
    console.error('提交错误:', e);
    message.error(`操作失败: ${e.message || '未知错误'}`);
  }
};

const handleCancel = () => {
  modalVisible.value = false;
};

const deletePolicy = async (record) => {
  try {
    await policiesApi.deletePolicy(record.id);
    message.success('Policy deleted successfully');
    fetchPolicies();
  } catch (e) {
    let errorMsg = 'Delete failed';
    if (e.response) {
      errorMsg += `: ${e.response.status} ${e.response.statusText}`;
      if (e.response.data && e.response.data.detail) {
        errorMsg += ` - ${e.response.data.detail}`;
      }
    } else if (e.message) {
      errorMsg += `: ${e.message}`;
    }
    message.error(errorMsg);
    console.error('Delete policy error:', e);
  }
};

// 表格中的下载文件函数
const downloadFile = async (record) => {
  try {
    const response = await policiesApi.downloadPolicyFile(record.id);
    const blob = response.data;
    
    // 从Content-Disposition获取文件名
    let filename = `policy_${record.id}.pdf`;
    const contentDisposition = response.headers['content-disposition'];
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
      if (filenameMatch && filenameMatch[1]) {
        filename = filenameMatch[1].replace(/['"]/g, '');
      }
    }

    // 创建一个临时下载链接并触发它
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();

    // 清理
    window.URL.revokeObjectURL(downloadUrl);
    document.body.removeChild(link);

    message.success(`Downloading ${filename}`);
  } catch (error) {
    let errorMsg = 'Download failed';
    if (error.response?.data?.detail) {
      errorMsg = error.response.data.detail;
    } else if (error.message) {
      errorMsg = error.message;
    }
    message.error(errorMsg);
    console.error('Download error:', error);
  }
};

// 处理文件对象下载的函数
const downloadFileByFile = async (file) => {
  if (file.originFileObj) {
    // 新上传的文件，直接用 File 对象生成下载
    const url = window.URL.createObjectURL(file.originFileObj);
    const link = document.createElement('a');
    link.href = url;
    link.download = file.name;
    document.body.appendChild(link);
    link.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(link);
    message.success(`Downloading ${file.name}`);
  } else if (file.url) {
    // 旧文件，走后端接口
    // 正确提取 policyId
    const match = file.url.match(/policies\/(\d+)\/download/);
    const policyId = match ? match[1] : null;
    if (!policyId) {
      message.error('Invalid policy ID');
      return;
    }
    const response = await policiesApi.downloadPolicyFile(policyId);
    const blob = response.data;
    let filename = file.name;
    const contentDisposition = response.headers['content-disposition'];
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
      if (filenameMatch && filenameMatch[1]) {
        filename = filenameMatch[1].replace(/['"]/g, '');
      }
    }
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    window.URL.revokeObjectURL(downloadUrl);
    document.body.removeChild(link);
    message.success(`Downloading ${filename}`);
  }
};

// 格式化日期显示
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString();
};

// 初始化加载
onMounted(() => {
  fetchPolicies();
});
</script>

<style scoped>
.policy-management {
  padding: 24px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.table-operations {
  margin-bottom: 16px;
  display: flex;
  gap: 16px;
}

/* 文件列表的自定义样式 */
.custom-file-list {
  margin-top: 8px;
}

.file-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 8px;
}

.custom-file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  margin-bottom: 4px;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  background-color: #fafafa;
}

.file-name-link {
  color: #1890ff;
  text-decoration: none;
  max-width: 60%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-name-link:hover {
  color: #40a9ff;
  text-decoration: underline;
}

.file-remove-btn {
  color: rgba(0, 0, 0, 0.45);
  padding: 0 4px;
  transition: all 0.3s;
}

.file-remove-btn:hover {
  color: #ff4d4f;
}

@media (max-width: 768px) {
  .policy-management {
    padding: 16px;
  }

  .custom-file-item {
    padding: 4px;
  }
}
</style>
