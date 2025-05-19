<template>
  <div class="login-bg-pro">

    <div class="login-container-pro">
      <div class="login-card-pro">
        <div class="logo-container-pro">
          <img src="/vite.svg" alt="E-DBA Logo" class="logo-pro" />
          <div class="brand-slogan">Education Data Bay Area</div>
        </div>
        <a-tabs v-model="loginType">
          <a-tab-pane key="password" tab="Password Login">
            <a-form
              :model="formState"
              name="login"
              @finish="onFinish"
              @finishFailed="onFinishFailed"
              autocomplete="off"
              layout="vertical"
            >
              <a-form-item
                label="Email"
                name="username"
                :rules="[{ required: true, message: 'Please enter your username or email!' }]"
                class="form-item-pro"
              >
                <a-input v-model="formState.username" size="large" placeholder="Email" class="input-pro" @input="e => { formState.username = e.target.value; console.log('username:', formState.username) }">
                  <template #prefix>
                    <UserOutlined />
                  </template>
                </a-input>
              </a-form-item>

              <a-form-item
                label="Password"
                name="password"
                :rules="[{ required: true, message: 'Please enter your password!' }]"
                class="form-item-pro"
              >
                <a-input-password v-model:value="formState.password" size="large" placeholder="password" class="input-pro" @input="e => { formState.password = e.target.value; console.log('password:', formState.password) }">
                  <template #prefix>
                    <LockOutlined />
                  </template>
                </a-input-password>
              </a-form-item>

              <a-form-item>
                <a-button type="primary" html-type="submit" size="large" block :loading="loading" class="login-btn-pro">
                  Login
                </a-button>
              </a-form-item>

              <div style="text-align: center; margin-bottom: 18px;">
                <a-button type="link" @click="forgotPassword">Forgot Password?</a-button>
              </div>

              <a-divider>Or</a-divider>

              <a-button type="default" size="large" block @click="goToRegisterOrganization" class="org-btn-pro">
                Register Organization Account
              </a-button>
            </a-form>
          </a-tab-pane>
          <a-tab-pane key="emailCode" tab="Email Code Login">
            <a-form :model="emailCodeForm" @finish="onEmailCodeLogin" layout="vertical">
              <a-form-item label="Email" name="email" :rules="[{ required: true, message: 'Please enter your email!' }]">
                <a-input v-model:value="emailCodeForm.email" size="large" placeholder="Email" class="input-pro" />
              </a-form-item>
              <a-form-item label="Code" name="code" :rules="[{ required: true, message: 'Please enter the code!' }]">
                <div style="display: flex; gap: 8px;">
                  <a-input v-model:value="emailCodeForm.code" size="large" placeholder="Code" style="flex: 1;" />
                  <a-button @click="sendEmailCode" :disabled="countdown > 0" style="min-width: 110px;">
                    {{ countdown > 0 ? `${countdown}s` : 'Send Code' }}
                  </a-button>
                </div>
              </a-form-item>
              <a-form-item>
                <a-button type="primary" html-type="submit" size="large" block :loading="loading" class="login-btn-pro">
                  Login
                </a-button>
              </a-form-item>
            </a-form>
          </a-tab-pane>
        </a-tabs>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'
import { authApi, usersApi } from '../../services/api'

const router = useRouter()
const loading = ref(false)

const loginType = ref('password')
const formState = reactive({
  username: '',
  password: ''
})
const emailCodeForm = reactive({
  email: '',
  code: ''
})
const countdown = ref(0)
let timer = null

const sendEmailCode = async () => {
  console.log('sendEmailCode called, email:', emailCodeForm.email)
  if (!emailCodeForm.email) {
    message.error('Please enter your email!')
    return
  }
  try {
    await authApi.sendEmailCode(emailCodeForm.email)
    message.success('Code sent')
    countdown.value = 60
    timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) clearInterval(timer)
    }, 1000)
  } catch (e) {
    console.error('sendEmailCode error:', e)
    message.error(e.response?.data?.detail || 'Failed to send code')
  }
}

const onEmailCodeLogin = async () => {
  console.log('onEmailCodeLogin called, form:', JSON.stringify(emailCodeForm))
  loading.value = true
  try {
    const response = await authApi.loginEmailCode(emailCodeForm.email, emailCodeForm.code)
    console.log('loginEmailCode response:', response)
    const { access_token, token_type } = response.data
    localStorage.setItem('token', access_token)
    localStorage.setItem('token_type', token_type)
    const userInfo = await usersApi.getCurrentUser(access_token)
    console.log('getCurrentUser response:', userInfo)
    const role = userInfo.data.role
    localStorage.setItem('role', role)
    localStorage.setItem('username', userInfo.data.username)
    localStorage.setItem('organization_id', userInfo.data.organization_id)
    localStorage.setItem('permission_level', userInfo.data.permission_level)
    if (role === 'T_ADMIN') {
      router.push('/admin')
    } else if (role === 'E_ADMIN') {
      router.push('/e-admin')
    } else if (role === 'SENIOR_E_ADMIN') {
      router.push('/senior-e-admin')
    } else if (role === 'O_CONVENER') {
      router.push('/o-convener')
    } else {
      router.push('/user')
    }
    message.success('Login successful')
  } catch (error) {
    console.error('loginEmailCode error:', error)
    message.error(error.response?.data?.detail || 'Login failed, please check your code and email')
  } finally {
    loading.value = false
  }
}

const onFinish = async (values) => {
  loading.value = true
  try {
    const response = await authApi.login(values.username, values.password)
    const { access_token, token_type } = response.data
    
    // Save token to local storage
    localStorage.setItem('token', access_token)
    localStorage.setItem('token_type', token_type)
    
    const userInfo = await usersApi.getCurrentUser(access_token)
    console.log(userInfo)
    const role = userInfo.data.role
    localStorage.setItem('role', role)
    localStorage.setItem('username', userInfo.data.username)
    localStorage.setItem('organization_id', userInfo.data.organization_id)
    localStorage.setItem('permission_level', userInfo.data.permission_level)
    if (role === 'T_ADMIN') {
      router.push('/admin')
    } else if (role === 'E_ADMIN') {
      router.push('/e-admin')
    } else if (role === 'SENIOR_E_ADMIN') {
      router.push('/senior-e-admin')
    } else if (role === 'O_CONVENER') {
      router.push('/o-convener')
    } else {
      router.push('/user')
    }
    message.success('Login successful')
  } catch (error) {
    console.error('Login failed:', error)
    if (error.response) {
      message.error(error.response.data.detail || 'Login failed, please check your username and password')
    } else {
      message.error('Login failed, please try again later')
    }
  } finally {
    loading.value = false
  }
}

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo)
  message.error('Please fill in all required fields')
}

const forgotPassword = () => {
  message.info('Password reset feature coming soon')
}

const goToRegister = () => {
  router.push('/register')
}

const goToRegisterOrganization = () => {
  router.push('/register-organization')
}
</script>

<style>
html, body {
  min-height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow-x: hidden;
}
</style>

<style scoped>
.login-bg-pro {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  overflow-x: hidden;
}
.login-illustration {
  width: 100%;
  min-height: 180px;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
  display: flex;
  justify-content: center;
  pointer-events: none;
}
.login-illustration img {
  width: 100%;
  max-width: 1200px;
  opacity: 0.7;
  user-select: none;
}
.login-container-pro {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}
.login-card-pro {
  width: 420px;
  border-radius: 20px;
  background: rgba(255,255,255,0.96);
  color: #222;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.22), 0 0 0 2px #667eea22;
  backdrop-filter: blur(8px) saturate(180%);
  border: 1.5px solid #e0eafc;
  padding: 36px 32px 28px 32px;
  position: relative;
  animation: fadeInUp 0.8s cubic-bezier(.23,1.01,.32,1) 0.1s both;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: none; }
}
.logo-container-pro {
  text-align: center;
  margin-bottom: 18px;
}
.logo-pro {
  height: 72px;
  margin-bottom: 8px;
  filter: drop-shadow(0 2px 8px rgba(33,147,176,0.15));
  animation: logoPop 1.2s cubic-bezier(.23,1.01,.32,1);
}
@keyframes logoPop {
  0% { transform: scale(0.7); opacity: 0; }
  80% { transform: scale(1.1); opacity: 1; }
  100% { transform: scale(1); }
}
.brand-slogan {
  font-size: 1.1rem;
  color: #667eea;
  font-weight: 600;
  letter-spacing: 1px;
  margin-bottom: 8px;
  text-shadow: 0 2px 8px #667eea22;
}
.form-item-pro {
  position: relative;
  margin-bottom: 28px;
}
.input-pro .ant-input,
.input-pro .ant-input-affix-wrapper input.ant-input {
  background: #fff !important;
  color: #222 !important;
  box-shadow: none !important;
  opacity: 1 !important;
}

/* 彻底覆盖 Chrome/Safari 的自动填充灰色 */
.input-pro .ant-input:-webkit-autofill,
.input-pro .ant-input-affix-wrapper input.ant-input:-webkit-autofill {
  -webkit-box-shadow: 0 0 0 1000px #fff inset !important;
  -webkit-text-fill-color: #222 !important;
  box-shadow: 0 0 0 1000px #fff inset !important;
  color: #222 !important;
  transition: background-color 5000s ease-in-out 0s;
}

/* Firefox 自动填充 */
.input-pro .ant-input:-moz-autofill,
.input-pro .ant-input-affix-wrapper input.ant-input:-moz-autofill {
  box-shadow: 0 0 0 1000px #fff inset !important;
  color: #222 !important;
}

/* Edge/IE 自动填充 */
.input-pro .ant-input:-ms-input-placeholder,
.input-pro .ant-input-affix-wrapper input.ant-input:-ms-input-placeholder {
  color: #222 !important;
  background: #fff !important;
}
.input-pro .ant-input:focus, .input-pro .ant-input-password:focus {
  border: 1.5px solid #667eea;
  box-shadow: 0 0 0 2px #667eea33;
}
.float-label {
  position: absolute;
  left: 38px;
  top: 12px;
  font-size: 1rem;
  color: #888;
  pointer-events: none;
  transition: 0.2s;
  opacity: 0.7;
}
.input-pro .ant-input:focus + .float-label,
.input-pro .ant-input:not(:placeholder-shown) + .float-label,
.input-pro .ant-input-password:focus + .float-label,
.input-pro .ant-input-password:not(:placeholder-shown) + .float-label {
  top: -12px;
  left: 32px;
  font-size: 0.85rem;
  color: #667eea;
  opacity: 1;
  background: #fff8;
  padding: 0 4px;
  border-radius: 6px;
}
.login-btn-pro {
  border-radius: 10px;
  background: linear-gradient(90deg, #667eea 0%, #43cea2 100%);
  border: none;
  color: #fff;
  font-weight: 600;
  font-size: 1.15rem;
  box-shadow: 0 2px 8px #667eea33;
  transition: background 0.3s, box-shadow 0.2s;
  margin-bottom: 8px;
}
.login-btn-pro:hover {
  background: linear-gradient(90deg, #43cea2 0%, #667eea 100%);
  color: #fff;
  box-shadow: 0 4px 16px #667eea55;
}
.org-btn-pro {
  border-radius: 10px;
  margin-top: 8px;
  font-size: 1.05rem;
  background: #f6f8fc;
  border: 1.5px solid #e0eafc;
  color: #667eea;
  font-weight: 500;
  transition: background 0.2s, border 0.2s;
}
.org-btn-pro:hover {
  background: #e0eafc;
  border: 1.5px solid #667eea;
  color: #667eea;
}
@media (max-width: 600px) {
  .login-card-pro {
    width: 98%;
    min-width: 0;
    padding: 12px 0;
  }
  .logo-pro {
    height: 48px;
  }
  .login-illustration {
    min-height: 80px;
  }
}
</style>