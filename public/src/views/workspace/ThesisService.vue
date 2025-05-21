<template>
  <a-card title="Thesis Services" :bordered="false">
    <a-alert v-if="!paperServices.length" type="warning" message="No thesis service found"
      description="Please contact the o-convener to enable the thesis service" show-icon style="margin-bottom: 16px" />
    <template v-else>
      <a-row :gutter="16" style="margin-bottom: 16px">
        <a-col :span="12">
          <a-form-item label="Thesis Search Service" required>
            <a-select v-model:value="selectedSearchService" style="width: 100%"
              placeholder="Please select the thesis search service">
              <a-select-option v-for="service in paperServices.filter(s => s.service_type === 'paper_sharing')"
                :key="service.id" :value="service.id">
                {{ service.name }}
              </a-select-option>
            </a-select>
          </a-form-item>
        </a-col>

      </a-row>

      <a-alert v-if="!selectedSearchService" type="info" message="Please select the thesis search service" show-icon
        style="margin-bottom: 16px" />
      <template v-else>
        <a-input-search v-model:value="searchKeyword" placeholder="Please enter the keywords to search for the thesis"
          enter-button="Search" @search="fetchPapers" style="max-width: 400px; margin-bottom: 16px;" />
        <a-table :data-source="papers" :loading="papersLoading" rowKey="id" :pagination="{ pageSize: 10 }">
          <a-table-column title="Thesis Title" dataIndex="title" key="title" />
          <a-table-column title="Abstract" dataIndex="abstract" key="abstract" />
          <a-table-column title="Fee" key="fee" :customRender="({ record }) => getServiceFee(record)" />
          <a-table-column title="Actions" key="actions">
            <template #default="{ record }">
              <a @click="onDownloadClick(record)">Download</a>
              <a-divider type="vertical" />
              <a @click="showPaperDetail(record)">Details</a>
            </template>
          </a-table-column>
        </a-table>
      </template>
    </template>

    <!-- 论文详情弹窗 -->
    <a-modal :open="paperDetailVisible" @update:open="val => paperDetailVisible = val" title="Thesis Details"
      :footer="null" @cancel="() => (paperDetailVisible = false)" width="600px">
      <div v-if="paperDetail">
        <h3>{{ paperDetail.title }}</h3>
        <p><b>Author:</b>{{ paperDetail.author }}</p>
        <p><b>Upload Time:</b>{{ paperDetail.created_at }}</p>
        <div v-if="paperDetail.abstract">
          <b>Abstract:</b>
          <div style="white-space: pre-wrap;">{{ paperDetail.abstract }}</div>
        </div>
      </div>
    </a-modal>

    <!-- 下载前余额确认弹窗 -->
    <a-modal
      :open="showBalanceModal"
      title="Confirm Download"
      @ok="confirmDownload"
      @cancel="showBalanceModal = false"
    >
      <p>Your current balance: <b>{{ currentBalance }}</b></p>
      <p>Are you sure you want to download this thesis?</p>
    </a-modal>
  </a-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { servicesApi } from '../../services/api'
import { usersApi } from '../../services/api'
import axios from 'axios'
import { QuestionCircleOutlined } from '@ant-design/icons-vue'
import { bankApi } from '../../services/api'

const paperServices = ref([])
const selectedSearchService = ref(null)
const selectedDownloadService = ref(null)
const papers = ref([])
const papersLoading = ref(false)
const paperDetail = ref(null)
const paperDetailVisible = ref(false)
const searchKeyword = ref('')
const showBalanceModal = ref(false)
const currentBalance = ref(0)
const userId = ref(null)
const pendingDownloadRecord = ref(null)

const permissionLevel = Number(localStorage.getItem('permission_level'))
const organizationId = Number(localStorage.getItem('organization_id'))
const activeOrganizationId = Number(localStorage.getItem('active_organization_id'))

const fetchPaperServices = async () => {
  try {
    const res = await servicesApi.getOrganizationServices({ organization_id: activeOrganizationId })
    paperServices.value = res.data.filter(service =>
      (service.service_type === 'paper_sharing' || service.service_type === 'paper_pdf') &&
      service.is_active
    )
    const searchServices = paperServices.value.filter(s => s.service_type === 'paper_sharing')
    const downloadServices = paperServices.value.filter(s => s.service_type === 'paper_pdf')
    if (searchServices.length > 0) {
      selectedSearchService.value = searchServices[0].id
    }
    if (downloadServices.length > 0) {
      selectedDownloadService.value = downloadServices[0].id
    }
  } catch (e) {
    message.error('Failed to get service configuration')
  }
}

const fetchPapers = async () => {
  if (!selectedSearchService.value) {
    message.error('Please select a paper search service first')
    return
  }
  if (!searchKeyword.value) {
    papers.value = []
    return
  }
  const searchService = paperServices.value.find(s => s.id === selectedSearchService.value)
  if (!searchService) {
    message.error('Selected search service not found')
    return
  }
  if (!searchService.base_url || !searchService.api_path) {
    message.error('Service configuration is incomplete, please check the base URL and API path')
    return
  }
  papersLoading.value = true
  try {
    let requestData = {}
    if (searchService.input_format) {
      requestData = {
        keywords: searchKeyword.value,
        page: 1,
        page_size: 10
      }
    } else {
      requestData = {
        query: searchKeyword.value
      }
    }
    const response = await axios({
      method: searchService.api_method || 'POST',
      url: `${searchService.base_url}${searchService.api_path}`,
      data: requestData,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    if (response.data) {
      if (Array.isArray(response.data)) {
        papers.value = response.data
      } else if (response.data.items) {
        papers.value = response.data.items
      } else if (response.data.data) {
        papers.value = response.data.data
      } else if (response.data.results) {
        papers.value = response.data.results
      } else {
        papers.value = [response.data]
      }
    } else {
      papers.value = []
    }
    if (papers.value.length === 0) {
      message.info('No related papers found')
    }
  } catch (e) {
    if (e.response) {
      message.error(e.response.data.message || 'Failed to get paper list')
    } else if (e.request) {
      message.error('Failed to connect to server')
    } else {
      message.error('Error occurred while searching papers')
    }
  } finally {
    papersLoading.value = false
  }
}

const showPaperDetail = (record) => {
  paperDetail.value = record
  paperDetailVisible.value = true
}

const handleDownloadPaper = async (record) => {
  if (!selectedDownloadService.value) {
    message.error('Please select a paper download service first')
    return
  }
  const downloadService = paperServices.value.find(s => s.id === selectedDownloadService.value)
  if (!downloadService) {
    message.error('Selected download service not found')
    return
  }
  const baseUrl = downloadService.base_url.endsWith('/') ? downloadService.base_url.slice(0, -1) : downloadService.base_url
  const apiPath = downloadService.api_path.startsWith('/') ? downloadService.api_path : '/' + downloadService.api_path
  const fullUrl = `${baseUrl}${apiPath}`
  try {
    const response = await axios.get(
      fullUrl,
      {
        params: { title: record.title },
        responseType: 'blob'
      }
    )
    const contentType = response.headers['content-type']
    if (contentType && contentType.includes('application/pdf')) {
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${record.title || 'paper'}.pdf`)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      message.success('Download successful')
    } else {
      const reader = new FileReader()
      reader.onload = () => {
        try {
          const errorData = JSON.parse(reader.result)
          message.error(errorData.detail || errorData.message || 'Download failed')
        } catch {
          message.error('Download failed')
        }
      }
      reader.readAsText(response.data)
    }
  } catch (e) {
    message.error('Download request failed')
  }
}

// get service fee
const getServiceFee = () => {
  // 只查找 paper_pdf 类型的服务
  const service = paperServices.value.find(s => s.service_type === 'paper_pdf')
  if (service && service.fee_per_use !== undefined && service.fee_unit) {
    return `${service.fee_per_use}`
  }
  return '-'
}

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

const onDownloadClick = async (record) => {
  await fetchUserBalance()
  pendingDownloadRecord.value = record
  showBalanceModal.value = true
}

const confirmDownload = async () => {
  showBalanceModal.value = false
  if (pendingDownloadRecord.value) {
    // 获取 paper_pdf 服务的费用
    const service = paperServices.value.find(s => s.service_type === 'paper_pdf')
    const fee = service && service.fee_per_use ? Number(service.fee_per_use) : 0
    if (!userId.value || !fee) {
      message.error('User info or service fee error')
      pendingDownloadRecord.value = null
      return
    }
    try {
      // 1. 扣除用户余额
      const balanceRes = await usersApi.editBalance(userId.value, -fee)
      // 检查余额是否足够
      if (balanceRes.data.message === "Balance not enough") {
        message.error('Balance not enough')
        pendingDownloadRecord.value = null
        return
      }
      // 2. 组织间转账
      const res = await bankApi.transferByOrg({
        from_org_id: organizationId,
        to_org_id: activeOrganizationId,
        amount: fee,
      })
      console.log(res)
      message.success(`Deducted ${fee} successfully`)
      handleDownloadPaper(pendingDownloadRecord.value)
    } catch (e) {
      message.error(e.response?.data?.detail || 'Balance deduction or transfer failed')
    }
    pendingDownloadRecord.value = null
  }
}

onMounted(() => {
  fetchPaperServices()
  fetchUserBalance()
})
</script>