<template>
  <div class="user-management-container">
    <a-page-header 
      title="User Management" 
      sub-title="Manage system users"
    />

    <a-card :bordered="false">
      <div class="search-section">
        <a-space>
          <a-input v-model:value="searchForm.username" placeholder="Username" style="width: 150px" allowClear @change="handleSearch" />
          <a-input v-model:value="searchForm.email" placeholder="Email" style="width: 180px" allowClear @change="handleSearch" />
          <a-select v-model:value="searchForm.role" placeholder="Role" style="width: 140px" allowClear @change="handleSearch">
            <a-select-option value="T_ADMIN">T-Admin</a-select-option>
            <a-select-option value="E_ADMIN">E-Admin</a-select-option>
            <a-select-option value="SENIOR_E_ADMIN">Senior E-Admin</a-select-option>
            <a-select-option value="O_CONVENER">O-Convener</a-select-option>
            <a-select-option value="DATA_USER">Data User</a-select-option>
          </a-select>
          <a-input 
            v-model:value="searchForm.organization_id" 
            placeholder="Org ID" 
            style="width: 100px" 
            allowClear 
            @change="handleSearch"
            :disabled="searchForm.isOrgIdDisabled"
            :title="searchForm.isOrgIdDisabled ? 'Organization ID is locked for O-Convener' : ''"
          />
          <a-input v-model:value="searchForm.permission_level" placeholder="Perm. Level" style="width: 100px" allowClear @change="handleSearch" />
          <a-button type="primary" @click="handleSearch">
            <template #icon><search-outlined /></template>
            Search
          </a-button>
        </a-space>

        <div class="action-buttons">
          <a-button 
            type="default" 
            danger 
            :disabled="!selectedRowKeys.length" 
            @click="handleBatchDelete"
          >
            <template #icon><delete-outlined /></template>
            Batch Delete
          </a-button>
          
          <a-button 
            type="primary" 
            @click="handleAdd"
          >
            <template #icon><plus-outlined /></template>
            Add User
          </a-button>

          <a-button type="default" @click="showBatchImportModal">
            <template #icon><upload-outlined /></template>
            Select Excel File (.xlsx)
          </a-button>
        </div>
      </div>

      <div class="table-container">
        <a-table 
          :columns="columns" 
          :data-source="displayedUsers" 
          :loading="loading" 
          :pagination="pagination"
          :row-selection="{ 
            selectedRowKeys: selectedRowKeys, 
            onChange: onSelectChange 
          }" 
          @change="handleTableChange"
          row-key="id"
          :bordered="false"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'role'">
              <a-tag :color="getRoleColor(record.role)">
                {{ getRoleName(record.role) }}
              </a-tag>
            </template>
            
            <template v-else-if="column.key === 'status'">
              <a-space>
                <a-badge 
                  :status="record.is_active ? 'success' : 'error'"
                  :text="record.is_active ? 'Active' : 'Disabled'" 
                />
                <a-tag v-if="record.is_deleted" color="red">Deleted</a-tag>
              </a-space>
            </template>
            
            <template v-else-if="column.key === 'balance'">
              {{ record.balance }} RMB
            </template>
            
            <template v-else-if="column.key === 'created_at'">
              {{ formatDate(record.created_at) }}
            </template>
            
            <template v-else-if="column.key === 'updated_at'">
              {{ formatDate(record.updated_at) }}
            </template>
            
            <template v-else-if="column.key === 'deleted_at'">
              {{ record.deleted_at ? formatDate(record.deleted_at) : '-' }}
            </template>
            
            <template v-else-if="column.key === 'action'">
              <a-space>
                <a-button type="link" size="small" @click="editUser(record)">
                  <template #icon><edit-outlined /></template>
                  Edit
                </a-button>
                <a-popconfirm
                  title="Are you sure you want to delete this user?"
                  ok-text="Confirm"
                  cancel-text="Cancel"
                  @confirm="deleteUser(record)"
                >
                  <a-button type="link" danger size="small">
                    <template #icon><delete-outlined /></template>
                    Delete
                  </a-button>
                </a-popconfirm>
              </a-space>
            </template>
          </template>
        </a-table>
      </div>
    </a-card>

    <a-modal
      :open="modalVisible"
      :title="modalTitle"
      @ok="handleModalOk"
      @cancel="() => { modalVisible = false }"
      :confirmLoading="modalLoading"
      :maskClosable="false"
      width="600px"
    >
      <a-form
        :model="userForm"
        :rules="rules"
        ref="userFormRef"
        layout="vertical"
      >
        <a-form-item label="Username" name="username">
          <a-input 
            v-model:value="userForm.username" 
            placeholder="Enter username"
            :maxLength="20"
          />
        </a-form-item>
        
        <a-form-item label="Email" name="email">
          <a-input 
            v-model:value="userForm.email" 
            placeholder="Enter email"
          />
        </a-form-item>
        
        <a-form-item label="Password" name="password" :rules="rules.password">
          <a-input-password
            v-model:value="userForm.password"
            placeholder="Enter password"
            :maxLength="32"
            autocomplete="new-password"
          />
        </a-form-item>
        
        <a-form-item label="Role" name="role">
          <a-select
            v-model:value="userForm.role"
            placeholder="Select role"
            :disabled="currentUserRole === 'O_CONVENER'"
          >
            <a-select-option value="DATA_USER">Data User</a-select-option>
            <a-select-option
              v-if="currentUserRole !== 'O_CONVENER'"
              value="T_ADMIN"
            >T-Admin</a-select-option>
            <a-select-option
              v-if="currentUserRole !== 'O_CONVENER'"
              value="E_ADMIN"
            >E-Admin</a-select-option>
            <a-select-option
              v-if="currentUserRole !== 'O_CONVENER'"
              value="SENIOR_E_ADMIN"
            >Senior E-Admin</a-select-option>
            <a-select-option
              v-if="currentUserRole !== 'O_CONVENER'"
              value="O_CONVENER"
            >O-Convener</a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item label="Permission Level" name="permission_level">
          <a-input-number 
            v-model:value="userForm.permission_level" 
            :min="1" 
            :max="3" 
            placeholder="1-3"
            style="width: 100%"
          />
        </a-form-item>
        
        <a-form-item label="Balance" name="balance">
          <a-input-number 
            v-model:value="userForm.balance" 
            :min="0" 
            :step="100" 
            placeholder="Enter balance"
            style="width: 100%"
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <a-modal
      :open="batchImportVisible"
      title="Batch Import Users"
      @ok="handleBatchImport"
      @cancel="() => { batchImportVisible = false }"
      :confirmLoading="batchImportLoading"
      :maskClosable="false"
      width="600px"
    >
      <a-upload
        :maxCount="1"
        accept=".xlsx"
        :customRequest="() => {}"
        @change="handleBatchFileChange"
        :fileList="batchImportFile ? [batchImportFile] : []"
        :showUploadList="{ showRemoveIcon: true }"
      >
        <a-button>
          <template #icon><upload-outlined /></template>
          Select Excel File (.xlsx)
        </a-button>
      </a-upload>
      <div style="margin-top: 16px; display: flex; justify-content: space-between; align-items: center;">
        <a-alert
          message="Excel must contain columns: username, email, password (headers must be lowercase, no extra spaces, no merged cells)"
          type="info"
          show-icon
        />
        <a-button type="link" @click="downloadTemplate">
          <template #icon><download-outlined /></template>
          Download Template
        </a-button>
      </div>
      <div v-if="batchImportResult.length" style="margin-top: 16px; max-height: 200px; overflow-y: auto;">
        <a-list
          :dataSource="batchImportResult"
          bordered
          size="small"
        >
          <template #renderItem="{ item }">
            <a-list-item>
              <template v-if="item.success">
                <span style="color: green;">✔</span>
                <span style="margin-left: 8px;">{{ item.email }} - Success (ID: {{ item.user_id }})</span>
              </template>
              <template v-else>
                <span style="color: red;">✖</span>
                <span style="margin-left: 8px;">
                  {{ item.email }} - Failed: {{ item.reason }}
                  <a-tooltip v-if="item.reason.includes('format')" title="Please check if the Excel file follows the required format">
                    <info-circle-outlined style="margin-left: 4px;" />
                  </a-tooltip>
                </span>
              </template>
            </a-list-item>
          </template>
        </a-list>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, computed } from 'vue'
import { message, Modal } from 'ant-design-vue'
import { PlusOutlined, EditOutlined, DeleteOutlined, SearchOutlined, UploadOutlined, DownloadOutlined, InfoCircleOutlined } from '@ant-design/icons-vue'
import { usersApi } from '../../services/api'

// 表格列定义
const columns = [
  {
    title: 'ID',
    dataIndex: 'id',
    key: 'id',
    sorter: (a, b) => a.id - b.id,
  },
  {
    title: 'Username',
    dataIndex: 'username',
    key: 'username',
    sorter: (a, b) => (a.username || '').localeCompare(b.username || ''),
  },
  {
    title: 'Email',
    dataIndex: 'email',
    key: 'email',
    sorter: (a, b) => (a.email || '').localeCompare(b.email || ''),
  },
  {
    title: 'Role',
    dataIndex: 'role',
    key: 'role',
    sorter: (a, b) => (a.role || '').localeCompare(b.role || ''),
  },
  {
    title: 'Permission Level',
    dataIndex: 'permission_level',
    key: 'permission_level',
    sorter: (a, b) => (a.permission_level || 0) - (b.permission_level || 0),
  },
  {
    title: 'Organization ID',
    dataIndex: 'organization_id',
    key: 'organization_id',
    sorter: (a, b) => {
      const aVal = a.organization_id === null ? -Infinity : a.organization_id;
      const bVal = b.organization_id === null ? -Infinity : b.organization_id;
      return aVal - bVal;
    },
  },
  {
    title: 'Balance',
    dataIndex: 'balance',
    key: 'balance',
    sorter: (a, b) => (a.balance || 0) - (b.balance || 0),
  },
  {
    title: 'Status',
    key: 'status',
    sorter: (a, b) => {
      // First compare is_active
      if (a.is_active !== b.is_active) {
        return a.is_active ? 1 : -1;
      }
      // Then compare is_deleted
      return (a.is_deleted ? -1 : 1) - (b.is_deleted ? -1 : 1);
    },
  },
  {
    title: 'Created At',
    dataIndex: 'created_at',
    key: 'created_at',
    sorter: (a, b) => new Date(a.created_at || 0) - new Date(b.created_at || 0),
  },
  {
    title: 'Updated At',
    dataIndex: 'updated_at',
    key: 'updated_at',
    sorter: (a, b) => new Date(a.updated_at || 0) - new Date(b.updated_at || 0),
  },
  {
    title: 'Deleted At',
    dataIndex: 'deleted_at',
    key: 'deleted_at',
    sorter: (a, b) => {
      // Handle null values for deleted_at
      if (!a.deleted_at && !b.deleted_at) return 0;
      if (!a.deleted_at) return -1;
      if (!b.deleted_at) return 1;
      return new Date(a.deleted_at) - new Date(b.deleted_at);
    },
  },
  {
    title: 'Action',
    key: 'action',
    fixed: 'right',
    width: 150,
  },
]

// 状态定义
const users = ref([])
const loading = ref(false)
const modalVisible = ref(false)
const modalLoading = ref(false)
const modalTitle = ref('Add User')
const editMode = ref(false)
const userFormRef = ref(null)
const searchForm = reactive({
  username: '',
  email: '',
  role: '',
  organization_id: '',
  permission_level: '',
  isOrgIdDisabled: computed(() => currentUserRole.value === 'O_CONVENER')
})
const selectedRowKeys = ref([])
const sortState = reactive({
  field: null,
  order: null
})

// 添加当前用户信息
const currentUserRole = ref(localStorage.getItem('role') || '')
const currentUserOrgId = ref(Number(localStorage.getItem('organization_id')) || null)

// 计算属性：处理排序和分页的用户列表
const displayedUsers = computed(() => {
  let result = [...users.value];

  // 如果有排序条件，应用排序
  if (sortState.field && sortState.order) {
    const column = columns.find(col => col.key === sortState.field);
    if (column && column.sorter) {
      // 使用列的sorter函数排序
      result.sort(column.sorter);

      // 如果是降序，反转结果
      if (sortState.order === 'descend') {
        result.reverse();
      }
    }
  }

  return result;
});

// 用户表单
const userForm = reactive({
  id: null,
  username: '',
  email: '',
  role: 'DATA_USER',
  permission_level: 1,
  organization_id: null,
  balance: 0,
  is_active: true,
  password: '',
})

// 表单验证规则
const rules = {
  username: [
    { required: true, message: 'Please enter username', trigger: 'blur' },
    { min: 3, max: 20, message: 'Username must be 3-20 characters', trigger: 'blur' },
  ],
  email: [
    { required: true, message: 'Please enter email', trigger: 'blur' },
    { type: 'email', message: 'Please enter a valid email address', trigger: 'blur' },
  ],
  role: [
    { required: true, message: 'Please select role', trigger: 'change' },
  ],
  permission_level: [
    { required: true, message: 'Please select permission level', trigger: 'change' },
  ],
  password: [
    {
      required: true, message: 'Please enter password', trigger: 'blur', validator: (rule, value) => {
        if (editMode.value) return Promise.resolve()
        return value ? Promise.resolve() : Promise.reject('Please enter password')
      }
    },
    { min: 6, message: 'Password must be at least 6 characters', trigger: 'blur' },
  ],
}

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showTotal: (total) => `Total ${total} records`,
  showQuickJumper: true,
})

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 获取角色名称
const getRoleName = (role) => {
  const roleMap = {
    'T_ADMIN': 'T-Admin',
    'E_ADMIN': 'E-Admin',
    'SENIOR_E_ADMIN': 'Senior E-Admin',
    'O_CONVENER': 'O-Convener',
    'DATA_USER': 'Data User'
  }
  return roleMap[role] || role
}

// 获取角色颜色
const getRoleColor = (role) => {
  const colorMap = {
    'T_ADMIN': 'red',
    'E_ADMIN': 'green',
    'SENIOR_E_ADMIN': 'blue',
    'O_CONVENER': 'orange',
    'DATA_USER': 'purple'
  }
  return colorMap[role] || 'default'
}

// 初始加载数据
onMounted(() => {
  // 如果是 O-Convener，自动填充组织 ID
  if (currentUserRole.value === 'O_CONVENER' && currentUserOrgId.value) {
    searchForm.organization_id = currentUserOrgId.value.toString()
  }
  fetchUsers()
})

// 获取用户列表
const fetchUsers = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.current - 1) * pagination.pageSize,
      limit: pagination.pageSize,
    }
    // 只传递有值的搜索条件
    if (searchForm.username) params.username = searchForm.username
    if (searchForm.email) params.email = searchForm.email
    if (searchForm.role) params.role = searchForm.role
    // 如果是 O-Convener，强制使用其组织 ID
   
    if (currentUserRole.value === 'O_CONVENER') {
      params.organization_id = currentUserOrgId.value
      console.log('currentUserOrgId.value:', currentUserOrgId.value)
    } else if (searchForm.organization_id) {
      params.organization_id = Number(searchForm.organization_id)
    }

    if (searchForm.permission_level) params.permission_level = Number(searchForm.permission_level)

    console.log('Search params:', params)

    const response = await usersApi.searchUsers(params)
    
    if (response.data && response.data.items) {
      // 如果是 O-Convener，过滤掉不属于自己组织的数据
      if (currentUserRole.value === 'O_CONVENER') {
        users.value = response.data.items.filter(user => 
          user.organization_id === currentUserOrgId.value
        )
      } else {
        users.value = response.data.items
      }
      pagination.total = response.data.total || 0
    } else {
      message.error('Get user list failed: Invalid data format')
    }
  } catch (error) {
    message.error('Get user list failed, please try again later')
  } finally {
    loading.value = false
  }
}

// 表格变化处理（分页、排序等）
const handleTableChange = (pag, filters, sorter) => {
  console.log('Table change:', pag, filters, sorter);

  // 处理分页变化
  pagination.current = pag.current;
  pagination.pageSize = pag.pageSize;

  // 处理排序变化 - 现在在前端处理
  if (sorter && sorter.field) {
    sortState.field = sorter.columnKey || sorter.field;
    sortState.order = sorter.order;
    console.log('Sort state updated:', sortState);
  } else {
    // 清除排序
    sortState.field = null;
    sortState.order = null;
  }

  // 无论分页还是排序变化，都重新获取数据
  fetchUsers();
}

// 编辑用户
const editUser = async (record) => {
  console.log('Edit user clicked for record:', record);

  resetForm();

  editMode.value = true;
  modalTitle.value = 'Edit User';

  // 先显示模态窗
  modalVisible.value = true;

  try {
    // 获取用户详细信息
    const response = await usersApi.getUserById(record.id);
    console.log('User API response:', response.data);

    if (response.data) {
      const userData = response.data;

      // 直接为每个字段赋值，确保类型正确
      userForm.id = Number(userData.id || 0);
      userForm.username = userData.username || '';
      userForm.email = userData.email || '';
      userForm.role = userData.role || 'O_CONVENER';
      userForm.permission_level = Number(userData.permission_level || 1);
      userForm.organization_id = userData.organization_id ? Number(userData.organization_id) : null;
      userForm.balance = Number(userData.balance || 0);

      // 使用nextTick确保UI更新
      nextTick(() => {
        console.log('Form populated with data after nextTick:', JSON.stringify(userForm));

        // 如果有Form实例，手动更新表单
        if (userFormRef.value) {
          userFormRef.value.setFieldsValue(userForm);
        }
      });
    } else {
      message.error('Get user details failed: Invalid data format');
    }
  } catch (error) {
    console.error('Get user details failed:', error);

    // 如果API请求失败，尝试使用表格中的数据
    userForm.id = Number(record.id || 0);
    userForm.username = record.username || '';
    userForm.email = record.email || '';
    userForm.role = record.role || 'O_CONVENER';
    userForm.permission_level = Number(record.permission_level || 1);
    userForm.organization_id = record.organization_id ? Number(record.organization_id) : null;
    userForm.balance = Number(record.balance || 0);

    // 使用nextTick确保UI更新
    nextTick(() => {
      if (userFormRef.value) {
        userFormRef.value.setFieldsValue(userForm);
      }
    });

    message.warning('Editing user with cached data, some information may be incomplete');
  }
}

// 删除用户
const deleteUser = async (record) => {
  // 如果是 O-Convener，检查是否在删除自己组织的用户
  if (currentUserRole.value === 'O_CONVENER' && record.organization_id !== currentUserOrgId.value) {
    message.error('You can only delete users in your organization')
    return
  }

  console.log('Delete user called for:', record.id);
  try {
    await usersApi.deleteUser(record.id)
    message.success('Delete user successfully')
    fetchUsers() // 刷新列表
  } catch (error) {
    console.error('Delete user failed:', error)
    if (error.response) {
      message.error(error.response.data.detail || 'Delete user failed, please try again later')
    } else {
      message.error('Delete user failed, please try again later')
    }
  }
}

// 处理模态框确认
const handleModalOk = async () => {
  try {
    await userFormRef.value.validate()

    // 如果是 O-Convener，强制设置组织 ID
    if (currentUserRole.value === 'O_CONVENER') {
      userForm.organization_id = currentUserOrgId.value
    }

    modalLoading.value = true

    if (editMode.value) {
      // 如果是 O-Convener，检查是否在修改自己组织的用户
      if (currentUserRole.value === 'O_CONVENER') {
        const userToEdit = users.value.find(u => u.id === userForm.id)
        if (!userToEdit || userToEdit.organization_id !== currentUserOrgId.value) {
          message.error('You can only edit users in your organization')
          modalLoading.value = false
          return
        }
      }

      const response = await usersApi.updateUser(userForm.id, userForm)
      console.log('response:', response.data)
      if (response.data) {
        message.success('User updated successfully')
        modalVisible.value = false
        fetchUsers() // 刷新列表
        resetForm()
      } else {
        message.error('Update user failed: Invalid data format')
      }
    } else {
      // 创建用户
      console.log('Create user:', userForm)
      const response = await usersApi.createUser(userForm)
      console.log('Create user response:', response.data)
      if (response.data) {
        message.success('User created successfully')
        modalVisible.value = false
        fetchUsers() // 刷新列表
        resetForm()
      } else {
        message.error('Create user failed: Invalid data format')
      }
    }
  } catch (error) {
    console.error('Save user failed:', error)
    if (error.response) {
      // 处理邮箱重复的错误
      if (error.response.status === 400 && error.response.data.detail === "该邮箱已被其他用户使用") {
        message.error('The email has already been used by another user')
      } else {
        message.error(error.response.data.detail || 'Save user failed, please try again later')
      }
    } else {
      message.error('Save user failed, please try again later')
    }
  } finally {
    modalLoading.value = false
  }
}

// 重置表单
const resetForm = () => {
  userForm.id = null;
  userForm.username = '';
  userForm.email = '';
  userForm.role = 'DATA_USER';
  userForm.permission_level = 1;
  userForm.balance = 1000;
  userForm.is_active = true;
  userForm.password = '';
  if (currentUserRole.value === 'O_CONVENER') {
    userForm.organization_id = currentUserOrgId.value;
  } else {
    userForm.organization_id = null;
  }
  nextTick(() => {
    if (userFormRef.value) {
      userFormRef.value.resetFields();
    }
  });
  editMode.value = false;
  modalTitle.value = 'Add User';
  console.log('Form reset completed. Current form state:', JSON.stringify(userForm));
}

// 修改 handleSearch 只做简单校验和重置页码
const handleSearch = () => {
  // 如果是 O-Convener，重置组织 ID 为当前用户的组织 ID
  if (currentUserRole.value === 'O_CONVENER') {
    searchForm.organization_id = currentUserOrgId.value.toString()
  } else {
    // 校验数字类型
    if (searchForm.organization_id && isNaN(Number(searchForm.organization_id))) {
      message.error('Organization ID must be a number')
      return
    }
  }
  
  if (searchForm.permission_level && (isNaN(Number(searchForm.permission_level)) || Number(searchForm.permission_level) < 1 || Number(searchForm.permission_level) > 3)) {
    message.error('Permission level must be a number between 1 and 3')
    return
  }
  pagination.current = 1
  fetchUsers()
}

// 添加行选择处理函数
const onSelectChange = (keys) => {
  console.log('Selected row keys changed:', keys);
  selectedRowKeys.value = keys;
}

// 添加批量删除处理函数，修复API使用
const handleBatchDelete = () => {
  if (!selectedRowKeys.value.length) return;

  // 如果是 O-Convener，检查是否都在删除自己组织的用户
  if (currentUserRole.value === 'O_CONVENER') {
    const selectedUsers = users.value.filter(user => selectedRowKeys.value.includes(user.id))
    const hasOtherOrgUser = selectedUsers.some(user => user.organization_id !== currentUserOrgId.value)
    if (hasOtherOrgUser) {
      message.error('You can only delete users in your organization')
      return
    }
  }

  console.log('Batch delete button clicked for', selectedRowKeys.value.length, 'users');

  Modal.confirm({
    title: 'Confirm Deletion',
    content: `Are you sure you want to delete the selected ${selectedRowKeys.value.length} users?`,
    okText: 'Yes',
    okType: 'danger',
    cancelText: 'No',
    onOk: async () => {
      console.log('Confirm button clicked, proceeding with deletion');
      try {
        const deletePromises = selectedRowKeys.value.map(id => usersApi.deleteUser(id));
        await Promise.all(deletePromises);
        message.success('Batch delete successfully');
        selectedRowKeys.value = [];
        fetchUsers();
      } catch (error) {
        console.error('Batch delete failed:', error);
        message.error('Batch delete failed, please try again later');
      }
    },
    onCancel() {
      console.log('Cancel button clicked');
    },
  });
}

// 添加新增用户处理函数
const handleAdd = () => {
  console.log('Add button clicked')
  resetForm()
  editMode.value = false
  modalTitle.value = 'Add User'
  modalVisible.value = true
}

const batchImportVisible = ref(false)
const batchImportLoading = ref(false)
const batchImportResult = ref([])
const batchImportFile = ref(null)

const showBatchImportModal = () => {
  batchImportVisible.value = true
  batchImportResult.value = []
  batchImportFile.value = null
}

const handleBatchFileChange = (info) => {
  if (info.file.status === 'removed') {
    batchImportFile.value = null
  } else {
    const file = info.file.originFileObj
    if (file && file.name && file.name.toLowerCase().endsWith('.xlsx')) {
      batchImportFile.value = info.file
    } else {
      message.error('Invalid file type. Please upload an .xlsx file.')
      batchImportFile.value = null
    }
  }
}

const handleBatchImport = async () => {
  if (!batchImportFile.value) {
    message.error('Please select an Excel file')
    return
  }
  batchImportLoading.value = true
  try {
    const formData = new FormData()
    formData.append('file', batchImportFile.value.originFileObj)
    const response = await usersApi.batchCreateUsers(formData)
    
    if (response.data && response.data.results) {
      batchImportResult.value = response.data.results
      message.success('Batch import completed')
      fetchUsers()
    }
  } catch (error) {
    console.error('Batch import error:', error)
    message.error(error.response?.data?.detail || 'Batch import failed')
  } finally {
    batchImportLoading.value = false
  }
}

// 添加下载模板函数
const downloadTemplate = () => {
  // 创建一个示例 Excel 文件
  const template = [
    ['username', 'email', 'password', 'permission_level','role'],
    ['example_user1', 'example_user1@example.com', 'password123', '1','DATA_USER'],
    ['example_user2', 'example_user2@example.com', 'password123', '2','DATA_USER'],
    ['example_user3', 'example_user3@example.com', 'password123', '3','DATA_USER']
  ]
  
  // 将数据转换为 CSV 格式
  const csvContent = template.map(row => row.join(',')).join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = 'user_import_template.csv'
  link.click()
  URL.revokeObjectURL(link.href)
}
</script>

<style scoped>
.user-management-container {
  padding: 24px;
  background: #f0f2f5;
  min-height: calc(100vh - 64px);
}

.mb-20 {
  margin-bottom: 20px;
}

:deep(.ant-card) {
  border-radius: 8px;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03), 
              0 1px 6px -1px rgba(0, 0, 0, 0.02), 
              0 2px 4px 0 rgba(0, 0, 0, 0.02);
}

:deep(.ant-card-body) {
  padding: 24px;
}

:deep(.ant-table) {
  border-radius: 8px;
}

:deep(.ant-table-thead > tr > th) {
  background: #fafafa;
  font-weight: 600;
}

:deep(.ant-table-tbody > tr:hover > td) {
  background: #f5f5f5;
}

:deep(.ant-input), 
:deep(.ant-input-search), 
:deep(.ant-select:not(.ant-select-customize-input) .ant-select-selector),
:deep(.ant-btn) {
  border-radius: 6px;
}

:deep(.ant-tag) {
  border-radius: 4px;
  padding: 2px 8px;
  font-weight: 500;
}

:deep(.ant-badge-status-dot) {
  width: 8px;
  height: 8px;
}

:deep(.ant-page-header) {
  padding: 16px 24px;
  background: white;
  border-radius: 8px;
  margin-bottom: 24px;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
}

:deep(.ant-page-header-heading-title) {
  font-weight: 600;
  font-size: 20px;
}

:deep(.ant-page-header-heading-sub-title) {
  color: #8c8c8c;
}

:deep(.ant-btn-primary) {
  height: 34px;
  font-weight: 500;
  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.015);
}

:deep(.ant-btn-primary[type="button"]) {
  background: #1890ff;
  border-color: #1890ff;
}

:deep(.ant-btn-primary[type="button"]:hover) {
  background: #40a9ff;
  border-color: #40a9ff;
}

:deep(.ant-btn-dangerous.ant-btn-primary) {
  background: #ff4d4f;
  border-color: #ff4d4f;
}

:deep(.ant-btn-dangerous.ant-btn-primary:hover) {
  background: #ff7875;
  border-color: #ff7875;
}

:deep(.ant-modal-content) {
  border-radius: 8px;
}

:deep(.ant-modal-header) {
  border-radius: 8px 8px 0 0;
}

:deep(.ant-form-item-label > label) {
  font-weight: 500;
}

.search-section {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.table-container {
  background: white;
  border-radius: 8px;
  padding: 24px;
}
</style>
