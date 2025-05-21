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

        <a-tab-pane key="batch" tab="Batch Processing">
          <a-form layout="vertical">
            <a-form-item label="Operation Type" required>
              <a-radio-group v-model:value="batchForm.operationType">
                <a-radio value="verify">Identity Verification</a-radio>
                <a-radio value="gpa">GPA Query</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item label="Excel File" required>
              <a-upload
                :file-list="batchForm.file ? [batchForm.file] : []"
                :before-upload="handleBatchFileUpload"
                :max-count="1"
                accept=".xlsx,.xls"
              >
                <a-button>
                  <upload-outlined /> Upload Excel File
                </a-button>
              </a-upload>
              <div class="upload-tip">
                <p>Please upload an Excel file with the following columns:</p>
                <ul>
                  <li>Required columns: Name, Student ID</li>
                  <li>For identity verification: Photo (optional, column name should be "Photo")</li>
                </ul>
                <a-button type="link" @click="downloadTemplate">Download Template</a-button>
              </div>
            </a-form-item>
            <a-form-item>
              <a-button 
                type="primary" 
                @click="handleBatchProcess"
                :loading="batchLoading"
                :disabled="!batchForm.file || !batchForm.operationType"
              >
                Start Batch Processing
              </a-button>
            </a-form-item>
          </a-form>

          <a-divider />

          <div v-if="batchResults.length" class="batch-results">
            <a-alert
              :type="batchProcessingStatus.type"
              :message="batchProcessingStatus.message"
              :description="batchProcessingStatus.description"
              show-icon
              style="margin-bottom: 16px"
            />
            <a-table
              :columns="batchResultColumns"
              :data-source="batchResults"
              :pagination="{ pageSize: 10 }"
              :scroll="{ x: true }"
            >
              <template #bodyCell="{ column, record }">
                <template v-if="column.key === 'status'">
                  <a-tag :color="record.status === 'success' ? 'success' : 'error'">
                    {{ record.status === 'success' ? 'Success' : 'Failed' }}
                  </a-tag>
                </template>
                <template v-if="column.key === 'message'">
                  <span :style="{ color: record.status === 'success' ? '#52c41a' : '#ff4d4f' }">
                    {{ record.message }}
                  </span>
                </template>
              </template>
            </a-table>
            <div class="batch-actions" style="margin-top: 16px">
              <a-button type="primary" @click="exportResults">
                Export Results
              </a-button>
            </div>
          </div>
        </a-tab-pane>
      </a-tabs>
    </template>

    <!-- 添加支付确认弹窗 -->
    <a-modal
      :open="showBalanceModal"
      title="Confirm Payment"
      @ok="confirmPayment"
      @cancel="showBalanceModal = false"
    >
      <p>Your current balance: <b>{{ currentBalance }}</b></p>
      <p>Service fee: <b>{{ pendingOperation ? getServiceFee(pendingOperation.type === 'verify' ? 'student_verification' : 'student_gpa') : 0 }}</b></p>
      <p>Are you sure you want to proceed?</p>
    </a-modal>
  </a-card>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { message } from 'ant-design-vue'
import { servicesApi, usersApi, bankApi } from '../../services/api'
import axios from 'axios'
import { UploadOutlined } from '@ant-design/icons-vue'
import * as XLSX from 'xlsx'

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

const batchForm = reactive({
  operationType: 'verify',
  file: null
})

const batchLoading = ref(false)
const batchResults = ref([])
const batchProcessingStatus = reactive({
  type: 'info',
  message: '',
  description: ''
})

const currentBalance = ref(0)
const userId = ref(null)
const showBalanceModal = ref(false)
const pendingOperation = ref(null)

const batchResultColumns = computed(() => {
  const baseColumns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Student ID', dataIndex: 'id', key: 'id' },
    { title: 'Status', dataIndex: 'status', key: 'status' },
    { title: 'Message', dataIndex: 'message', key: 'message' }
  ]
  
  if (batchForm.operationType === 'gpa') {
    return [
      ...baseColumns,
      { title: 'GPA', dataIndex: 'gpa', key: 'gpa' },
      { title: 'Enroll Year', dataIndex: 'enroll_year', key: 'enroll_year' },
      { title: 'Graduation Year', dataIndex: 'graduation_year', key: 'graduation_year' }
    ]
  }
  
  return baseColumns
})

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

const fetchUserBalance = async () => {
  try {
    const res = await usersApi.getCurrentUser()
    currentBalance.value = res.data.balance || 0
    userId.value = res.data.id
  } catch (e) {
    currentBalance.value = 0
    userId.value = null
  }
}

const getServiceFee = (serviceType) => {
  const service = studentServices.value.find(s => s.service_type === serviceType)
  if (service && service.fee_per_use !== undefined && service.fee_unit) {
    return Number(service.fee_per_use)
  }
  return 0
}

const handlePayment = async (operation) => {
  await fetchUserBalance()
  pendingOperation.value = operation
  showBalanceModal.value = true
}

const confirmPayment = async () => {
  showBalanceModal.value = false
  if (!pendingOperation.value) return

  const { type, callback, params } = pendingOperation.value
  const fee = getServiceFee(type === 'verify' ? 'student_verification' : 'student_gpa')

  if (!userId.value || !fee) {
    message.error('User info or service fee error')
    pendingOperation.value = null
    return
  }

  try {
    // 1. 扣除用户余额
    const balanceRes = await usersApi.editBalance(userId.value, -fee)
    // 检查余额是否足够
    if (balanceRes.data.message === "Balance not enough") {
      message.error('Balance not enough')
      pendingOperation.value = null
      return
    }

    // 2. 组织间转账
    await bankApi.transferByOrg({
      from_org_id: organizationId,
      to_org_id: activeOrganizationId,
      amount: fee,
    })

    message.success(`Deducted ${fee} successfully`)
    // 执行原操作
    await callback(...params)
  } catch (e) {
    message.error(e.response?.data?.detail || 'Balance deduction or transfer failed')
  }
  pendingOperation.value = null
}

const handleVerifyStudent = async () => {
  if (!selectedVerifyService.value) { 
    message.error('Please select an identity verification service first')
    return 
  }
  if (!verifyForm.name || !verifyForm.id) { 
    message.error('Please fill in the complete information')
    return 
  }

  const verifyService = studentServices.value.find(s => s.id === selectedVerifyService.value)
  if (!verifyService) { 
    message.error('Selected verification service not found')
    return 
  }

  if (!verifyService.base_url || !verifyService.api_path) { 
    message.error('Service configuration is incomplete, please check the base URL and API path')
    return 
  }

  await handlePayment({
    type: 'verify',
    callback: async () => {
      verifyLoading.value = true
      try {
        const baseUrl = verifyService.base_url.endsWith('/') ? verifyService.base_url.slice(0, -1) : verifyService.base_url
        const apiPath = verifyService.api_path.startsWith('/') ? verifyService.api_path : ('/' + verifyService.api_path)
        const fullUrl = `${baseUrl}${apiPath}`

        const formData = new FormData()
        formData.append('name', verifyForm.name)
        formData.append('id', verifyForm.id)
        if (verifyForm.photo) { 
          formData.append('photo', verifyForm.photo) 
        }

        const response = await axios.post(fullUrl, formData, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'multipart/form-data'
          }
        })

        if (verifyService.output_format) {
          const result = {}
          for (const [key, type] of Object.entries(verifyService.output_format)) {
            if (response.data[key] !== undefined) {
              result[key] = response.data[key]
            }
          }
          message.info(JSON.stringify(result, null, 2))
        } else {
          message.info(JSON.stringify(response.data, null, 2))
        }
      } catch (e) {
        if (e.response) {
          message.error(e.response.data.detail || e.response.data.message || '身份验证失败')
        } else if (e.request) {
          message.error('Failed to connect to server')
        } else {
          message.error('Identity verification request failed')
        }
      } finally {
        verifyLoading.value = false
      }
    },
    params: []
  })
}

const handleQueryGPA = async () => {
  if (!selectedGPAService.value) { 
    message.error('Please select a GPA query service first')
    return 
  }
  if (!gpaForm.name || !gpaForm.id) { 
    message.error('Please fill in the complete information')
    return 
  }

  const gpaService = studentServices.value.find(s => s.id === selectedGPAService.value)
  if (!gpaService) { 
    message.error('Selected GPA query service not found')
    return 
  }

  if (!gpaService.base_url || !gpaService.api_path) { 
    message.error('Service configuration is incomplete, please check the base URL and API path')
    return 
  }

  await handlePayment({
    type: 'gpa',
    callback: async () => {
      gpaLoading.value = true
      try {
        const requestUrl = `${gpaService.base_url}${gpaService.api_path}`
        const response = await axios.post(requestUrl, {
          name: gpaForm.name,
          id: gpaForm.id
        }, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        gpaResult.value = response.data
        message.success('GPA query successful')
      } catch (e) {
        if (e.response) {
          if (e.response.data.detail === 'Student not found') {
            message.warning('Student information not found, please check if the name and ID are correct')
          } else if (e.response.data.detail) {
            message.error(e.response.data.detail)
          } else if (e.response.data.message) {
            message.error(e.response.data.message)
          } else {
            message.error('GPA query failed')
          }
        } else if (e.request) {
          message.error('Failed to connect to server')
        } else {
          message.error('GPA query request failed')
        }
      } finally {
        gpaLoading.value = false
      }
    },
    params: []
  })
}

const handleBatchFileUpload = (file) => {
  const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || 
                  file.type === 'application/vnd.ms-excel'
  if (!isExcel) {
    message.error('You can only upload Excel files!')
    return false
  }
  batchForm.file = file
  return false
}

const downloadTemplate = () => {
  const template = {
    verify: [
      { Name: '', 'Student ID': '', Photo: '' }
    ],
    gpa: [
      { Name: '', 'Student ID': '' }
    ]
  }
  
  const ws = XLSX.utils.json_to_sheet(template[batchForm.operationType])
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Template')
  XLSX.writeFile(wb, `student_${batchForm.operationType}_template.xlsx`)
}

const processBatchVerify = async (students) => {
  const results = []
  const verifyService = studentServices.value.find(s => s.id === selectedVerifyService.value)
  
  for (const student of students) {
    try {
      const formData = new FormData()
      formData.append('name', student.Name)
      formData.append('id', student['Student ID'])
      if (student.Photo) {
        formData.append('photo', student.Photo)
      }
      
      const baseUrl = verifyService.base_url.endsWith('/') ? verifyService.base_url.slice(0, -1) : verifyService.base_url
      const apiPath = verifyService.api_path.startsWith('/') ? verifyService.api_path : ('/' + verifyService.api_path)
      const fullUrl = `${baseUrl}${apiPath}`
      
      const response = await axios.post(fullUrl, formData, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'multipart/form-data'
        }
      })
      
      results.push({
        name: student.Name,
        id: student['Student ID'],
        status: 'success',
        message: 'Verification successful',
        data: response.data
      })
    } catch (error) {
      results.push({
        name: student.Name,
        id: student['Student ID'],
        status: 'error',
        message: error.response?.data?.detail || error.response?.data?.message || 'Verification failed',
        data: null
      })
    }
  }
  
  return results
}

const processBatchGPA = async (students) => {
  const results = []
  const gpaService = studentServices.value.find(s => s.id === selectedGPAService.value)
  
  for (const student of students) {
    try {
      const baseUrl = gpaService.base_url.endsWith('/') ? gpaService.base_url.slice(0, -1) : gpaService.base_url
      const apiPath = gpaService.api_path.startsWith('/') ? gpaService.api_path : ('/' + gpaService.api_path)
      const fullUrl = `${baseUrl}${apiPath}`
      
      const response = await axios.post(fullUrl, {
        name: student.Name,
        id: student['Student ID']
      }, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      results.push({
        name: student.Name,
        id: student['Student ID'],
        status: 'success',
        message: 'GPA query successful',
        gpa: response.data.gpa,
        enroll_year: response.data.enroll_year,
        graduation_year: response.data.graduation_year,
        data: response.data
      })
    } catch (error) {
      results.push({
        name: student.Name,
        id: student['Student ID'],
        status: 'error',
        message: error.response?.data?.detail || error.response?.data?.message || 'GPA query failed',
        data: null
      })
    }
  }
  
  return results
}

const handleBatchProcess = async () => {
  if (!batchForm.file || !batchForm.operationType) {
    message.error('Please select operation type and upload Excel file')
    return
  }
  
  const service = batchForm.operationType === 'verify' ? selectedVerifyService.value : selectedGPAService.value
  if (!service) {
    message.error(`Please select a ${batchForm.operationType} service first`)
    return
  }

  // 先读取文件获取学生数量
  try {
    const reader = new FileReader()
    reader.onload = async (e) => {
      try {
        const data = new Uint8Array(e.target.result)
        const workbook = XLSX.read(data, { type: 'array' })
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]]
        const students = XLSX.utils.sheet_to_json(firstSheet)
        
        if (students.length === 0) {
          throw new Error('No data found in Excel file')
        }

        // 计算总费用
        const serviceType = batchForm.operationType === 'verify' ? 'student_verification' : 'student_gpa'
        const feePerStudent = getServiceFee(serviceType)
        const totalFee = feePerStudent * students.length

        // 检查余额
        await fetchUserBalance()
        if (currentBalance.value < totalFee) {
          message.error(`Balance not enough. Required: ${totalFee}, Current: ${currentBalance.value}`)
          return
        }

        // 扣除总费用
        try {
          const balanceRes = await usersApi.editBalance(userId.value, -totalFee)
          if (balanceRes.data.message === "Balance not enough") {
            message.error('Balance not enough')
            return
          }

          // 组织间转账
          await bankApi.transferByOrg({
            from_org_id: organizationId,
            to_org_id: activeOrganizationId,
            amount: totalFee,
          })

          message.success(`Deducted ${totalFee} successfully`)
          
          // 开始处理批量请求
          batchLoading.value = true
          batchResults.value = []
          batchProcessingStatus.type = 'info'
          batchProcessingStatus.message = 'Processing...'
          batchProcessingStatus.description = 'Please wait while we process your request'
          
          const results = batchForm.operationType === 'verify' 
            ? await processBatchVerify(students)
            : await processBatchGPA(students)
          
          batchResults.value = results
          const successCount = results.filter(r => r.status === 'success').length
          const failCount = results.length - successCount
          
          batchProcessingStatus.type = failCount === 0 ? 'success' : (successCount === 0 ? 'error' : 'warning')
          batchProcessingStatus.message = `Processing completed: ${successCount} succeeded, ${failCount} failed`
          batchProcessingStatus.description = failCount > 0 ? 'Some records failed to process. Please check the results table for details.' : 'All records processed successfully.'
        } catch (e) {
          message.error(e.response?.data?.detail || 'Balance deduction or transfer failed')
        } finally {
          batchLoading.value = false
        }
      } catch (error) {
        console.error('Error processing Excel file:', error)
        message.error('Failed to process Excel file: ' + error.message)
        batchProcessingStatus.type = 'error'
        batchProcessingStatus.message = 'Processing failed'
        batchProcessingStatus.description = error.message
        batchLoading.value = false
      }
    }
    
    reader.onerror = () => {
      message.error('Failed to read Excel file')
      batchLoading.value = false
      batchProcessingStatus.type = 'error'
      batchProcessingStatus.message = 'File reading failed'
      batchProcessingStatus.description = 'Unable to read the uploaded file'
    }
    
    reader.readAsArrayBuffer(batchForm.file)
  } catch (error) {
    console.error('Error in batch processing:', error)
    message.error('Batch processing failed: ' + error.message)
    batchLoading.value = false
    batchProcessingStatus.type = 'error'
    batchProcessingStatus.message = 'Processing failed'
    batchProcessingStatus.description = error.message
  }
}

const exportResults = () => {
  if (!batchResults.value.length) {
    message.warning('No results to export')
    return
  }
  
  const exportData = batchResults.value.map(result => ({
    Name: result.name,
    'Student ID': result.id,
    Status: result.status,
    Message: result.message,
    ...(batchForm.operationType === 'gpa' ? {
      GPA: result.gpa,
      'Enroll Year': result.enroll_year,
      'Graduation Year': result.graduation_year
    } : {})
  }))
  
  const ws = XLSX.utils.json_to_sheet(exportData)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Results')
  XLSX.writeFile(wb, `student_${batchForm.operationType}_results.xlsx`)
}

onMounted(() => { fetchStudentServices() })

</script>

<style scoped>
.gpa-result { margin-top: 24px; padding: 16px; background: #fafafa; border-radius: 4px; }
.batch-results { margin-top: 24px; }
.upload-tip { margin-top: 8px; color: rgba(0, 0, 0, 0.45); font-size: 14px; }
.upload-tip ul { margin: 8px 0; padding-left: 20px; }
.batch-actions { display: flex; justify-content: flex-end; }
</style> 