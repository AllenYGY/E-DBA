<template>
  <a-card title="Service Configuration" :bordered="false">
    <a-table
      :data-source="services"
      :loading="servicesLoading"
      rowKey="id"
      :pagination="{ pageSize: 10 }"
    >
      <template #expandedRowRender="{ record }">
        <a-descriptions bordered column="1" size="small">
          <a-descriptions-item label="API Configuration">
            <div>Base URL: {{ record.base_url || '-' }}</div>
            <div>API Path: {{ record.api_path || '-' }}</div>
            <div>Request Method: {{ record.api_method || '-' }}</div>
          </a-descriptions-item>
          <a-descriptions-item label="Input Format">
            <pre style="margin: 0; white-space: pre-wrap;">{{ record.input_format ? JSON.stringify(record.input_format, null, 2) : '-' }}</pre>
          </a-descriptions-item>
          <a-descriptions-item label="Output Format">
            <pre style="margin: 0; white-space: pre-wrap;">{{ record.output_format ? JSON.stringify(record.output_format, null, 2) : '-' }}</pre>
          </a-descriptions-item>
        </a-descriptions>
      </template>
      <a-table-column title="Service Name" dataIndex="name" key="name" />
      <a-table-column title="Description" dataIndex="description" key="description" />
      <a-table-column title="Status" key="status">
        <template #default="{ record }">
          <a-tag :color="record.is_active ? 'green' : 'red'">
            {{ record.is_active ? 'Running' : 'Stopped' }}
          </a-tag>
        </template>
      </a-table-column>
      <a-table-column title="Public" key="is_public">
        <template #default="{ record }">
          <a-tag :color="record.is_public ? 'blue' : 'orange'">
            {{ record.is_public ? 'Public' : 'Private' }}
          </a-tag>
        </template>
      </a-table-column>
      <a-table-column title="Fee" key="fee">
        <template #default="{ record }">
          {{ record.fee_per_use }} {{ record.fee_unit }}
        </template>
      </a-table-column>
      <a-table-column title="Service Type" key="service_type">
        <template #default="{ record }">
          {{ record.service_type }}
        </template>
      </a-table-column>
      <a-table-column title="Created Time" dataIndex="created_at" key="created_at" />
      <a-table-column title="Actions" key="actions" width="160px">
        <template #default="{ record }">
          <a @click="showEditServiceModal(record)">Edit</a>
          <a-divider type="vertical" />
          <a @click="showTestServiceModal(record)">Test</a>
        </template>
      </a-table-column>
    </a-table>

    <!-- 编辑服务弹窗 -->
    <a-modal
      :open="serviceModalVisible"
      @update:open="val => serviceModalVisible = val"
      title="Edit Service"
      :confirmLoading="serviceFormLoading"
      @ok="handleServiceModalOk"
      @cancel="() => (serviceModalVisible = false)"
      width="600px"
      destroyOnClose
    >
      <a-form :model="serviceForm" layout="vertical">
        <a-form-item label="Service Name" required>
          <a-input 
            :value="serviceForm.name"
            @update:value="val => serviceForm.name = val"
            placeholder="Please enter the service name" 
          />
        </a-form-item>
        <a-form-item label="Description">
          <a-textarea 
            :value="serviceForm.description"
            @update:value="val => serviceForm.description = val"
            placeholder="Please enter the service description" 
            :rows="4" 
          />
        </a-form-item>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="Status">
              <a-select 
                :value="serviceForm.is_active"
                @update:value="val => serviceForm.is_active = val"
              >
                <a-select-option :value="true">Running</a-select-option>
                <a-select-option :value="false">Stopped</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="Public">
              <a-select 
                :value="serviceForm.is_public"
                @update:value="val => serviceForm.is_public = val"
              >
                <a-select-option :value="true">Yes</a-select-option>
                <a-select-option :value="false">No</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        <a-divider>API Configuration</a-divider>
        <a-form-item label="Base URL" required>
          <a-input 
            :value="serviceForm.base_url"
            @update:value="val => serviceForm.base_url = val"
            placeholder="Please enter the base URL of the API, for example: https://api.example.com" 
          />
        </a-form-item>
        <a-form-item label="API Path" required>
          <a-input 
            :value="serviceForm.api_path"
            @update:value="val => serviceForm.api_path = val"
            placeholder="Please enter the API path, for example: /api/v1/data" 
          >
            <template #addonBefore>/</template>
          </a-input>
        </a-form-item>
        <a-form-item label="Request Method" required>
          <a-select 
            :value="serviceForm.api_method"
            @update:value="val => serviceForm.api_method = val"
            style="width: 100%"
          >
            <a-select-option value="GET">GET</a-select-option>
            <a-select-option value="POST">POST</a-select-option>
            <a-select-option value="PUT">PUT</a-select-option>
            <a-select-option value="DELETE">DELETE</a-select-option>
            <a-select-option value="PATCH">PATCH</a-select-option>
          </a-select>
        </a-form-item>
        <a-divider>Input and Output Format</a-divider>
        <a-form-item label="Input Format (JSON)">
          <a-textarea 
            :value="serviceForm.input_format_str"
            @update:value="val => { serviceForm.input_format_str = val; handleInputFormatChange({ target: { value: val } }); }"
            placeholder="Please enter the JSON definition of the input format, for example:&#10;{&#10;  &quot;name&quot;: &quot;string&quot;,&#10;  &quot;age&quot;: &quot;number&quot;&#10;}"
            :rows="6"
          />
        </a-form-item>
        <a-form-item label="Output Format (JSON)">
          <a-textarea 
            :value="serviceForm.output_format_str"
            @update:value="val => { serviceForm.output_format_str = val; handleOutputFormatChange({ target: { value: val } }); }"
            placeholder="Please enter the JSON definition of the output format, for example:&#10;{&#10;  &quot;result&quot;: &quot;string&quot;,&#10;  &quot;status&quot;: &quot;number&quot;&#10;}"
            :rows="6"
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 测试服务弹窗 -->
    <a-modal
      :open="testModalVisible"
      @update:open="val => testModalVisible = val"
      title="Test Service"
      :confirmLoading="testLoading"
      @ok="handleTestService"
      @cancel="() => (testModalVisible = false)"
      width="600px"
      destroyOnClose
    >
      <template v-if="testService">
        <a-descriptions bordered size="small" :column="1" style="margin-bottom: 16px;">
          <a-descriptions-item label="Service Name">{{ testService.name }}</a-descriptions-item>
          <a-descriptions-item label="API URL">{{ testService.base_url }}{{ testService.api_path }}</a-descriptions-item>
          <a-descriptions-item label="Method">{{ testService.api_method }}</a-descriptions-item>
        </a-descriptions>
        <a-form layout="vertical" :model="testForm">
          <a-form-item
            v-for="(type, key) in testService.input_format"
            :key="key"
            :label="key"
          >
            <a-upload
              v-if="type === 'file'"
              :before-upload="file => { testForm[key] = file; return false; }"
              :file-list="testForm[key] ? [testForm[key]] : []"
              :max-count="1"
              accept="image/*"
            >
              <a-button>Upload</a-button>
            </a-upload>
            <a-input
              v-else
              v-model:value="testForm[key]"
              :placeholder="`Enter ${key}`"
            />
          </a-form-item>
        </a-form>
        <div v-if="testResult" style="margin-top: 16px;">
          <b>Response:</b>
          <a-alert type="success" :message="testResult" show-icon />
        </div>
        <div v-if="testError" style="margin-top: 16px;">
          <b>Error:</b>
          <a-alert type="error" :message="testError" show-icon />
        </div>
        <div v-if="testFileBlob" style="margin-top: 16px;">
          <a-button type="primary" @click="downloadTestFile">Download</a-button>
          <div style="margin-top: 8px;">
            <b>Preview:</b>
            <a-alert
              v-if="testFilePreview"
              type="info"
              :message="testFilePreview"
              show-icon
              style="white-space: pre-wrap;"
            />
          </div>
        </div>
      </template>
      <template v-else>
        <a-empty description="No service selected" />
      </template>
    </a-modal>
  </a-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { servicesApi } from '../../services/api'
import axios from 'axios'

// 服务列表相关
const services = ref([])
const servicesLoading = ref(false)
const serviceModalVisible = ref(false)
const serviceForm = reactive({
  id: null,
  name: '',
  description: '',
  is_active: true,
  is_public: false,
  fee_per_use: 0.0,
  fee_unit: 'RMB',
  base_url: '',
  api_path: '',
  api_method: 'POST',
  input_format: null,
  output_format: null,
  input_format_str: '',  // 用于文本框显示的字符串
  output_format_str: '', // 用于文本框显示的字符串
})
const serviceFormLoading = ref(false)

// 测试服务相关
const testModalVisible = ref(false)
const testService = ref(null)
const testInput = ref('')
const testResult = ref('')
const testError = ref('')
const testLoading = ref(false)
const testForm = reactive({})
const testFileFields = ref([]) // 记录哪些字段是 file
const testFileBlob = ref(null)
const testFileName = ref('downloaded_file')
const testFilePreview = ref('')

// 获取服务列表
const fetchServices = async () => {
  servicesLoading.value = true
  try {
    const res = await servicesApi.getOrganizationServices()
    // 过滤掉 bank_transfer 和 bank_auth 类型的服务
    services.value = res.data.filter(service => 
      service.service_type !== 'bank_transfer' && 
      service.service_type !== 'bank_auth'
    )
  } catch (e) {
    message.error('Failed to get service list')
  } finally {
    servicesLoading.value = false
  }
}

// 处理输入格式变化
const handleInputFormatChange = (e) => {
  try {
    const value = e.target.value
    if (!value) {
      serviceForm.input_format = null
      return
    }
    serviceForm.input_format = JSON.parse(value)
  } catch (error) {
    // 解析失败时不更新 input_format，保持原值
    console.error('Invalid JSON format for input_format:', error)
  }
}

// 处理输出格式变化
const handleOutputFormatChange = (e) => {
  try {
    const value = e.target.value
    if (!value) {
      serviceForm.output_format = null
      return
    }
    serviceForm.output_format = JSON.parse(value)
  } catch (error) {
    // 解析失败时不更新 output_format，保持原值
    console.error('Invalid JSON format for output_format:', error)
  }
}

// 打开编辑服务弹窗
const showEditServiceModal = (record) => {
  Object.assign(serviceForm, {
    id: record.id,
    name: record.name,
    description: record.description,
    is_active: record.is_active,
    is_public: record.is_public,
    fee_per_use: record.fee_per_use,
    fee_unit: record.fee_unit,
    base_url: record.base_url,
    api_path: record.api_path,
    api_method: record.api_method,
    input_format: record.input_format,
    output_format: record.output_format,
    input_format_str: record.input_format ? JSON.stringify(record.input_format, null, 2) : '',
    output_format_str: record.output_format ? JSON.stringify(record.output_format, null, 2) : '',
  })
  serviceModalVisible.value = true
}

// 提交编辑服务
const handleServiceModalOk = async () => {
  // 验证 JSON 格式
  try {
    if (serviceForm.input_format_str) {
      JSON.parse(serviceForm.input_format_str)
    }
    if (serviceForm.output_format_str) {
      JSON.parse(serviceForm.output_format_str)
    }
  } catch (error) {
    message.error('Invalid JSON format for input or output format')
    return
  }

  serviceFormLoading.value = true
  try {
    await servicesApi.updateService(serviceForm.id, {
      name: serviceForm.name,
      description: serviceForm.description,
      is_active: serviceForm.is_active,
      is_public: serviceForm.is_public,
      fee_per_use: serviceForm.fee_per_use,
      fee_unit: serviceForm.fee_unit,
      base_url: serviceForm.base_url,
      api_path: serviceForm.api_path,
      api_method: serviceForm.api_method,
      input_format: serviceForm.input_format,
      output_format: serviceForm.output_format,
    })
    message.success('Service updated successfully')
    serviceModalVisible.value = false
    fetchServices()
  } catch (e) {
    message.error('Update failed')
  } finally {
    serviceFormLoading.value = false
  }
}

const showTestServiceModal = (record) => {
  testService.value = record
  // 清空 testForm
  Object.keys(testForm).forEach(key => delete testForm[key])
  testFileFields.value = []
  if (record.input_format) {
    for (const key in record.input_format) {
      if (record.input_format[key] === 'file') {
        testFileFields.value.push(key)
        // 不主动加 testForm[key]，等用户上传时再加
      } else {
        testForm[key] = ''
      }
    }
  }
  testResult.value = ''
  testError.value = ''
  testFileBlob.value = null
  testFileName.value = 'downloaded_file'
  testModalVisible.value = true
}

const handleTestService = async () => {
  testResult.value = ''
  testError.value = ''
  testFileBlob.value = null
  testFileName.value = 'downloaded_file'
  if (!testService.value) return

  // 判断 testForm 里是否有实际的文件对象
  const hasActualFile = Object.entries(testService.value.input_format || {}).some(
    ([key, type]) => type === 'file' && testForm[key]
  )

  let data
  let headers = {}

  if (hasActualFile) {
    data = new FormData()
    for (const key in testForm) {
      // 只 append 有值的字段（file 字段没选就不传）
      if (
        testForm[key] !== null &&
        testForm[key] !== undefined &&
        testForm[key] !== '' // 空字符串也不传
      ) {
        data.append(key, testForm[key])
      }
    }
  } else {
    data = {}
    for (const key in testForm) {
      data[key] = testForm[key]
    }
    headers['Content-Type'] = 'application/json'
  }

  console.log('data:', data)
  console.log('headers:', headers)

  testLoading.value = true
  try {
    let response
    const isGet = (testService.value.api_method || 'POST').toUpperCase() === 'GET'
    // 先用 responseType: 'blob' 请求
    if (isGet) {
      response = await axios.get(
        testService.value.base_url + testService.value.api_path,
        { params: data, responseType: 'blob', headers }
      )
    } else {
      response = await axios({
        method: testService.value.api_method || 'POST',
        url: testService.value.base_url + testService.value.api_path,
        data,
        headers,
        responseType: 'blob'
      })
    }

    // 检查 Content-Type
    const contentType = response.headers['content-type']
    if (
      contentType &&
      (
        contentType.startsWith('application/octet-stream') ||
        contentType.startsWith('application/pdf') ||
        contentType.startsWith('image/') ||
        contentType.startsWith('application/vnd')
      )
    ) {
      // 是文件
      testFileBlob.value = response.data
      // 尝试从 Content-Disposition 获取文件名
      const disposition = response.headers['content-disposition']
      if (disposition) {
        const match = disposition.match(/filename=\"?([^\";]+)\"?/)
        if (match) testFileName.value = decodeURIComponent(match[1])
      }
      testResult.value = ''
      // 新增：尝试预览文本内容
      previewFileContent(response.data, contentType)
    } else {
      // 不是文件，尝试解析为文本
      const text = await blobToText(response.data)
      try {
        testResult.value = JSON.stringify(JSON.parse(text), null, 2)
      } catch {
        testResult.value = text
      }
      testFileBlob.value = null
    }
  } catch (e) {
    if (e.response && e.response.data) {
      // 尝试解析 blob 错误
      const text = await blobToText(e.response.data)
      testError.value = text
    } else {
      testError.value = e.message || 'Request failed.'
    }
  } finally {
    testLoading.value = false
  }
}

// 辅助函数
function blobToText(blob) {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.readAsText(blob)
  })
}

const downloadTestFile = () => {
  if (!testFileBlob.value) return
  const url = URL.createObjectURL(testFileBlob.value)
  const a = document.createElement('a')
  a.href = url
  a.download = testFileName.value
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

function previewFileContent(blob, contentType) {
  // 只对文本类文件尝试预览
  if (
    contentType.startsWith('text/') ||
    contentType.includes('json') ||
    contentType.includes('csv') ||
    contentType.includes('xml')
  ) {
    const reader = new FileReader()
    reader.onload = () => {
      const text = reader.result
      const lines = text.split('\n')
      if (lines.length > 5) {
        testFilePreview.value = lines.slice(0, 5).join('\n') + '\n...'
      } else {
        testFilePreview.value = text
      }
    }
    reader.readAsText(blob)
  } else {
    testFilePreview.value = '[文件不可预览]'
  }
}

onMounted(() => {
  fetchServices()
})
</script>

<style scoped>
:deep(.ant-card) {
  border-radius: 8px;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03), 
              0 1px 6px -1px rgba(0, 0, 0, 0.02), 
              0 2px 4px 0 rgba(0, 0, 0, 0.02);
}

:deep(.ant-card-body) {
  padding: 24px;
}

:deep(.ant-table) {
  border-radius: 8px;
}

:deep(.ant-table-thead > tr > th) {
  background: #fafafa;
  font-weight: 600;
}

:deep(.ant-table-tbody > tr:hover > td) {
  background: #f5f5f5;
}

:deep(.ant-modal-content) {
  border-radius: 8px;
}

:deep(.ant-modal-header) {
  border-radius: 8px 8px 0 0;
}

:deep(.ant-form-item-label > label) {
  font-weight: 500;
}

:deep(.ant-tag) {
  border-radius: 4px;
  padding: 2px 8px;
  font-weight: 500;
}
</style> 