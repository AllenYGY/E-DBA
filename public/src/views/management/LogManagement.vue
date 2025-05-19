<template>
    <div class="system-log">
        <a-page-header title="System Log" sub-title="View and search system operation logs" class="mb-20">
            <template #extra>
                <a-tag color="blue">Total Records: {{ pagination.total }}</a-tag>
            </template>
        </a-page-header>

        <a-card :bordered="false" class="search-card">
            <a-row>
                <a-col :span="24">
                    <a-space size="middle" class="search-space">
                        <a-input-search 
                            :value="searchText"
                            @update:value="val => searchText = val"
                            placeholder="Search by user or action" 
                            style="width: 250px" 
                            @search="onSearch"
                        >
                            <template #prefix>
                                <search-outlined />
                            </template>
                        </a-input-search>

                        <a-input-number 
                            :value="userId"
                            @update:value="val => userId = val"
                            placeholder="User ID" 
                            style="width: 120px" 
                            :min="1" 
                            @change="onUserIdChange"
                        >
                            <template #prefix>
                                <user-outlined />
                            </template>
                        </a-input-number>

                        <a-input-number 
                            :value="organizationId"
                            @update:value="val => organizationId = val"
                            placeholder="Org ID" 
                            style="width: 120px" 
                            :min="1" 
                            @change="onOrgIdChange"
                        >
                            <template #prefix>
                                <team-outlined />
                            </template>
                        </a-input-number>

                        <a-select 
                            :value="logType"
                            @update:value="val => logType = val"
                            placeholder="Log Type" 
                            style="width: 150px" 
                            allow-clear 
                            @change="onLogTypeChange"
                        >
                            <template #prefix>
                                <audit-outlined />
                            </template>
                            <a-select-option value="">All Types</a-select-option>
                            <a-select-option value="ORGANIZATION">Organization</a-select-option>
                            <a-select-option value="SYSTEM">System</a-select-option>
                            <a-select-option value="LOGIN">Login</a-select-option>
                            <a-select-option value="COURSE">Course</a-select-option>
                            <a-select-option value="LOGOUT">Logout</a-select-option>
                            <a-select-option value="SERVICE_ACCESS">Service Access</a-select-option>
                            <a-select-option value="PAYMENT">Payment</a-select-option>
                            <a-select-option value="ADMIN_ACTION">Admin Action</a-select-option>
                        </a-select>

                        <a-range-picker v-model="dateRange" style="width: 260px" @change="fetchLogs">
                            <template #prefix>
                                <calendar-outlined />
                            </template>
                        </a-range-picker>
                    </a-space>
                </a-col>
            </a-row>

            <a-table :columns="columns" :data-source="logs" :loading="loading" :pagination="pagination"
                @change="handleTableChange" row-key="id" :bordered="false"
                :rowClassName="(_, idx) => idx % 2 === 1 ? 'table-row-striped' : ''" class="log-table">
                <template #created_at="{ text }">
                    {{ new Date(text).toLocaleString() }}
                </template>
                <template #log_type="{ text }">
                    <a-tag :color="getLogTypeColor(text)">{{ text }}</a-tag>
                </template>
                <template #organization_name="{ text }">
                    <span>{{ text || '-' }}</span>
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
    TeamOutlined,
    AuditOutlined,
    CalendarOutlined
} from '@ant-design/icons-vue'
import { logApi } from '../../services/api' // 你需要实现对应的API

const searchText = ref('')
const logType = ref('')
const userId = ref(null)
const organizationId = ref(null)
const logs = ref([])
const loading = ref(false)
const dateRange = ref([])

const pagination = reactive({
    current: 1,
    pageSize: 20,
    total: 0,
    showSizeChanger: true,
    showTotal: (total) => `Total ${total} records`,
    showQuickJumper: true,
    pageSizeOptions: ['10', '20', '50', '100'],
})

const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Time', dataIndex: 'created_at', key: 'created_at', slots: { customRender: 'created_at' } },
    { title: 'User ID', dataIndex: 'user_id', key: 'user_id' },
    { title: 'Org ID', dataIndex: 'organization_id', key: 'organization_id' },
    { title: 'Type', dataIndex: 'log_type', key: 'log_type', slots: { customRender: 'log_type' } },
    { title: 'Action', dataIndex: 'action', key: 'action' },
    { title: 'Details', key: 'details', slots: { customRender: 'details' } },
]

const getLogTypeColor = (type) => {
    // 确保类型是字符串并转换为大写
    const normalizedType = String(type).toUpperCase().trim();
    
    const colorMap = {
        'SYSTEM': 'blue',         // 系统级操作 - 蓝色
        'ORGANIZATION': 'green',  // 组织相关 - 绿色
        'LOGIN': 'cyan',         // 登录 - 青色
        'LOGOUT': 'orange',      // 登出 - 橙色
        'COURSE': 'purple',      // 课程 - 紫色
        'SERVICE_ACCESS': 'geekblue', // 服务访问 - 极客蓝
        'PAYMENT': 'gold',       // 支付 - 金色
        'ADMIN_ACTION': 'magenta', // 管理员操作 - 品红色
        'USER': 'lime'           // 用户操作 - 青柠色
    };

    return colorMap[normalizedType] || 'blue';  // 如果没有匹配的类型，返回蓝色
}

const fetchLogs = async () => {
    loading.value = true
    try {
        console.log('Current values:', {
            searchText: searchText.value,
            logType: logType.value,
            userId: userId.value,
            organizationId: organizationId.value,
            dateRange: dateRange.value
        })

        const params = {
            skip: (pagination.current - 1) * pagination.pageSize,
            limit: pagination.pageSize
        }

        if (searchText.value) params.search = searchText.value.trim();
        if (logType.value) params.log_type = logType.value;
        if (userId.value) params.user_id = userId.value;
        if (organizationId.value) params.organization_id = organizationId.value;

        if (dateRange.value && dateRange.value.length === 2) {
            params.start_date = dateRange.value[0].format('YYYY-MM-DD');
            params.end_date = dateRange.value[1].format('YYYY-MM-DD');
        }

        console.log('Fetching logs with params:', params)
        const response = await logApi.getLogs(params)
        console.log('Response:', response.data)
        const data = response.data
        logs.value = data.items
        pagination.total = data.total
    } catch (error) {
        console.error('Error fetching logs:', error)
        message.error('Failed to fetch logs')
    } finally {
        loading.value = false
    }
}

const handleTableChange = (pag, filters, sorter) => {
    pagination.current = pag.current
    pagination.pageSize = pag.pageSize
    fetchLogs()
}

const onSearch = () => {
    console.log('Search triggered with text:', searchText.value);
    fetchLogs();
}

const onUserIdChange = (value) => {
    console.log('User ID changed to:', value);
    userId.value = value;
    fetchLogs();
}

const onOrgIdChange = (value) => {
    console.log('Org ID changed to:', value);
    organizationId.value = value;
    fetchLogs();
}

const onLogTypeChange = (value) => {
    console.log('Log type changed to:', value);
    logType.value = value;
    fetchLogs();
}

onMounted(fetchLogs)
</script>

<style scoped>
.mb-20 {
    margin-bottom: 20px;
}

.search-card {
    margin-bottom: 24px;
    background: #fff;
    border-radius: 8px;
}

.search-space {
    margin-bottom: 24px;
}

.log-table {
    margin-top: 16px;
}

.table-row-striped td {
    background: #fafafa !important;
}

.details-text {
    margin-bottom: 0;
    line-height: 1.5;
}

:deep(.ant-table) {
    border-radius: 8px;
}

:deep(.ant-card-body) {
    padding: 24px;
}

:deep(.ant-tag) {
    border-radius: 4px;
}

:deep(.ant-input-number) {
    border-radius: 4px;
}

:deep(.ant-select:not(.ant-select-customize-input) .ant-select-selector) {
    border-radius: 4px;
}

:deep(.ant-input-search .ant-input) {
    border-radius: 4px;
}

:deep(.ant-picker) {
    border-radius: 4px;
}
</style>