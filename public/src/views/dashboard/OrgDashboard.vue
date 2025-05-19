<template>
  <a-layout class="dashboard-layout">
    <a-layout-sider
      :collapsed="collapsed"
      :trigger="null"
      collapsible
      class="dashboard-sider"
    >
      <div class="logo">
        <img src="/vite.svg" alt="E-DBA Logo" />
        <span v-if="!collapsed">O-Convener</span>
      </div>
      <a-menu :selectedKeys="selectedKeys" theme="dark" mode="inline">
        <a-menu-item key="overview" @click="() => setContent('overview')">
          <template #icon><UserOutlined /></template>
          <span>Dashboard</span>
        </a-menu-item>

        <a-menu-item key="workspace" @click="() => setContent('workspace')">
          <template #icon><AppstoreOutlined /></template>
          <span>Workspace</span>
        </a-menu-item>

        <a-menu-item key="bank-account" @click="() => setContent('bank-account')">
          <template #icon><BankOutlined /></template>
          <span>Bank Account Information</span>
        </a-menu-item>
        <a-menu-item key="members" @click="() => setContent('members')">
          <template #icon><UserOutlined /></template>
          <span>Member Management</span>
        </a-menu-item>
        <a-menu-item key="activity-log" @click="() => setContent('activity-log')">
          <template #icon><HistoryOutlined /></template>
          <span>Activity Log</span>
        </a-menu-item>
        <a-menu-item key="services" @click="() => setContent('services')">
          <template #icon><AppstoreAddOutlined /></template>
          <span>Service Management</span>
        </a-menu-item>
        <a-menu-item key="profile" @click="() => setContent('profile')">
          <user-outlined /> Personal Profile
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header class="dashboard-header">
        <menu-unfold-outlined
          v-if="collapsed"
          class="trigger"
          @click="() => (collapsed = !collapsed)"
        />
        <menu-fold-outlined
          v-else
          class="trigger"
          @click="() => (collapsed = !collapsed)"
        />
        <div class="header-right">
          <a-dropdown>
            <a class="user-dropdown" @click.prevent>
              <a-avatar><template #icon><UserOutlined /></template></a-avatar>
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
            <h2>Organization Dashboard</h2>
            <p>Welcome to the organization workspace!</p>
            <div class="dashboard-cards">
              <div class="card" @click="() => setContent('workspace')">
                <AppstoreOutlined class="card-icon" />
                <span>Workspace</span>
              </div>
              <div class="card" @click="() => setContent('profile')">
                <UserOutlined class="card-icon" />
                <span>Personal Profile</span>
              </div>
              <div class="card" @click="() => setContent('bank-account')">
                <BankOutlined class="card-icon" />
                <span>Bank Account Information</span>
              </div>
              <div class="card" @click="() => setContent('members')">
                <UserOutlined class="card-icon" />
                <span>Member Management</span>
              </div>
              <div class="card" @click="() => setContent('activity-log')">
                <HistoryOutlined class="card-icon" />
                <span>Activity Log</span>
              </div>
              <div class="card" @click="() => setContent('services')">
                <AppstoreAddOutlined class="card-icon" />
                <span>Service Management</span>
              </div>
            </div>
          </div>
          <div v-else-if="contentKey === 'profile'">
            <UserProfileCard />
          </div>
          <div v-else-if="contentKey === 'workspace'">
            <Workspace />
          </div>
          <div v-else-if="contentKey === 'bank-account'">
            <BankAccount />
          </div>
          <div v-else-if="contentKey === 'members'">
            <Members />
          </div>
          <div v-else-if="contentKey === 'activity-log'">
            <ActivityLog />
          </div>
          <div v-else-if="contentKey === 'services'">
            <ServicesManagement />
          </div>
          <div v-else>
            <h2>Organization Dashboard</h2>
            <p>Welcome to the organization workspace!</p>
          </div>
        </div>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import BankAccount from '../workspace/BankAccount.vue'
import Members from '../management/UserManagement.vue'
import ActivityLog from '../workspace/ActivityLog.vue'
import ServicesManagement from '../workspace/ServicesManagement.vue'
import UserProfileCard from '../dashboard/UserProfileCard.vue'
import Workspace from '../workspace/Workspace.vue'
import {
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  UserOutlined,
  LogoutOutlined,
  BankOutlined,
  HistoryOutlined,
  AppstoreAddOutlined,
  AppstoreOutlined
} from '@ant-design/icons-vue'

const router = useRouter()
const collapsed = ref(false)
const username = ref('Organization Convener')
const contentKey = ref('overview')

const selectedKeys = computed(() => [contentKey.value])

const setContent = (key) => {
  contentKey.value = key
}

onMounted(() => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
    return
  }
  username.value = localStorage.getItem('username') || 'Organization Convener'
})

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  message.success('Logged out successfully')
  router.push('/login')
}
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
  .logo span { display: none; }
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
