<template>
  <a-layout class="dashboard-layout">
    <a-layout-sider
      v-model:collapsed="collapsed"
      :trigger="null"
      collapsible
      class="dashboard-sider"
    >
      <div class="logo">
        <img src="/vite.svg" alt="E-DBA Logo" />
        <span v-if="!collapsed">E-DBA</span>
      </div>
      <a-menu
        v-model:selectedKeys="selectedKeys"
        theme="dark"
        mode="inline"
      >
        <a-menu-item key="papers" @click="() => router.push('/dashboard/papers')">
          <template #icon><FileOutlined /></template>
          <span>Papers</span>
        </a-menu-item>
        <a-menu-item key="student-verification" @click="() => router.push('/dashboard/student-verification')">
          <template #icon><IdcardOutlined /></template>
          <span>Students</span>
        </a-menu-item>
        <a-menu-item key="gpa-records" @click="() => router.push('/dashboard/gpa-records')">
          <template #icon><ProfileOutlined /></template>
          <span>GPA</span>
        </a-menu-item>
        <a-menu-item key="courses" @click="() => router.push('/dashboard/courses')">
          <template #icon><BookOutlined /></template>
          <span>Courses</span>
        </a-menu-item>
        <a-menu-item key="user-management" @click="() => router.push('/dashboard/user-management')">
          <template #icon><TeamOutlined /></template>
          <span>Users</span>
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
                <a-menu-item key="profile" @click="() => router.push('/dashboard/profile')">
                  <user-outlined />
                  Personal Profile
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item key="logout" @click="handleLogout">
                  <logout-outlined />
                  Logout
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
      </a-layout-header>
      <a-layout-content class="dashboard-content">
        <div class="content-wrapper">
          <router-view />
        </div>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import {
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  UserOutlined,
  LogoutOutlined,
  FileOutlined,
  IdcardOutlined,
  ProfileOutlined,
  BookOutlined,
  TeamOutlined
} from '@ant-design/icons-vue'

const router = useRouter()
const route = useRoute()
const collapsed = ref(false)
const username = ref('用户')

// 根据当前路由设置选中的菜单项
const selectedKeys = computed(() => {
  const path = route.path
  const key = path.split('/').pop()
  return [key]
})

// 模拟获取用户信息
onMounted(() => {
  // 这里应该从API获取用户信息
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
    return
  }
  
  // 模拟用户名，实际应从API获取
  username.value = localStorage.getItem('username') || '用户'
})

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('token_type')
  localStorage.removeItem('username')
  message.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
}

.dashboard-sider {
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
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
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  z-index: 9;
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
  margin: 24px 16px;
  padding: 24px;
  background: #fff;
  min-height: 280px;
  overflow: auto;
}

.content-wrapper {
  padding: 0;
  background: #fff;
  min-height: 100%;
}
</style>