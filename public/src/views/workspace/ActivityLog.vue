<template>
  <div class="activity-log-container">
    <a-card class="activity-log-card" :bordered="false">
      <template #title>
        <div class="card-title">
          <span class="title-text">Activity Log</span>
          <a-tag color="blue" class="total-tag">Total Records: {{ pagination.total }}</a-tag>
        </div>
      </template>
      <template #extra>
        <span class="subtitle-text">View and search activity logs related to your organization</span>
      </template>

      <div class="search-section">
        <a-space size="middle" class="search-space">
          <a-input-search
            v-model:value="searchText"
            @search="fetchLogs"
            placeholder="Search by activity"
            class="search-input"
          >
            <template #prefix>
              <search-outlined />
            </template>
          </a-input-search>

          <a-input-number
            v-model:value="userId"
            placeholder="User ID"
            class="user-input"
            :min="1"
            @change="fetchLogs"
          >
            <template #prefix>
              <user-outlined />
            </template>
          </a-input-number>

          <a-range-picker
            v-model:value="dateRange"
            class="date-picker"
            @change="fetchLogs"
          >
            <template #prefix>
              <calendar-outlined />
            </template>
          </a-range-picker>
        </a-space>

        <div class="org-info">
          <a-tag color="green" class="org-tag">
            <template #icon><bank-outlined /></template>
            Organization ID: {{ organizationId }}
          </a-tag>
        </div>
      </div>

      <a-table
        :columns="columns"
        :data-source="logs"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        row-key="id"
        :bordered="false"
        class="log-table"
      >
        <template #created_at="{ text }">
          <span class="time-text">{{ new Date(text).toLocaleString() }}</span>
        </template>
        <template #log_type="{ text }">
          <a-tag :color="getLogTypeColor(text)" class="log-tag">{{ text }}</a-tag>
        </template>
        <template #organization_name="{ text }">
          <span class="org-name">{{ text || '-' }}</span>
        </template>
        <template #details="{ record }">
          <a-typography-paragraph
            :ellipsis="{ rows: 2, expandable: true, symbol: 'more' }"
            :content="record.details"
            class="details-text"
          />
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import {
  SearchOutlined,
  UserOutlined,
  CalendarOutlined,
  BankOutlined
} from '@ant-design/icons-vue'
import { logApi } from '../../services/api'

const searchText = ref('')
const userId = ref(null)
const dateRange = ref([])
const logs = ref([])
const loading = ref(false)
const organizationId = ref(localStorage.getItem('organization_id'))

const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0,
  showSizeChanger: true,
  showTotal: (total) => `Total ${total} records`,
  showQuickJumper: true,
  pageSizeOptions: ['10', '20', '50', '100']
})

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id' },
  {
    title: 'Time',
    dataIndex: 'created_at',
    key: 'created_at',
    slots: { customRender: 'created_at' }
  },
  { title: 'User ID', dataIndex: 'user_id', key: 'user_id' },
  { title: 'Org ID', dataIndex: 'organization_id', key: 'organization_id' },
  {
    title: 'Type',
    dataIndex: 'log_type',
    key: 'log_type',
    slots: { customRender: 'log_type' }
  },
  { title: 'Action', dataIndex: 'action', key: 'action' },
  {
    title: 'Details',
    key: 'details',
    slots: { customRender: 'details' }
  }
]

const getLogTypeColor = (type) => {
  const map = {
    SYSTEM: 'blue',
    ORGANIZATION: 'green',
    LOGIN: 'cyan',
    LOGOUT: 'orange',
    COURSE: 'purple',
    SERVICE_ACCESS: 'geekblue',
    PAYMENT: 'gold',
    ADMIN_ACTION: 'magenta',
    USER: 'lime'
  }
  return map[type?.toUpperCase()] || 'blue'
}

const fetchLogs = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.current - 1) * pagination.pageSize,
      limit: pagination.pageSize
    }

    if (searchText.value) params.search = searchText.value.trim()
    if (userId.value) params.user_id = userId.value
    if (dateRange.value?.length === 2) {
      params.start_date = dateRange.value[0].format('YYYY-MM-DD')
      params.end_date = dateRange.value[1].format('YYYY-MM-DD')
    }

    const response = await logApi.getOrganizationLogs(organizationId.value, params)
    logs.value = response.data
    pagination.total = response.data.length // 如果后端返回 total 请改为 response.data.total
  } catch (error) {
    console.error('日志获取失败:', error)
    message.error('Failed to fetch logs')
  } finally {
    loading.value = false
  }
}

const handleTableChange = (pag) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchLogs()
}

onMounted(fetchLogs)
</script>

<style scoped>
.activity-log-container {
  padding: 24px;
  min-height: 100%;
  background: #f0f2f5;
}

.activity-log-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-text {
  font-size: 18px;
  font-weight: 600;
  color: #1f1f1f;
}

.subtitle-text {
  color: #666;
  font-size: 14px;
}

.total-tag {
  font-size: 13px;
  padding: 2px 8px;
  border-radius: 4px;
}

.search-section {
  margin: 24px 0;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
}

.search-space {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 16px;
}

.search-input {
  width: 280px;
}

.user-input {
  width: 180px;
}

.date-picker {
  width: 280px;
}

.org-info {
  margin-top: 16px;
}

.org-tag {
  font-size: 13px;
  padding: 4px 12px;
  border-radius: 4px;
}

.log-table {
  margin-top: 16px;
}

.log-table :deep(.ant-table-thead > tr > th) {
  background: #fafafa;
  font-weight: 600;
  color: #1f1f1f;
}

.log-table :deep(.ant-table-tbody > tr:hover > td) {
  background: #f5f5f5;
}

.time-text {
  color: #666;
  font-size: 13px;
}

.log-tag {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
}

.org-name {
  color: #1890ff;
  font-weight: 500;
}

.details-text {
  margin-bottom: 0;
  line-height: 1.5;
  color: #666;
}

/* 统一输入框样式 */
:deep(.ant-input-affix-wrapper),
:deep(.ant-input-number),
:deep(.ant-picker) {
  border-radius: 6px;
  border: 1px solid #d9d9d9;
  transition: all 0.3s;
}

:deep(.ant-input-affix-wrapper:hover),
:deep(.ant-input-number:hover),
:deep(.ant-picker:hover) {
  border-color: #40a9ff;
}

:deep(.ant-input-affix-wrapper-focused),
:deep(.ant-input-number-focused),
:deep(.ant-picker-focused) {
  border-color: #40a9ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

/* 表格样式优化 */
:deep(.ant-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.ant-table-thead > tr > th) {
  background: #fafafa;
  font-weight: 600;
}

:deep(.ant-table-tbody > tr > td) {
  border-bottom: 1px solid #f0f0f0;
}

:deep(.ant-pagination-item) {
  border-radius: 4px;
}

:deep(.ant-pagination-item-active) {
  background: #1890ff;
  border-color: #1890ff;
}

:deep(.ant-pagination-item-active a) {
  color: #fff;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .search-space {
    flex-direction: column;
  }
  
  .search-input,
  .user-input,
  .date-picker {
    width: 100%;
  }
}
</style>
