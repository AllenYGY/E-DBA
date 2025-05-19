<template>
  <div class="organization-management">
    <a-tabs :activeKey="activeTab" @change="handleTabChange">
      <a-tab-pane key="verifications" tab="Verification Management">
        <div class="table-operations">
          <a-select
            :value="verificationFilter"
            style="width: 200px"
            placeholder="Filter by verification status"
            @change="onVerificationFilterChange"
          >
            <a-select-option value="all">All</a-select-option>
            <a-select-option value="pending">Pending</a-select-option>
            <a-select-option value="approved">Approved</a-select-option>
            <a-select-option value="rejected">Rejected</a-select-option>
          </a-select>
        </div>
        <a-table
          :columns="verificationColumns"
          :data-source="verifications"
          :loading="verificationLoading"
          :pagination="verificationPagination"
          @change="handleVerificationTableChange"
        >
          <template #verification_document="{ record }">
            <a-button 
              v-if="record.organization.verification_document" 
              type="link" 
              @click="downloadVerificationFile(record)"
            >
              <template #icon><DownloadOutlined /></template>
              Verification File
            </a-button>
            <span v-else>No file</span>
          </template>
          <template #e_admin_approved="{ record }">
            <div>
              <a-tag :color="getEAdminStatusColor(record)">
                {{ getEAdminStatusText(record) }}
              </a-tag>
              <div v-if="record.e_admin_comment" style="font-size: 12px; color: #888; margin-top: 2px;">
                {{ record.e_admin_comment }}
              </div>
            </div>
          </template>
          <template #senior_approved="{ record }">
  <div>
              <a-tag :color="getSeniorEAdminStatusColor(record)">
                {{ getSeniorEAdminStatusText(record) }}
              </a-tag>
              <div v-if="record.senior_comment" style="font-size: 12px; color: #888; margin-top: 2px;">
                {{ record.senior_comment }}
              </div>
            </div>
          </template>
          <template #verification_status="{ record }">
            <a-tag :color="record.organization.is_verified ? 'green' : 'orange'">
              {{ record.organization.is_verified ? 'Verified' : 'Unverified' }}
            </a-tag>
          </template>
          <template #created_at="{ text }">
            {{ new Date(text).toLocaleString() }}
          </template>
          <template #updated_at="{ text }">
            {{ new Date(text).toLocaleString() }}
          </template>
          <template #verification_action="{ record }">
            <div style="display: flex; flex-direction: column; gap: 4px; align-items: flex-start;">
              <a-button type="primary" size="small" @click="showVerificationDetail(record)">
                <template #icon><EyeOutlined /></template>
                View Details
              </a-button>
              <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                <a-button
                  v-if="currentUserRole === 'E_ADMIN'"
                  @click="handleVerification(record, true, 'eAdmin')"
                  size="small"
                >Pass</a-button>
                <a-button
                  v-if="currentUserRole === 'E_ADMIN'"
                  @click="handleVerification(record, false, 'eAdmin')"
                  danger
                  size="small"
                >Reject</a-button>
                <a-button
                  v-if="currentUserRole === 'SENIOR_E_ADMIN'"
                  @click="handleVerification(record, true, 'senior')"
                  size="small"
                >Pass</a-button>
                <a-button
                  v-if="currentUserRole === 'SENIOR_E_ADMIN'"
                  @click="handleVerification(record, false, 'senior')"
                  danger
                  size="small"
                >Reject</a-button>
                <a-button
                  v-if="currentUserRole === 'T_ADMIN'"
                  @click="handleVerification(record, true, 'tAdmin')"
                  size="small"
                >Pass</a-button>
                <a-button
                  v-if="currentUserRole === 'T_ADMIN'"
                  @click="handleVerification(record, false, 'tAdmin')"
                  danger
                  size="small"
                >Reject</a-button>
              </div>
            </div>
          </template>
        </a-table>
      </a-tab-pane>
      <a-tab-pane key="organizations" tab="Organization List">
        <div class="table-operations">
          <a-input-search
            :value="searchText"
            placeholder="Search organization name"
            style="width: 200px"
            @search="onSearch"
          />
        </div>
        <a-table
          :columns="orgColumns"
          :data-source="organizations"
          :loading="loading"
          :pagination="pagination"
          @change="handleTableChange"
        >
          <template #status="{ record }">
            <a-space>
              <a-tag :color="record.is_verified ? 'green' : 'orange'">
                {{ record.is_verified ? 'Verified' : 'Unverified' }}
              </a-tag>
              <a-tag :color="record.is_active ? 'blue' : 'red'">
                {{ record.is_active ? 'Active' : 'Inactive' }}
              </a-tag>
            </a-space>
          </template>
          <template #created_at="{ text }">
            {{ new Date(text).toLocaleString() }}
          </template>
          <template #updated_at="{ text }">
            {{ new Date(text).toLocaleString() }}
          </template>
          <template #action="{ record }">
            <a-space>
              <a-button type="link" @click="showEditModal(record)">
                <template #icon><EditOutlined /></template>
                Edit
              </a-button>
              <a-button type="link" @click="showVerificationModal(record)">
                <template #icon><SafetyCertificateOutlined /></template>
                Verification
              </a-button>
            </a-space>
          </template>
        </a-table>
      </a-tab-pane>

    </a-tabs>

    <!-- Edit organization information modal -->
    <a-modal
      :open="editModalVisible"
      title="Edit Organization Information"
      @ok="handleEditSubmit"
      @cancel="handleEditCancel"
    >
      <a-form
        :model="editForm" 
        :rules="editRules"
        ref="editFormRef"
        layout="vertical"
      >
        <a-form-item label="Organization Name" name="name">
          <a-input v-model:value="editForm.name" placeholder="Organization name" />
        </a-form-item>
        <a-form-item label="Organization Full Name" name="full_name">
          <a-textarea v-model:value="editForm.full_name" :rows="4" placeholder="Organization full name" />
        </a-form-item>
        <a-form-item label="Email Domain" name="email_domain">
          <a-input v-model:value="editForm.email_domain" placeholder="Email domain" />
        </a-form-item>
        <a-form-item label="Organization Status" name="is_active">
          <a-switch v-model:value="editForm.is_active" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- Verification details modal -->
    <a-modal
      :open="verificationDetailVisible"
      title="Verification Details"
      width="800px"
      :footer="null"
      @cancel="verificationDetailVisible = false"
      closable
    >
      <a-descriptions bordered>
        <a-descriptions-item label="Organization Name" :span="3">
          {{ currentVerification?.organization?.name }}
        </a-descriptions-item>
        <a-descriptions-item label="Verification File" :span="3">
          <a-button type="link" @click="downloadVerificationFile(currentVerification)">
            <template #icon><DownloadOutlined /></template>
            Download verification file
          </a-button>
        </a-descriptions-item>
        <a-descriptions-item label="E-Admin Review" :span="3">
          <a-tag :color="getEAdminStatusColor(currentVerification)">
            {{ getEAdminStatusText(currentVerification) }}
          </a-tag>
          <div v-if="currentVerification?.e_admin_comment">
            Note: {{ currentVerification.e_admin_comment }}
          </div>
        </a-descriptions-item>
        <a-descriptions-item label="Senior E-Admin Review" :span="3">
          <a-tag :color="getSeniorEAdminStatusColor(currentVerification)">
            {{ getSeniorEAdminStatusText(currentVerification) }}
          </a-tag>
          <div v-if="currentVerification?.senior_comment">
            Note: {{ currentVerification.senior_comment }}
          </div>
        </a-descriptions-item>
      </a-descriptions>
    </a-modal>

    <!-- New: Review comment modal -->
    <a-modal
      :open="reviewModalVisible"
      title="Please enter review comment"
      @ok="submitReview"
      @cancel="() => (reviewModalVisible = false)"
    >
      <a-textarea v-model:value="reviewComment" placeholder="Please enter comment" :rows="4" />
    </a-modal>
  </div>
</template>
<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message, Modal, Input } from 'ant-design-vue'
import {
  EditOutlined,
  SafetyCertificateOutlined,
  EyeOutlined,
  CheckOutlined,
  CloseOutlined,
  DownloadOutlined
} from '@ant-design/icons-vue'
import { organizationApi, verificationApi } from '../../services/api'

// 状态变量
const activeTab =  ref('verifications')
const loading = ref(false)
const verificationLoading = ref(false)
const searchText = ref('')
const verificationFilter = ref('all')
const editModalVisible = ref(false)
const verificationDetailVisible = ref(false)
const currentVerification = ref(null)
const organizations = ref([])
const verifications = ref([])
const currentUserRole = ref(localStorage.getItem('role') || 'E_ADMIN')

// 新增：审核评论输入
const reviewModalVisible = ref(false)
const reviewComment = ref('')
const reviewAction = ref({}) // { record, approved, roleType }

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showTotal: (total) => `Total ${total} records`,
  showQuickJumper: true,
  pageSizeOptions: ['10', '20', '50', '100'],
})

const verificationPagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showTotal: (total) => `Total ${total} records`,
  showQuickJumper: true,
  pageSizeOptions: ['10', '20', '50', '100'],
})

// 表格列定义
const orgColumns = [
  {
    title: 'Organization ID',
    dataIndex: 'id',
    key: 'id',
  },
  {
    title: 'Organization Name',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: 'Organization Full Name',
    dataIndex: 'full_name',
    key: 'full_name',
    ellipsis: true,
  },
  {
    title: 'Email Domain',
    dataIndex: 'email_domain',
    key: 'email_domain',
  },
  {
    title: 'Status',
    key: 'status',
    slots: { customRender: 'status' },
  },
  {
    title: 'Created Time',
    dataIndex: 'created_at',
    key: 'created_at',
    slots: { customRender: 'created_at' },
  },
  {
    title: 'Updated Time',
    dataIndex: 'updated_at',
    key: 'updated_at',
    slots: { customRender: 'updated_at' },
  },
  {
    title: 'Action',
    key: 'action',
    width: 200,
    slots: { customRender: 'action' },
  },
]

const verificationColumns = [
  {
    title: 'Organization ID',
    dataIndex: 'organization_id',
    key: 'organization_id',
  },
  {
    title: 'Organization Name',
    dataIndex: ['organization', 'name'],
    key: 'organization_name',
  },
  {
    title: 'Email Domain',
    dataIndex: ['organization', 'email_domain'],
    key: 'organization_email_domain',
  },
  {
    title: 'Organization Full Name',
    dataIndex: ['organization', 'full_name'],
    key: 'organization_full_name',
    ellipsis: true,
  },
  {
    title: 'Verification File',
    key: 'verification_document',
    slots: { customRender: 'verification_document' },
  },
  {
    title: 'E-Admin Review',
    key: 'e_admin_approved',
    slots: { customRender: 'e_admin_approved' },
  },
  {
    title: 'Senior E-Admin Review',
    key: 'senior_approved',
    slots: { customRender: 'senior_approved' },
  },
  {
    title: 'Status',
    key: 'status',
    slots: { customRender: 'verification_status' },
  },
  {
    title: 'Application Time',
    dataIndex: 'submitted_at',
    key: 'submitted_at',
    slots: { customRender: 'created_at' },
  },
  {
    title: 'Updated Time',
    dataIndex: 'e_admin_reviewed_at',
    key: 'e_admin_reviewed_at',
    slots: { customRender: 'updated_at' },
  },
  {
    title: 'Action',
    key: 'action',
    width: 150,
    slots: { customRender: 'verification_action' },
  },
]

// 表单相关
const editFormRef = ref(null)
const editForm = reactive({
  id: null,
  name: '',
  full_name: '',
  email_domain: '',
  is_active: true,
  is_verified: false,
})

const editRules = {
  name: [{ required: true, message: 'Please enter organization name' }],
  full_name: [{ required: true, message: 'Please enter organization full name' }],
  email_domain: [{ required: true, message: 'Please enter email domain' }],
}

// 方法定义
const fetchOrganizations = async () => {
  loading.value = true
  try {
    console.log('Fetching organizations with params:', {
      skip: (pagination.current - 1) * pagination.pageSize,
      limit: pagination.pageSize
    })
    const response = await organizationApi.getOrganizations({
      skip: (pagination.current - 1) * pagination.pageSize,
      limit: pagination.pageSize
    })
    console.log('Received organizations data:', response)
    
    // 从 Axios 响应中获取实际数据
    const data = response.data
    if (data && Array.isArray(data)) {
      organizations.value = data
      pagination.total = data.length
    } else if (data && data.items && Array.isArray(data.items)) {
      organizations.value = data.items
      pagination.total = data.total || data.items.length
    } else {
      console.error('Invalid data format received:', data)
      message.error('Failed to fetch organization list: Invalid data format')
    }
  } catch (error) {
    console.error('Error fetching organizations:', error)
    message.error(`Failed to fetch organization list: ${error.message || 'Unknown error'}`)
  } finally {
    loading.value = false
  }
}

const fetchVerifications = async () => {
  verificationLoading.value = true
  try {
    const params = {
      skip: (verificationPagination.current - 1) * verificationPagination.pageSize,
      limit: verificationPagination.pageSize
    }
    
    // 根据用户角色和筛选条件添加状态参数
    if (verificationFilter.value !== 'all') {
      if (currentUserRole.value === 'E_ADMIN') {
        // E-Admin 只关注 e_admin_status
        if (verificationFilter.value === 'pending') {
          params.status = 'PENDING'
        } else if (verificationFilter.value === 'approved') {
          params.status = 'APPROVAL'
        } else if (verificationFilter.value === 'rejected') {
          params.status = 'REJECTION'
        }
      } else if (currentUserRole.value === 'SENIOR_E_ADMIN') {
        // Senior E-Admin 只关注 senior_status
        if (verificationFilter.value === 'pending') {
          params.status = 'PENDING'
        } else if (verificationFilter.value === 'approved') {
          params.status = 'APPROVAL'
        } else if (verificationFilter.value === 'rejected') {
          params.status = 'REJECTION'
        }
      }
      else if (currentUserRole.value === 'T_ADMIN') {
        if (verificationFilter.value === 'pending') {
          params.e_admin_status = 'PENDING'
          params.senior_status = 'PENDING'
        } else if (verificationFilter.value === 'approved') {
          params.e_admin_status = 'APPROVAL'
          params.senior_status = 'APPROVAL'
        } else if (verificationFilter.value === 'rejected') {
          params.e_admin_status = 'REJECTION'
          params.senior_status = 'REJECTION'
        }
      }
    }

    let response
    if (currentUserRole.value === 'E_ADMIN') {
      response = await verificationApi.getByEAdminStatus(params)
    } else if (currentUserRole.value === 'SENIOR_E_ADMIN') {
      response = await verificationApi.getBySeniorStatus(params)
    } else {
      response = await verificationApi.getVerificationsByStatus(params)
    }
    const data = response.data
    if (data && data.items && Array.isArray(data.items)) {
      verifications.value = data.items
      verificationPagination.total = data.total || data.items.length
    } else {
      verifications.value = []
      verificationPagination.total = 0
      message.error('Failed to fetch verification list: Invalid data format')
    }
  } catch (error) {
    console.error('Error fetching verifications:', error)
    message.error(`Failed to fetch verification list: ${error.message || 'Unknown error'}`)
  } finally {
    verificationLoading.value = false
  }
}

const showEditModal = (record) => {
  editForm.id = record.id
  editForm.name = record.name
  editForm.full_name = record.full_name
  editForm.email_domain = record.email_domain
  editForm.is_active = record.is_active
  editForm.is_verified = record.is_verified
  editModalVisible.value = true
}

const handleEditSubmit = async () => {
  try {
    await editFormRef.value.validate()
    await organizationApi.updateOrganization(editForm.id, editForm)
    message.success('Update successful')
    editModalVisible.value = false
    fetchOrganizations()
  } catch (error) {
    message.error('Update failed')
  }
}

const handleEditCancel = () => {
  editModalVisible.value = false
}

const showVerificationModal = (record) => {
  // 实现验证模态框逻辑
}

const showVerificationDetail = (record) => {
  currentVerification.value = record
  verificationDetailVisible.value = true
}

const handleVerification = (record, approved, roleType) => {
  reviewAction.value = { record, approved, roleType }
  reviewComment.value = ''
  reviewModalVisible.value = true
}

const submitReview = async () => {
  const { record, approved, roleType } = reviewAction.value
  // 确保 approved 为 false 时使用 REJECTION
  const approvedStr = approved ? 'APPROVAL' : 'REJECTION'
  const comment = reviewComment.value || (approved ? 'Approved' : 'Rejected')
  try {
    console.log('Submitting review:', { roleType, approvedStr, comment }) // 添加日志
    if (roleType === 'eAdmin') {
      await verificationApi.eAdminReview(record.organization_id, { 
        e_admin_approved: approvedStr, 
        e_admin_comment: comment 
      })
    } else if (roleType === 'senior') {
      await verificationApi.seniorReview(record.organization_id, { 
        senior_approved: approvedStr, 
        senior_comment: comment 
      })
    } else if (roleType === 'tAdmin') {
      await verificationApi.tAdminReview(record.organization_id, { 
        approved: approvedStr, 
        comment 
      })
    }
    message.success(approved ? 'Review passed successfully' : 'Review rejected successfully')
    reviewModalVisible.value = false
    fetchVerifications()
  } catch (error) {
    console.error('Review submission failed:', error) // 添加错误日志
    message.error('Review submission failed: ' + (error.message || 'Unknown error'))
  }
}

const downloadVerificationFile = (record) => {
  const dataUrl = record.organization.verification_document
  if (!dataUrl) {
    message.error('Verification file does not exist')
    return
  }
  // 解析 data URL
  const arr = dataUrl.split(',')
  const mime = arr[0].match(/:(.*?);/)[1]
  const bstr = atob(arr[1])
  let n = bstr.length
  const u8arr = new Uint8Array(n)
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n)
  }
  const blob = new Blob([u8arr], { type: mime })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `verification_${record.organization_id}.pdf`
  document.body.appendChild(a)
  a.click()
  window.URL.revokeObjectURL(url)
  document.body.removeChild(a)
}

// 工具方法
const getVerificationStatusColor = (record) => {
  if (record.senior_approved) return 'green'
  if (record.senior_approved === false) return 'red'
  if (record.e_admin_approved) return 'blue'
  if (record.e_admin_approved === false) return 'orange'
  return 'default'
}

const getVerificationStatusText = (record) => {
  if (record.senior_approved) return 'Approved'
  if (record.senior_approved === false) return 'Rejected'
  if (record.e_admin_approved) return 'E-Admin Approved'
  if (record.e_admin_approved === false) return 'E-Admin Rejected'
  return 'Pending'
}

const getEAdminStatusColor = (record) => {
  if (record?.e_admin_approved === 'APPROVAL') return 'green'
  if (record?.e_admin_approved === 'REJECTION') return 'red'
  if (record?.e_admin_approved === 'PENDING') return 'orange'
  return 'default'
}

const getEAdminStatusText = (record) => {
  if (record?.e_admin_approved === 'APPROVAL') return 'Approved'
  if (record?.e_admin_approved === 'REJECTION') return 'Rejected'
  if (record?.e_admin_approved === 'PENDING') return 'Pending'
  return ''
}

const getSeniorEAdminStatusColor = (record) => {
  if (record?.senior_approved === 'APPROVAL') return 'green'
  if (record?.senior_approved === 'REJECTION') return 'red'
  if (record?.senior_approved === 'PENDING') return 'orange'
  return 'default'
}

const getSeniorEAdminStatusText = (record) => {
  if (record?.senior_approved === 'APPROVAL') return 'Approved'
  if (record?.senior_approved === 'REJECTION') return 'Rejected'
  if (record?.senior_approved === 'PENDING') return 'Pending'
  return ''
}

// 事件处理
const handleTableChange = (pag, filters, sorter) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchOrganizations()
}

const handleVerificationTableChange = (pag, filters, sorter) => {
  verificationPagination.current = pag.current
  verificationPagination.pageSize = pag.pageSize
  fetchVerifications()
}

const onSearch = () => {
  pagination.current = 1
  fetchOrganizations()
}

const onVerificationFilterChange = (value) => {
  verificationFilter.value = value
  verificationPagination.current = 1
  fetchVerifications()
}

// 添加 tab 切换处理
const handleTabChange = (key) => {
  activeTab.value = key
  if (key === 'verifications') {
    fetchVerifications()
  } else {
    fetchOrganizations()
  }
}

// 生命周期钩子
onMounted(() => {
  fetchOrganizations()
  fetchVerifications()
})
</script> 

<style scoped>
.organization-management {
  padding: 24px;
  background: #fff;
  border-radius: 8px;
}

.table-operations {
  margin-bottom: 16px;
  display: flex;
  gap: 16px;
}

:deep(.ant-table-thead > tr > th) {
  background: #fafafa;
}

:deep(.ant-table-tbody > tr > td) {
  vertical-align: top;
}

:deep(.ant-descriptions-item-label) {
  width: 150px;
}
</style> 