<template>
  <div class="user-management-container">
    <a-page-header
      title="Manage User Access and Payment Quota"
      sub-title="Add balance to users for thesis download access"
      class="mb-20"
    />

    <!-- Search Section -->
    <a-card :bordered="false" class="search-card">
      <a-space size="middle" class="search-space">
        <a-input
          v-model="searchForm.username"
          placeholder="Search by username"
          style="width: 200px"
          @input="fetchUsers"
        />
        <a-input
          v-model="searchForm.email"
          placeholder="Search by email"
          style="width: 200px"
          @input="fetchUsers"
        />
        <a-input-number
          v-model="searchForm.role"
          placeholder="Role"
          style="width: 120px"
          @change="fetchUsers"
        />
      </a-space>
    </a-card>

    <!-- User List Section -->
    <a-card :bordered="false" class="user-list-card">
      <a-table
        :columns="columns"
        :data-source="users"
        :loading="loading"
        row-key="id"
        :pagination="pagination"
        @change="handleTableChange"
        :bordered="false"
      >
        <template #user_name="{ text }">
          <span>{{ text || '-' }}</span>
        </template>
        <template #email="{ text }">
          <span>{{ text || '-' }}</span>
        </template>
        <template #balance="{ text, record }">
          <span>{{ text || '-' }}</span>
        </template>
      </a-table>
    </a-card>

    <!-- Add Balance Section (Bottom Section) -->
    <a-card :bordered="false" class="balance-card" style="margin-top: 20px;">
      <a-space direction="vertical">
        <a-input-number
          v-model:value="userId"
          placeholder="Enter User ID"
          style="width: 150px"
        />
        <a-input-number
          v-model:value="amount"
          :min="0"
          placeholder="Amount to add"
          style="width: 150px"
        />
        <a-button
          type="primary"
          @click="submitBalance"
          :loading="loadingBalance"
        >
          Add Balance
        </a-button>
      </a-space>
    </a-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { usersApi } from '../../services/api'

const users = ref([])  // Array to hold user data
const loading = ref(false)  // Loading state for user data
const loadingBalance = ref(false)  // Loading state for adding balance
const userId = ref(null)  // User ID to add balance
const amount = ref(0)  // Amount to be added
const searchForm = reactive({
  username: '',
  email: '',
  role: null,
  organization_id: localStorage.getItem('organization_id')
})  // Search form object to handle search parameters
const organizationId = ref(localStorage.getItem('organization_id'))  // Get organization ID from localStorage

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  pageSizeOptions: ['10', '20', '50']
})

// Columns
const columns = [
  { title: 'User ID', dataIndex: 'id', key: 'id' },
  { title: 'User Name', dataIndex: 'username', key: 'username', slots: { customRender: 'user_name' } },
  { title: 'Email', dataIndex: 'email', key: 'email', slots: { customRender: 'email' } },
  {
    title: 'Current Balance/Quota', 
    dataIndex: 'balance', 
    key: 'balance',
    slots: { customRender: 'balance' }
  }
]

const fetchUsers = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.current - 1) * pagination.pageSize,
      limit: pagination.pageSize,
      username: searchForm.username,
      email: searchForm.email,
      role: searchForm.role,
      organization_id: organizationId.value,
    }

    console.log('Search params:', params)

    const response = await usersApi.searchUsers(params)
    
    if (response.data && response.data.items) {
      users.value = response.data.items
      pagination.total = response.data.total || 0  // Update total count
    } else {
      message.error('获取用户列表失败：数据格式无效')
    }
  } catch (error) {
    message.error('获取用户列表失败，请稍后再试')
  } finally {
    loading.value = false
  }
}

// Handle Add Balance functionality for a specific user
const submitBalance = async () => {
  if (!userId.value || userId.value <= 0) {
    message.error('请输入有效的用户 ID')
    return
  }
  if (amount.value <= 0) {
    message.error('请输入有效的金额')
    return
  }

  loadingBalance.value = true
  try {
    console.log('Adding balance for userId:', userId.value, 'Amount:', amount.value);

    // Here we call the addBalance API
    await usersApi.addBalance(userId.value, amount.value)
    message.success('余额添加成功')
    fetchUsers()  // Refresh user list after adding balance
  } catch (error) {
    console.error('Error adding balance:', error)
    message.error('添加余额失败')
  } finally {
    loadingBalance.value = false
  }
}

// Handle pagination and sorting
const handleTableChange = (pag) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchUsers()
}

onMounted(fetchUsers)  // Fetch users on component mount
</script>

<style scoped>
.user-management-container {
  margin: 20px;
}

.mb-20 {
  margin-bottom: 20px;
}

.search-card {
  margin-bottom: 24px;
  background: #fff;
  border-radius: 8px;
}

.user-list-card {
  margin-bottom: 24px;
  background: #fff;
  border-radius: 8px;
}

.balance-card {
  background: #fff;
  border-radius: 8px;
}

a-space {
  display: flex;
  flex-direction: column;
}

a-table {
  margin-top: 16px;
}

.details-text {
  margin-bottom: 0;
  line-height: 1.5;
}

:deep(.ant-table),
:deep(.ant-input-number),
:deep(.ant-picker),
:deep(.ant-tag),
:deep(.ant-card-body),
:deep(.ant-select:not(.ant-select-customize-input) .ant-select-selector),
:deep(.ant-input-search .ant-input) {
  border-radius: 4px;
}
</style>
