<template>
  <div class="services-management">
    <a-card title="Services Management" :bordered="false">
      <!-- Create New Service Button -->
      <div class="mb-4">
        <a-button type="primary" @click="showCreateModal">
          Create New Service
        </a-button>
      </div>

      <!-- Services List -->
      <div class="services-list">
        <a-table
          :columns="serviceColumns"
          :data-source="services"
          :loading="loading"
          :pagination="{ pageSize: 10 }"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'service_type'">
              {{ getServiceTypeLabel(record.service_type) }}
            </template>
            <template v-if="column.key === 'fee'">
              {{ record.fee_per_use }} {{ record.fee_unit }}
            </template>
            <template v-if="column.key === 'status'">
              <a-tag :color="record.is_active ? 'green' : 'red'">
                {{ record.is_active ? 'Active' : 'Inactive' }}
              </a-tag>
            </template>
            <template v-if="column.key === 'actions'">
              <a-space>
                <a-button
                  type="primary"
                  size="small"
                  @click="showEditModal(record)"
                >
                  Edit
                </a-button>
                <a-button
                  danger
                  size="small"
                  @click="confirmDelete(record)"
                >
                  Delete
                </a-button>
              </a-space>
            </template>
          </template>
        </a-table>
      </div>

      <!-- Create/Edit Service Modal -->
      <a-modal
        :open="modalVisible"
        :title="modalTitle"
        @ok="handleModalOk"
        @cancel="modalVisible = false"
        :confirmLoading="modalLoading"
      >
        <a-form
          :model="serviceForm"
          layout="vertical"
          :rules="formRules"
        >
          <a-form-item
            label="Service Type"
            name="service_type"
            :rules="[{ required: true, message: 'Please select service type' }]"
          >
            <a-select
              v-model:value="serviceForm.service_type"
              placeholder="Select service type"
            >
              <a-select-option value="course_sharing">Course Sharing</a-select-option>
              <a-select-option value="student_verification">Student Verification</a-select-option>
              <a-select-option value="paper_sharing">Paper Sharing</a-select-option>
              <a-select-option value="student_gpa">Student GPA Record</a-select-option>
              <a-select-option value="data_vault">Data Vault</a-select-option>
              <a-select-option value="paper_pdf">Paper PDF Retrieval</a-select-option>
              <a-select-option value="bank_auth">Bank Account Authentication</a-select-option>
              <a-select-option value="bank_transfer">Bank Transfer</a-select-option>
              <a-select-option value="custom_service">Custom Service</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item
            label="Service Name"
            name="name"
            :rules="[{ required: true, message: 'Please enter service name' }]"
          >
            <a-input v-model:value="serviceForm.name" placeholder="Enter service name" />
          </a-form-item>
          <a-form-item
            label="Description"
            name="description"
          >
            <a-textarea
              v-model:value="serviceForm.description"
              placeholder="Enter service description"
              :rows="4"
            />
          </a-form-item>
          <a-form-item
            label="Fee per Use"
            name="fee_per_use"
          >
            <a-input-number
              v-model:value="serviceForm.fee_per_use"
              :min="0"
              :step="0.01"
              style="width: 200px"
            />
          </a-form-item>
          <a-form-item
            label="Fee Unit"
            name="fee_unit"
          >
            <a-select
              v-model:value="serviceForm.fee_unit"
              style="width: 200px"
            >
              <a-select-option value="RMB">RMB</a-select-option>
              <a-select-option value="USD">USD</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item
            label="Service Status"
            name="is_active"
          >
            <a-switch v-model:checked="serviceForm.is_active" />
          </a-form-item>
          <a-form-item
            label="Public Service"
            name="is_public"
          >
            <a-switch v-model:checked="serviceForm.is_public" />
            <!-- {{ serviceForm.is_active }} -->
          </a-form-item>

        </a-form>
      </a-modal>
    </a-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message, Modal } from 'ant-design-vue'
import api from '../../services/api'

// 表格列定义
const serviceColumns = [
  {
    title: 'Service Name',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: 'Type',
    dataIndex: 'service_type',
    key: 'service_type',
  },
  {
    title: 'Description',
    dataIndex: 'description',
    key: 'description',
  },
  {
    title: 'Fee',
    key: 'fee',
    width: 120,
  },
  {
    title: 'Status',
    key: 'status',
    width: 100,
  },
  {
    title: 'Actions',
    key: 'actions',
    width: 150,
  },
]

// 状态变量
const services = ref([])
const loading = ref(false)
const modalVisible = ref(false)
const modalLoading = ref(false)
const modalTitle = ref('Create New Service')
const editingServiceId = ref(null)
const activeOrgId = ref(Number(localStorage.getItem('active_organization_id')) || myOrgId)

const serviceForm = reactive({
  service_type: undefined,
  name: '',
  description: '',
  fee_per_use: 0,
  fee_unit: 'RMB',
  is_active: true,
  is_public: false,
})

const formRules = {
  service_type: [{ required: true, message: 'Please select service type' }],
  name: [{ required: true, message: 'Please enter service name' }],
}

// 获取服务类型标签
const getServiceTypeLabel = (type) => {
  const typeMap = {
    course_sharing: 'Course Sharing',
    student_verification: 'Student Verification',
    paper_sharing: 'Paper Sharing',
    student_gpa: 'Student GPA Record',
    data_vault: 'Data Vault',
    paper_pdf: 'Paper PDF Retrieval',
    bank_auth: 'Bank Account Authentication',
    bank_transfer: 'Bank Transfer',
    custom_service: 'Custom Service',
  }
  return typeMap[type] || type
}

// 加载服务列表
const loadServices = async () => {

  loading.value = true
  const params = {
      organization_id: activeOrgId.value,
      skip: 0,
      limit: 100
    }
  try {
    const response = await api.services.getOrganizationServices(params)
    console.log('response:', response)
    services.value = response.data
  } catch (error) {
    message.error(error.response?.data?.detail || 'Failed to get service list')
    console.error('Error loading services:', error)
    message.error('loadServices params:', params)

  } finally {
    loading.value = false
  }
}

// 显示创建服务模态框
const showCreateModal = () => {
  modalTitle.value = 'Create New Service'
  editingServiceId.value = null
  Object.assign(serviceForm, {
    service_type: undefined,
    name: '',
    description: '',
    fee_per_use: 0,
    fee_unit: 'RMB',
    is_active: true,
    is_public: false,
  })
  modalVisible.value = true
}

// 显示编辑服务模态框
const showEditModal = (record) => {
  modalTitle.value = 'Edit Service'
  editingServiceId.value = record.id
  Object.assign(serviceForm, {
    service_type: record.service_type,
    name: record.name,
    description: record.description,
    fee_per_use: record.fee_per_use,
    fee_unit: record.fee_unit,
    is_active: record.is_active,
    is_public: record.is_public,
  })
  modalVisible.value = true
}

// 处理模态框确认
const handleModalOk = async () => {
  modalLoading.value = true
  try {
    if (editingServiceId.value) {
      // 更新服务
      await api.services.updateService(editingServiceId.value, serviceForm)
      message.success('Service updated successfully')
    } else {
      // 创建服务
      await api.services.createService(serviceForm)
      message.success('Service created successfully')
    }
    modalVisible.value = false
    loadServices()
  } catch (error) {
    message.error(error.response?.data?.detail || 'Operation failed')
    console.error('Error saving service:', error)
  } finally {
    modalLoading.value = false
  }
}

// 确认删除服务
const confirmDelete = (record) => {
  Modal.confirm({
    title: 'Are you sure you want to delete this service?',
    content: `Service: ${record.name}`,
    okText: 'Yes',
    okType: 'danger',
    cancelText: 'No',
    onOk: async () => {
      try {
        await api.services.deleteService(record.id)
        message.success('Service deleted successfully')
        loadServices()
      } catch (error) {
        message.error(error.response?.data?.detail || 'Failed to delete service')
        console.error('Error deleting service:', error)
      }
    },
  })
}

// 组件挂载时加载服务列表
onMounted(() => {

  loadServices()
})
</script>

<style scoped>
.services-management {
  padding: 24px;
  background: #fff;
  border-radius: 8px;
}

.mb-4 {
  margin-bottom: 16px;
}

:deep(.ant-card) {
  margin-bottom: 24px;
}

:deep(.ant-table-thead > tr > th) {
  background: #fafafa;
}

:deep(.ant-table-tbody > tr > td) {
  vertical-align: middle;
}
</style>
