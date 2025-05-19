/* eslint-disable vue/no-v-model-argument */
<template>
  <a-card title="Answer Help" :bordered="false">
    <a-table
      :columns="columns"
      :data-source="helpList"
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
              v-if="responseCache[record.id]?.length" 
              style="color: #faad14; font-size: 16px;" 
              title="This question has been answered"
            />
          </div>
        </template>
        <template v-else-if="column.key === 'created_at'">
          {{ dayjs(record.created_at).format('YYYY-MM-DD HH:mm:ss') }}
        </template>
        <template v-else-if="column.key === 'updated_at'">
          {{ dayjs(record.updated_at).format('YYYY-MM-DD HH:mm:ss') }}
        </template>
        <template v-else-if="column.key === 'action'">
          <a-button type="primary" @click="handleAnswer(record)">
            <template #icon><EditOutlined /></template>
            Answer Question
          </a-button>
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

    <!-- 回答问题的模态框 -->
    <a-modal
      :open="modalVisible"
      title="Answer Question"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
      width="600px"
      ok-text="Submit Answer"
      cancel-text="Cancel"
      :bodyStyle="{ paddingBottom: '16px' }"
    >
      <a-form
        :model="formState"
        :rules="rules"
        ref="formRef"
        layout="vertical"
      >
        <a-form-item label="Question Title" name="title">
          <div style="color: #222; font-weight: 500; padding: 6px 0 6px 8px; background: #f7f7f7; border-radius: 4px;">{{ formState.title }}</div>
        </a-form-item>
        <a-form-item label="Question Description" name="description">
          <div style="color: #222; padding: 6px 0 6px 8px; background: #f7f7f7; border-radius: 4px; min-height: 48px;">{{ formState.description }}</div>
        </a-form-item>
        <a-form-item label="Answer" name="answer">
          <a-textarea
            v-model:value="formState.answer"
            placeholder="Please enter your answer..."
            :rows="4"
            style="width: 100%"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </a-card>
</template>

<script setup>
import { ref, reactive, onMounted, h } from 'vue'
import { message } from 'ant-design-vue'
import { EditOutlined, StarOutlined } from '@ant-design/icons-vue'
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
const modalVisible = ref(false)
const formRef = ref(null)
const currentQuestionId = ref(null)
const responseCache = reactive({})
const helpList = ref([])

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
  { title: 'Question Title', dataIndex: 'title', key: 'title' },
  { title: 'Question Description', dataIndex: 'description', key: 'description' },
  { title: 'Questioner Email', dataIndex: 'email', key: 'email' },
  { title: 'Questioner Role', dataIndex: 'role', key: 'role' },
  { title: 'Created Time', dataIndex: 'created_at', key: 'created_at' },
  { title: 'Updated Time', dataIndex: 'updated_at', key: 'updated_at' },
  { title: 'Action', key: 'action', width: 200 },
]

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
})

const formState = reactive({
  title: '',
  description: '',
  answer: '',
})

const rules = {
  answer: [{ required: true, message: 'Please enter your answer' }],
}

// 获取问题列表
const fetchHelpList = async () => {
  loading.value = true
  try {
    const response = await helpApi.getQuestions({
      skip: (pagination.current - 1) * pagination.pageSize,
      limit: pagination.pageSize
    })
    helpList.value = response.data.items
    pagination.total = response.data.total
    // 预加载每个问题的回答
    await Promise.all(helpList.value.map(async (question) => {
      try {
        const res = await helpApi.getResponses(question.id)
        responseCache[question.id] = res.data
      } catch (e) {
        responseCache[question.id] = []
      }
    }))
  } catch (error) {
    message.error('Failed to get question list')
  } finally {
    loading.value = false
  }
}

const handleAnswer = (record) => {
  currentQuestionId.value = record.id
  formState.title = record.title
  formState.description = record.description
  formState.answer = ''
  modalVisible.value = true
}

const handleModalOk = async () => {
  try {
    await formRef.value.validate()
    await helpApi.createResponse(currentQuestionId.value, { content: formState.answer })
    message.success('Answer submitted successfully')
    modalVisible.value = false
    fetchHelpList()
  } catch (error) {
    message.error('Operation failed')
  }
}

const handleModalCancel = () => {
  modalVisible.value = false
}

const handleTableChange = (pag) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchHelpList()
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
  fetchHelpList()
})
</script>

<style scoped>
.a-card {
  min-width: 320px;
}
</style> 