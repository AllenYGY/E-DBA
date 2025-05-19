<template>
  <a-card title="Seek Help" :bordered="false">
    <!-- 新建问题表单 -->
    <a-form :model="form" :rules="rules" ref="formRef" layout="vertical" style="max-width: 600px; margin-bottom: 32px;">
      <a-form-item label="Question Title" name="title">
        <a-input v-model:value="form.title" placeholder="Please enter the question title" />
      </a-form-item>
      <a-form-item label="Question Description" name="description">
        <a-textarea v-model:value="form.description" placeholder="Please describe your question in detail" :rows="4" />
      </a-form-item>
      <a-form-item>
        <a-button type="primary" :loading="submitLoading" @click="handleSubmit">Submit Question</a-button>
      </a-form-item>
    </a-form>

    <!-- 历史问题列表 -->
    <a-table
      :columns="columns"
      :data-source="questionList"
      :loading="loading"
      :pagination="pagination"
      @change="handleTableChange"
      :row-key="record => record.id"
      @expand="onExpand"
      bordered
      size="middle"
      :expandIcon="expandIconRender"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'role'">
          <a-tag :color="getRoleColor(record.role)">
            {{ getRoleName(record.role) }}
          </a-tag>
        </template>
        <template v-else-if="column.key === 'title'">
          <div style="display: flex; align-items: center; gap: 8px;">
            {{ record.title }}
            <star-outlined 
              v-if="questionHasResponse[record.id]" 
              style="color: #faad14; font-size: 16px;" 
              title="This question has been answered"
            />
          </div>
        </template>
      </template>
      <template #expandedRowRender="{ record }">
        <div v-if="responseCache[record.id] && responseCache[record.id].length">
          <a-list :data-source="responseCache[record.id]" bordered>
            <template #renderItem="{ item }">
              <a-list-item>
                <a-avatar style="background-color: #1890ff; margin-right: 12px;">{{ item.responder_id }}</a-avatar>
                <div style="flex:1">
                  <div style="font-weight: 500; margin-bottom: 2px;">{{ item.content }}</div>
                  <div style="color: #888; font-size: 12px;">Time: {{ dayjs(item.created_at).format('YYYY-MM-DD HH:mm:ss') }}</div>
                </div>
              </a-list-item>
            </template>
          </a-list>
        </div>
        <div v-else style="color: #aaa;">No response yet</div>
      </template>
    </a-table>
  </a-card>
</template>

<script setup>
import { ref, reactive, onMounted, h } from 'vue'
import { message } from 'ant-design-vue'
import { StarOutlined } from '@ant-design/icons-vue'
import { helpApi } from '../../services/api'
import dayjs from 'dayjs'

// 角色颜色映射
const getRoleColor = (role) => {
  const colorMap = {
    'T_ADMIN': 'red',
    'E_ADMIN': 'green',
    'SENIOR_E_ADMIN': 'blue',
    'O_CONVENER': 'orange',
    'DATA_USER': 'purple'
  }
  return colorMap[role] || 'default'
}

// 获取角色名称
const getRoleName = (role) => {
  const roleMap = {
    'T_ADMIN': 'T-admin',
    'E_ADMIN': 'E-Admin',
    'SENIOR_E_ADMIN': 'Senior E-Admin',
    'O_CONVENER': 'O-Convener',
    'DATA_USER': 'Data User'
  }
  return roleMap[role] || role
}

const loading = ref(false)
const submitLoading = ref(false)
const formRef = ref(null)
const form = reactive({ title: '', description: '' })
const rules = {
  title: [{ required: true, message: 'Please enter the question title' }],
  description: [{ required: true, message: 'Please enter the question description' }],
}

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
  { title: 'User ID', dataIndex: 'user_id', key: 'user_id', width: 80 },
  { title: 'Question Title', dataIndex: 'title', key: 'title' },
  { title: 'Question Description', dataIndex: 'description', key: 'description' },
  { title: 'Email', dataIndex: 'email', key: 'email' },
  { title: 'Role', dataIndex: 'role', key: 'role' },
  {
    title: 'Created Time',
    dataIndex: 'created_at',
    key: 'created_at',
    customRender: ({ text }) => dayjs(text).format('YYYY-MM-DD HH:mm:ss'),
  },
]

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showTotal: total => `Total ${total} items`,
  showSizeChanger: true,
  pageSizeOptions: ['10', '20', '50', '100'],
  showQuickJumper: true
})
const questionList = ref([])
const responseCache = reactive({})
const questionHasResponse = reactive({})

const fetchQuestions = async () => {
  loading.value = true
  try {
    const res = await helpApi.getQuestions({ skip: (pagination.current - 1) * pagination.pageSize, limit: pagination.pageSize })
    questionList.value = res.data.items
    
    // 获取每个问题的回答状态
    await Promise.all(questionList.value.map(async (question) => {
      try {
        const responseRes = await helpApi.getResponses(question.id)
        questionHasResponse[question.id] = responseRes.data.length > 0
        responseCache[question.id] = responseRes.data
      } catch (e) {
        questionHasResponse[question.id] = false
        responseCache[question.id] = []
      }
    }))
    
    pagination.total = res.data.total
  } catch (e) {
    message.error('Failed to get question list')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  await formRef.value.validate()
  submitLoading.value = true
  try {
    await helpApi.createQuestion({ title: form.title, description: form.description })
    message.success('Question submitted successfully')
    form.title = ''
    form.description = ''
    fetchQuestions()
  } catch (e) {
    message.error('Failed to submit question')
  } finally {
    submitLoading.value = false
  }
}

const handleTableChange = (pag) => {
  if (pagination.current !== pag.current || pagination.pageSize !== pag.pageSize) {
    pagination.current = pag.current
    pagination.pageSize = pag.pageSize
    fetchQuestions()
  }
}

const onExpand = async (expanded, record) => {
  if (expanded && !responseCache[record.id]) {
    try {
      const res = await helpApi.getResponses(record.id)
      responseCache[record.id] = res.data
    } catch (e) {
      responseCache[record.id] = []
    }
  }
}

const expandIconRender = ({ expanded, onExpand, record }) => {
  return h(
    'span',
    {
      style: {
        cursor: 'pointer',
        color: expanded ? '#1890ff' : '#bfbfbf',
        fontSize: '18px',
        marginRight: '8px',
        display: 'inline-block',
        transition: 'color 0.2s'
      },
      onClick: e => onExpand(record, e)
    },
    [
      h(
        'svg',
        {
          viewBox: '0 0 1024 1024',
          width: '1em',
          height: '1em',
          fill: 'currentColor'
        },
        [
          h('path', {
            d: 'M512 624c-8.2 0-16.4-3.1-22.6-9.4L246.6 372.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L512 547.7l220.1-220.4c12.5-12.5 32.8-12.5 45.3 0s12.5 32.8 0 45.3L534.6 614.6c-6.2 6.2-14.4 9.4-22.6 9.4z'
          })
        ]
      )
    ]
  )
}

onMounted(() => {
  fetchQuestions()
})
</script>

<style scoped>
.a-card {
  min-width: 320px;
}
</style> 