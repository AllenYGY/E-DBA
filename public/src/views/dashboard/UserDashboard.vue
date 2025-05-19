<template>
  <a-layout class="dashboard-layout">
    <a-layout-sider :collapsed="collapsed" :trigger="null" collapsible class="dashboard-sider">
      <div class="logo">
        <img src="/vite.svg" alt="Workspace Logo" />
        <span v-if="!collapsed">Data User</span>
      </div>
      
      <a-menu :selectedKeys="selectedKeys" theme="dark" mode="inline">
        <a-menu-item key="overview" @click="() => setContent('overview')">
          <template #icon>
            <UserOutlined />
          </template>
          <span>Dashboard</span>
        </a-menu-item>

        <a-menu-item key="workspace" @click="() => setContent('workspace')">
          <template #icon>
            <AppstoreOutlined />
          </template>
          <span>Workspace</span>
        </a-menu-item>

        <a-menu-item key="policies" @click="() => setContent('policies')">
          <template #icon>
            <FileTextOutlined />
          </template>
          <span>Policy Viewing</span>
        </a-menu-item>
        <a-menu-item key="profile" @click="() => setContent('profile')">
          <template #icon>
            <UserOutlined />
          </template>
          <span>Personal Profile</span>
        </a-menu-item>
        <a-menu-item key="seek-help" @click="() => setContent('seek-help')">
          <template #icon>
            <QuestionCircleOutlined />
          </template>
          <span>Seek Help</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header class="dashboard-header">
        <menu-unfold-outlined v-if="collapsed" class="trigger" @click="() => (collapsed = !collapsed)" />
        <menu-fold-outlined v-else class="trigger" @click="() => (collapsed = !collapsed)" />
        <div class="header-right">
          <a-dropdown>
            <a class="user-dropdown" @click.prevent>
              <a-avatar><template #icon>
                  <UserOutlined />
                </template></a-avatar>
              <span class="username">{{ username }}</span>
            </a>
            <template #overlay>
              <a-menu>
                <a-menu-item key="profile" @click="() => setContent('profile')">
                  <user-outlined /> Personal Profile
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item key="logout" @click="handleLogout">
                  <logout-outlined /> Logout
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
      </a-layout-header>
      <a-layout-content class="dashboard-content">
        <div class="content-wrapper">
          <div v-if="contentKey === 'overview'">
            <h2>User Dashboard</h2>
            <p>Welcome to your workspace!</p>
            <div class="dashboard-cards">
              <div class="card" @click="() => setContent('workspace')">
                <AppstoreOutlined class="card-icon" />
                <span>Workspace</span>
              </div>
              <div class="card" @click="() => setContent('policies')">
                <FileTextOutlined class="card-icon" />
                <span>Policy Viewing</span>
              </div>
              <div class="card" @click="() => setContent('profile')">
                <UserOutlined class="card-icon" />
                <span>Personal Profile</span>
              </div>
              <div class="card" @click="() => setContent('seek-help')">
                <QuestionCircleOutlined class="card-icon" />
                <span>Seek Help</span>
              </div>
            </div>
          </div>
          <div v-else-if="contentKey === 'workspace'">
            <Workspace />
          </div>
          <div v-else-if="contentKey === 'profile'" class="profile-container">
            <UserProfileCard :userInfo="userInfo" :loading="loading" @edit-field="showEditFieldModal"
              :getRoleName="getRoleName" :getRoleColor="getRoleColor" :formatDateTime="formatDateTime" />
          </div>
          <div v-else-if="contentKey === 'policies'">
            <PolicyViewing />
          </div>
          <div v-else-if="contentKey === 'seek-help'">
            <SeekHelp />
          </div>
        </div>
        <!-- Edit Field Modal -->
        <a-modal :open="editFieldModalVisible" @update:open="val => editFieldModalVisible = val"
          :title="editField === 'username' ? 'Edit Username' : 'Edit Email'" :confirmLoading="editFieldLoading"
          @ok="handleEditFieldOk" @cancel="() => (editFieldModalVisible = false)" destroyOnClose class="profile-modal">
          <a-form :model="editFieldForm" layout="vertical">
            <a-form-item :label="editField === 'username' ? 'Username' : 'Email'">
              <a-input v-if="editField === 'username'" :value="editFieldForm.username"
                @update:value="val => editFieldForm.username = val" placeholder="Enter new username" />
              <a-input v-else :value="editFieldForm.email" @update:value="val => editFieldForm.email = val"
                placeholder="Enter new email" />
            </a-form-item>
          </a-form>
        </a-modal>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup>
import { ref, computed, onMounted, reactive, h, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  UserOutlined, AppstoreAddOutlined, DatabaseOutlined, CheckCircleOutlined,
  FileTextOutlined, BookOutlined, IdcardOutlined, MenuUnfoldOutlined, MenuFoldOutlined, LogoutOutlined, QuestionCircleOutlined, UploadOutlined, EditOutlined, AppstoreOutlined
} from '@ant-design/icons-vue'
import { message, Descriptions as aDescriptions, DescriptionsItem as aDescriptionsItem } from 'ant-design-vue'
import { usersApi, policiesApi } from '../../services/api'
import UserProfileCard from './UserProfileCard.vue'
import CourseManagement from '../management/CourseManagement.vue'
import ServiceConfiguration from '../management/ServiceConfiguration.vue'
import PolicyViewing from '../workspace/PolicyViewing.vue'
import ThesisService from '../workspace/ThesisService.vue'
import StudentServices from '../workspace/StudentServices.vue'
import SeekHelp from '../workspace/SeekHelp.vue'
import Workspace from '../workspace/Workspace.vue'

const router = useRouter()
const collapsed = ref(false)
const contentKey = ref('overview')
const selectedKeys = computed(() => [contentKey.value])
const username = ref('Data User')

const userInfo = ref({})
const loading = ref(false)



const policies = ref([])
const policiesLoading = ref(false)
const policyDetail = ref(null)
const policyDetailVisible = ref(false)

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

const setContent = (key) => {
  contentKey.value = key
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  message.success('Logged out successfully')
  router.push('/login')
}


// 获取政策列表
const fetchPolicies = async () => {
  policiesLoading.value = true
  try {
    const res = await policiesApi.getPolicies()
    policies.value = Array.isArray(res.data) ? res.data : (res.data.items || [])
  } catch (e) {
    message.error('Failed to get policy list')
  } finally {
    policiesLoading.value = false
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
      console.log('Username:', editFieldForm.username)
      message.success('Username updated successfully')
    } else {
      await usersApi.updateCurrentUser({ email: editFieldForm.email })
      localStorage.setItem('email', editFieldForm.email)
      console.log('Email:', editFieldForm.email)
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
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
    return
  }
  username.value = localStorage.getItem('username') || 'Data User'
  fetchUserInfo()
  fetchPolicies()
})
</script>

<style scoped>
.dashboard-layout {
  width: 100%;
  height: 100vh;
  min-height: 100vh;
  display: flex;
  background: #f5f6fa;
  min-width: 0;
  overflow-x: hidden;
}

.dashboard-sider {
  width: 220px !important;
  min-width: 220px !important;
  max-width: 220px !important;
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.15);
  z-index: 10;
}

.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  margin: 0;
  overflow: hidden;
}

.logo img {
  height: 32px;
  margin-right: 8px;
}

.logo span {
  color: white;
  font-size: 18px;
  font-weight: 600;
  white-space: nowrap;
}

.dashboard-header {
  background: #fff;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  z-index: 9;
  min-height: 64px;
}

.trigger {
  font-size: 18px;
  cursor: pointer;
  transition: color 0.3s;
}

.trigger:hover {
  color: #1890ff;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.username {
  margin-left: 8px;
}

.dashboard-content {
  flex: 1;
  min-width: 0;
  min-height: calc(100vh - 64px);
  background: #fff;
  padding: 32px 32px 24px 32px;
  margin: 0;
  overflow: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
}

.content-wrapper {
  flex: 1;
  padding: 0;
  background: #fff;
  min-height: 100%;
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow-x: hidden;
}

@media (max-width: 900px) {
  .dashboard-content {
    padding: 16px 4px 8px 4px;
  }

  .dashboard-sider {
    width: 60px !important;
    min-width: 60px !important;
    max-width: 60px !important;
  }

  .logo span {
    display: none;
}
}

.gpa-result {
  margin-top: 24px;
  padding: 16px;
  background: #fafafa;
  border-radius: 4px;
}

.profile-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px;
}

.profile-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.profile-card :deep(.ant-card-head) {
  border-bottom: 1px solid #f0f0f0;
  padding: 16px 24px;
}

.profile-card :deep(.ant-card-head-title) {
  font-size: 18px;
  font-weight: 600;
  color: #1f1f1f;
}

.edit-button {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 36px;
  padding: 0 16px;
  border-radius: 6px;
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

.profile-modal :deep(.ant-modal-content) {
  border-radius: 8px;
}

.profile-modal :deep(.ant-modal-header) {
  border-radius: 8px 8px 0 0;
  padding: 16px 24px;
}

.profile-modal :deep(.ant-modal-title) {
  font-size: 16px;
  font-weight: 600;
}

.profile-input {
  border-radius: 6px;
}

.profile-input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 16px;
  }

  .profile-descriptions :deep(.ant-descriptions-item) {
    padding: 12px 16px !important;
  }
}

.inline-edit-btn {
  margin-left: 8px;
  padding: 0 4px;
  font-size: 13px;
  vertical-align: middle;
}

.dashboard-cards {
  display: flex;
  gap: 24px;
  margin-top: 32px;
}

.card {
  background: #f6f8fa;
  border-radius: 8px;
  padding: 32px;
  min-width: 180px;
  text-align: center;
  box-shadow: 0 2px 8px #eee;
  font-size: 18px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: #fff;
}

.card-icon {
  font-size: 32px;
  color: #1890ff;
}

.card span {
  color: #333;
}
</style> 