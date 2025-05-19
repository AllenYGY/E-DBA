<template>
  <a-card title="Student Services" :bordered="false">
    <a-alert
      v-if="!studentServices.length"
      type="warning"
      message="No student query service found"
      description="Please contact the administrator to configure the student query service"
      show-icon
      style="margin-bottom: 16px"
    />
    <template v-else>
      <a-tabs v-model:value="studentQueryTab">
        <a-tab-pane key="verify" tab="Identity Verification">
          <a-form layout="vertical">
            <a-form-item label="Name" required>
              <a-input v-model:value="verifyForm.name" placeholder="Please enter the student name" />
            </a-form-item>
            <a-form-item label="Student ID" required> 
              <a-input v-model:value="verifyForm.id" placeholder="Please enter the student ID" />
            </a-form-item>
            <a-form-item label="Photo">
              <a-upload
                :file-list="verifyForm.photo ? [verifyForm.photo] : []"
                :before-upload="handlePhotoUpload"
                :max-count="1"
                accept="image/*"
              >
                <a-button>
                  <upload-outlined /> Upload Photo
                </a-button>
              </a-upload>
            </a-form-item>
            <a-form-item>
              <a-button 
                type="primary" 
                @click="handleVerifyStudent"
                :loading="verifyLoading"
                :disabled="!selectedVerifyService"
              >
                Verify Identity
              </a-button>
            </a-form-item>
          </a-form>
        </a-tab-pane>

        <a-tab-pane key="gpa" tab="GPA Query">
          <a-form layout="vertical">
            <a-form-item label="Name" required>
              <a-input v-model:value="gpaForm.name" placeholder="Please enter the student name" />
            </a-form-item>
            <a-form-item label="Student ID" required>
              <a-input v-model:value="gpaForm.id" placeholder="Please enter the student ID" />
            </a-form-item>
            <a-form-item>
              <a-button 
                type="primary" 
                @click="handleQueryGPA"
                :loading="gpaLoading"
                :disabled="!selectedGPAService"
              >
                Query GPA
              </a-button>
            </a-form-item>
          </a-form>

          <a-divider />

          <div v-if="gpaResult" class="gpa-result">
            <a-descriptions title="Student GPA Information" bordered>
              <a-descriptions-item label="Name">{{ gpaResult.name }}</a-descriptions-item>
              <a-descriptions-item label="Enroll Year">{{ gpaResult.enroll_year }}</a-descriptions-item>
              <a-descriptions-item label="Graduation Year">{{ gpaResult.graduation_year }}</a-descriptions-item>
              <a-descriptions-item label="GPA">{{ gpaResult.gpa }}</a-descriptions-item>
            </a-descriptions>
          </div>
        </a-tab-pane>
      </a-tabs>
    </template>
  </a-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { servicesApi } from '../../services/api'
import axios from 'axios'
import { UploadOutlined } from '@ant-design/icons-vue'

const permissionLevel = Number(localStorage.getItem('permission_level'))
const organizationId = Number(localStorage.getItem('organization_id'))
const activeOrganizationId = Number(localStorage.getItem('active_organization_id'))

const studentServices = ref([])
const selectedVerifyService = ref(null)
const selectedGPAService = ref(null)
const studentQueryTab = ref('verify')
const verifyLoading = ref(false)
const gpaLoading = ref(false)
const gpaResult = ref(null)
const verifyForm = reactive({ name: '', id: '', photo: null })
const gpaForm = reactive({ name: '', id: '' })

const fetchStudentServices = async () => {
  try {
    const res = await servicesApi.getOrganizationServices({ organization_id: activeOrganizationId })
    studentServices.value = res.data.filter(service => (service.service_type === 'student_verification' || service.service_type === 'student_gpa') && service.is_active)
    const verifyServices = studentServices.value.filter(s => s.service_type === 'student_verification')
    const gpaServices = studentServices.value.filter(s => s.service_type === 'student_gpa')
    if (verifyServices.length > 0) { selectedVerifyService.value = verifyServices[0].id }
    if (gpaServices.length > 0) { selectedGPAService.value = gpaServices[0].id }
  } catch (e) { message.error('Failed to get service configuration') }
}

const handlePhotoUpload = (file) => { verifyForm.photo = file; return false }

const handleVerifyStudent = async () => {
  if (!selectedVerifyService.value) { message.error('Please select an identity verification service first'); return }
  if (!verifyForm.name || !verifyForm.id) { message.error('Please fill in the complete information'); return }
  const verifyService = studentServices.value.find(s => s.id === selectedVerifyService.value)
  if (!verifyService) { message.error('Selected verification service not found'); return }
  console.log('Verify Service Configuration:', { service_id: verifyService.id, service_name: verifyService.name, base_url: verifyService.base_url, api_path: verifyService.api_path, full_url: verifyService.base_url + (verifyService.api_path.startsWith('/') ? '' : '/') + verifyService.api_path })
  if (!verifyService.base_url || !verifyService.api_path) { console.error('Service configuration is incomplete:', { base_url: verifyService.base_url, api_path: verifyService.api_path }); message.error('Service configuration is incomplete, please check the base URL and API path'); return }
  try {
    const baseUrl = (verifyService.base_url.endsWith('/') ? verifyService.base_url.slice(0, -1) : verifyService.base_url)
    const apiPath = (verifyService.api_path.startsWith('/') ? verifyService.api_path : ('/' + verifyService.api_path))
    const fullUrl = `${baseUrl}${apiPath}`
    new URL(fullUrl)
    console.log('Valid URL constructed:', fullUrl)
    verifyLoading.value = true
    try {
      const formData = new FormData()
      formData.append('name', verifyForm.name)
      formData.append('id', verifyForm.id)
      if (verifyForm.photo) { formData.append('photo', verifyForm.photo) }
      console.log('Sending verification request to:', fullUrl, 'Request data:', { name: verifyForm.name, id: verifyForm.id, hasPhoto: !!verifyForm.photo })
      const response = await axios.post(fullUrl, formData, { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}`, 'Content-Type': 'multipart/form-data' } })
      console.log('Verification response:', response.data)
      if (verifyService.output_format) { const result = {}; for (const [key, type] of Object.entries(verifyService.output_format)) { if (response.data[key] !== undefined) { result[key] = response.data[key] } }; message.info(JSON.stringify(result, null, 2)) } else { message.info(JSON.stringify(response.data, null, 2)) }
    } catch (e) { console.error('Error verifying student:', e); if (e.response) { console.error('Error response data:', e.response.data); message.error(e.response.data.detail || e.response.data.message || '身份验证失败') } else if (e.request) { message.error('Failed to connect to server') } else { message.error('Identity verification request failed') } } finally { verifyLoading.value = false } } catch (urlError) { console.error('Invalid URL construction:', { base_url: verifyService.base_url, api_path: verifyService.api_path, error: urlError.message }); message.error('Service URL configuration is invalid, please check the format of the base URL and API path'); return } }

const handleQueryGPA = async () => {
  if (!selectedGPAService.value) { message.error('Please select a GPA query service first'); return }
  if (!gpaForm.name || !gpaForm.id) { message.error('Please fill in the complete information'); return }
  const gpaService = studentServices.value.find(s => s.id === selectedGPAService.value)
  if (!gpaService) { message.error('Selected GPA query service not found'); return }
  console.log('Selected GPA Service:', gpaService, 'Service ID:', selectedGPAService.value, 'All Student Services:', studentServices.value)
  if (!gpaService.base_url || !gpaService.api_path) { console.error('Service configuration is incomplete:', { base_url: gpaService.base_url, api_path: gpaService.api_path }); message.error('Service configuration is incomplete, please check the base URL and API path'); return }
  gpaLoading.value = true
  try { const requestUrl = `${gpaService.base_url}${gpaService.api_path}`; console.log('Request URL:', requestUrl, 'Request Data:', { name: gpaForm.name, id: gpaForm.id }); const response = await axios.post(requestUrl, { name: gpaForm.name, id: gpaForm.id }, { headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('token')}` } }); gpaResult.value = response.data; message.success('GPA query successful') } catch (e) { console.error('Error querying GPA:', e); if (e.response) { if (e.response.data.detail === 'Student not found') { message.warning('Student information not found, please check if the name and ID are correct') } else if (e.response.data.detail) { message.error(e.response.data.detail) } else if (e.response.data.message) { message.error(e.response.data.message) } else { message.error('GPA query failed') } } else if (e.request) { message.error('Failed to connect to server') } else { message.error('GPA query request failed') } } finally { gpaLoading.value = false } }

onMounted(() => { fetchStudentServices() })

</script>

<style scoped>
.gpa-result { margin-top: 24px; padding: 16px; background: #fafafa; border-radius: 4px; }
</style> 