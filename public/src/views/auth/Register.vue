<template>
  <div class="register-container">
    <a-card class="register-card" title="User Registration" :bordered="false">
      <div class="logo-container">
        <img src="/vite.svg" alt="E-DBA Logo" class="logo" />
      </div>
      <a-form
        :model="formState"
        name="register"
        @finish="onFinish"
        @finishFailed="onFinishFailed"
        autocomplete="off"
        layout="vertical"
      >
        <a-form-item
          label="Email"
          name="email"
          :rules="[{ required: true, type: 'email', message: 'Please enter a valid email address!' }]"
        >
          <a-input v-model:value="formState.email" size="large" placeholder="Please enter your email">
            <template #prefix>
              <MailOutlined />
            </template>
          </a-input>
        </a-form-item>

        <a-form-item
          label="Username"
          name="username"
          :rules="[{ required: true, message: 'Please enter a username!' }]"
        >
          <a-input v-model:value="formState.username" size="large" placeholder="Please enter a username">
            <template #prefix>
              <UserOutlined />
            </template>
          </a-input>
        </a-form-item>

        <a-form-item
          label="Password"
          name="password"
          :rules="[
            { required: true, message: 'Please enter a password!' },
            { min: 8, message: 'Password must be at least 8 characters!' }
          ]"
        >
          <a-input-password v-model:value="formState.password" size="large" placeholder="Please enter a password">
            <template #prefix>
              <LockOutlined />
            </template>
          </a-input-password>
        </a-form-item>

        <a-form-item>
          <a-button type="primary" html-type="submit" size="large" block :loading="loading">
            Register
          </a-button>
        </a-form-item>

        <div class="register-actions">
          <a-button type="link" @click="goToLogin">Already have an account? Login</a-button>
        </div>
      </a-form>
    </a-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { MailOutlined, UserOutlined, LockOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'
import { authApi } from '../../services/api'

const router = useRouter()
const loading = ref(false)

const formState = reactive({
  email: '',
  username: '',
  password: ''
})

const onFinish = async (values) => {
  loading.value = true
  try {
    const response = await authApi.register(values.email, values.username, values.password)
    message.success('Registration successful')
    router.push('/login')
  } catch (error) {
    console.error('Registration failed:', error)
    if (error.response) {
      message.error(error.response.data.detail || 'Registration failed, please check your input')
    } else {
      message.error('Registration failed, please try again later')
    }
  } finally {
    loading.value = false
  }
}

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo)
  message.error('Please fill in all required fields')
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}

.register-card {
  width: 400px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

.logo-container {
  text-align: center;
  margin-bottom: 24px;
}

.logo {
  height: 64px;
}

.register-actions {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>