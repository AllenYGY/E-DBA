<template>
  <a-card
    title="Personal Information"
    :loading="loading"
    class="profile-card"
    :bordered="false"
  >
    <a-descriptions 
      bordered 
      :column="2" 
      class="profile-descriptions"
      size="middle"
    >
      <a-descriptions-item label="Username" class="profile-item">
        <span class="profile-value">{{ userInfo.username }}</span>
        <a-button type="link" size="small" class="inline-edit-btn" @click="showEditFieldModal('username')">
          <template #icon><edit-outlined /></template>
          Edit
        </a-button>
      </a-descriptions-item>
      <a-descriptions-item label="User ID" class="profile-item">
        <span class="profile-value">{{ userInfo.id || '-' }}</span>
      </a-descriptions-item>
      <a-descriptions-item label="Email" class="profile-item">
        <span class="profile-value">{{ userInfo.email }}</span>
        <a-button type="link" size="small" class="inline-edit-btn" @click="showEditFieldModal('email')">
          <template #icon><edit-outlined /></template>
          Edit
        </a-button>
      </a-descriptions-item>
      <a-descriptions-item label="Role" class="profile-item">
        <a-tag :color="getRoleColor(userInfo.role)" class="profile-tag">{{ getRoleName(userInfo.role) }}</a-tag>
      </a-descriptions-item>
      <a-descriptions-item label="Permission Level" class="profile-item">
        <a-tag :color="userInfo.permission_level === 'admin' ? 'red' : 'green'" class="profile-tag">
          {{ userInfo.permission_level }} 
        </a-tag>
      </a-descriptions-item>
      <a-descriptions-item label="Organization" class="profile-item">
        <span class="profile-value">{{ userInfo.organization_short_name || '-' }}</span>
      </a-descriptions-item>
      <a-descriptions-item label="Organization ID" class="profile-item">
        <span class="profile-value">{{ userInfo.organization_id || '-' }}</span>
      </a-descriptions-item>
      <a-descriptions-item label="Organization Full Name" class="profile-item">
        <span class="profile-value">{{ userInfo.organization_full_name || '-' }}</span>
      </a-descriptions-item>
      <a-descriptions-item label="Balance" class="profile-item">
        <span class="profile-value balance">{{ userInfo.balance }} {{ userInfo.balance_unit || 'RMB' }}</span>
      </a-descriptions-item>
      <a-descriptions-item label="Registration Time" class="profile-item">
        <span class="profile-value">{{ formatDateTime(userInfo.created_at) }}</span>
      </a-descriptions-item>
    </a-descriptions>

    <!-- 编辑弹窗 -->
    <a-modal
      :open="editFieldModalVisible"
      @update:open="val => editFieldModalVisible = val"
      :title="editField === 'username' ? 'Edit Username' : 'Edit Email'"
      :confirmLoading="editFieldLoading"
      @ok="handleEditFieldOk"
      @cancel="() => (editFieldModalVisible = false)"
      destroyOnClose
      class="profile-modal"
    >
      <a-form :model="editFieldForm" layout="vertical">
        <a-form-item :label="editField === 'username' ? 'Username' : 'Email'">
          <a-input
            v-if="editField === 'username'"
            v-model:value="editFieldForm.username"
            placeholder="Enter new username"
          />
          <a-input
            v-else
            v-model:value="editFieldForm.email"
            placeholder="Enter new email"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </a-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { EditOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { usersApi } from '../../services/api'

const userInfo = ref({})
const loading = ref(false)

const editFieldModalVisible = ref(false)
const editField = ref('') // 'username' or 'email'
const editFieldForm = reactive({ username: '', email: '' })
const editFieldLoading = ref(false)

const fetchUserInfo = async () => {
  loading.value = true
  try {
    const res = await usersApi.getCurrentUser()
    userInfo.value = res.data
  } catch (e) {
    message.error('Failed to get personal information')
  } finally {
    loading.value = false
  }
}

const showEditFieldModal = (field) => {
  editField.value = field
  if (field === 'username') {
    editFieldForm.username = userInfo.value.username
  } else {
    editFieldForm.email = userInfo.value.email
  }
  editFieldModalVisible.value = true
}

const handleEditFieldOk = async () => {
  editFieldLoading.value = true
  try {
    if (editField.value === 'username') {
      await usersApi.updateCurrentUser({ username: editFieldForm.username })
      localStorage.setItem('username', editFieldForm.username)
      message.success('Username updated successfully')
    } else {
      await usersApi.updateCurrentUser({ email: editFieldForm.email })
      localStorage.setItem('email', editFieldForm.email)
      message.success('Email updated successfully')
    }
    editFieldModalVisible.value = false
    fetchUserInfo()
  } catch (e) {
    message.error('Failed to update')
  } finally {
    editFieldLoading.value = false
  }
}

// 获取角色名称
const getRoleName = (role) => {
  const roleMap = {
    'T_ADMIN': 'Technical admin',
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

// 格式化日期时间
const formatDateTime = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  const pad = (n) => n.toString().padStart(2, '0');
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ` +
         `${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
}

onMounted(() => {
  fetchUserInfo()
})
</script>

<style scoped>
.profile-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.profile-descriptions {
  margin-top: 8px;
}
.profile-descriptions :deep(.ant-descriptions-item-label) {
  width: 160px;
  font-weight: 500;
  color: #666;
  background-color: #fafafa;
}
.profile-item {
  padding: 16px 24px !important;
}
.profile-value {
  color: #1f1f1f;
  font-size: 14px;
}
.profile-tag {
  font-size: 13px;
  padding: 2px 8px;
  border-radius: 4px;
}
.balance {
  font-weight: 600;
  color: #1890ff;
}
.inline-edit-btn {
  margin-left: 8px;
  padding: 0 4px;
  font-size: 13px;
  vertical-align: middle;
}
</style> 