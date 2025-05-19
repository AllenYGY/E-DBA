<template>
  <div class="register-org-container">
    <a-card class="register-org-card" title="Organization Registration" :bordered="false">
      <div class="logo-container">
        <img src="/vite.svg" alt="E-DBA Logo" class="logo" />
      </div>
      <a-steps :current="currentStep" size="small" class="mb-20">
        <a-step title="User Information" />
        <a-step title="Organization Information" />
        <a-step title="Complete" />
      </a-steps>
      
      <a-alert v-if="errorMsg" :message="errorMsg" type="error" show-icon style="margin-bottom: 16px;" />
      
      <div v-if="currentStep === 0">
        <a-form
          :model="userForm"
          name="userForm"
          @finish="onUserFormFinish"
          layout="vertical"
        >
          <a-form-item
            label="Email"
            name="email"
            :rules="[{ required: true, type: 'email', message: 'Please enter a valid email address!' }]"
          >
            <a-input v-model:value="userForm.email" placeholder="Please enter your email">
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
            <a-input v-model:value="userForm.username" placeholder="Please enter a username">
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
            <a-input-password v-model:value="userForm.password" placeholder="Please enter a password">
              <template #prefix>
                <LockOutlined />
              </template>
            </a-input-password>
          </a-form-item>

          <a-form-item>
            <a-button type="primary" html-type="submit" size="large" block :loading="loading">
              Next
            </a-button>
          </a-form-item>
        </a-form>
      </div>

      <div v-if="currentStep === 1">
        <a-form
          :model="orgForm"
          name="orgForm"
          @finish="onOrgFormFinish"
          layout="vertical"
        >
          <a-form-item
            label="Organization Name"
            name="name"
            :rules="[{ required: true, message: 'Please enter the organization name!' }]"
          >
            <a-input v-model:value="orgForm.name" placeholder="Please enter the organization name" />
          </a-form-item>

          <a-form-item
            label="Organization Full Name"
            name="full_name"
            :rules="[{ required: true, message: 'Please enter the organization full name!' }]"
          >
            <a-textarea v-model:value="orgForm.full_name" placeholder="This is an example organization" auto-size />
          </a-form-item>

          <a-form-item
            label="Email Domain"
            name="email_domain"
            :rules="[{ required: true, message: 'Please enter the email domain!' }]"
          >
            <a-input v-model:value="orgForm.email_domain" placeholder="example.com" />
          </a-form-item>

          <a-form-item
            label="Verification Document"
            name="verification_document"
            :rules="[{ required: true, message: 'Please upload the verification document!' }]"
          >
            <a-upload
              :before-upload="beforeUpload"
              :show-upload-list="false"
              accept=".pdf,.jpg,.jpeg,.png,.doc,.docx,.pdf"
            >
              <a-button>Click to Upload</a-button>
            </a-upload>
            <div v-if="orgForm.verification_document_name" style="margin-top: 8px; color: #666;">
              Uploaded: {{ orgForm.verification_document_name }}
              <template v-if="orgForm.verification_document.startsWith('data:image')">
                <div style="margin-top: 8px;"><img :src="orgForm.verification_document" alt="preview" style="max-width: 200px; max-height: 120px; border: 1px solid #eee;" /></div>
              </template>
              <template v-else-if="orgForm.verification_document.startsWith('data:application/pdf')">
                <div style="margin-top: 8px;"><a :href="orgForm.verification_document" target="_blank" download>预览/下载 PDF</a></div>
              </template>
            </div>
          </a-form-item>

          <a-form-item class="form-actions">
            <a-button @click="prevStep" size="large" style="margin-right: 12px;">
              Previous
            </a-button>
            <a-button type="primary" html-type="submit" size="large" :loading="loading">
              Complete Registration
            </a-button>
          </a-form-item>
        </a-form>
      </div>

      <div v-if="currentStep === 2">
        <div class="completion-message">
          <p>Registration Complete! Please login to continue.</p>
          <a-button type="primary" @click="goToLogin">Go to Login</a-button>
        </div>
      </div>
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
const currentStep = ref(0)
const errorMsg = ref('')

const userForm = reactive({
  email: '',
  username: '',
  password: ''
})

const orgForm = reactive({
  name: '',
  full_name: '',
  email_domain: '',
  verification_document: '',
  verification_document_name: '',
  verification_document_file: null,
})

const onUserFormFinish = async (values) => {
  currentStep.value = 1
}

const onOrgFormFinish = async (values) => {
  loading.value = true
  try {
    const formData = new FormData();
    formData.append('username', userForm.username);
    formData.append('email', userForm.email);
    formData.append('password', userForm.password);
    formData.append('name', orgForm.name);
    formData.append('full_name', orgForm.full_name);
    formData.append('email_domain', orgForm.email_domain);
    formData.append('verification_document', orgForm.verification_document_file);
    await authApi.registerOrganizationMultipart(formData);
    message.success('Organization registration successful')
    currentStep.value = 2
  } catch (error) {
    console.error('Registration failed:', error)
    if (error.response) {
      errorMsg.value = error.response.data.detail || 'Registration failed, please check your input'
    } else {
      errorMsg.value = 'Registration failed, please try again later'
    }
    message.error(errorMsg.value)
  } finally {
    loading.value = false
  }
}

const goToLogin = () => {
  router.push('/login')
}

// 文件上传处理
const beforeUpload = (file) => {
  orgForm.verification_document_file = file;
  orgForm.verification_document_name = file.name;
  // 预览
  const reader = new FileReader();
  reader.onload = (e) => {
    orgForm.verification_document = e.target.result;
  };
  reader.readAsDataURL(file);
  return false;
}

const prevStep = () => {
  if (currentStep.value > 0) currentStep.value--
}
</script>

<style scoped>
.register-org-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}

.register-org-card {
  width: 600px;
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

.completion-message {
  text-align: center;
  margin-top: 24px;
}

.form-actions .ant-btn {
  min-width: 120px;
  border-radius: 6px;
}
</style>