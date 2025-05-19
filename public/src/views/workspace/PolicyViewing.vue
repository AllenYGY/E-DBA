<template>
  <div>
    <a-card title="Policy Viewing" :bordered="false">
      <a-table
        :data-source="policies"
        :loading="policiesLoading"
        rowKey="id"
        :pagination="{ pageSize: 10 }"
      >
        <a-table-column title="Policy Name" dataIndex="title" key="title" />
        <a-table-column title="Description" dataIndex="description" key="description" />
        <a-table-column title="Created Time" dataIndex="created_at" key="created_at" />
        <a-table-column title="Actions" key="actions">
          <template #default="{ record }">
            <a @click="showPolicyDetail(record)">View Details</a>
            <a-divider type="vertical" />
            <a @click="downloadFile(record)">Download</a>
          </template>
        </a-table-column>
      </a-table>
    </a-card>
    <a-modal
      :open="policyDetailVisible"
      @update:open="val => policyDetailVisible = val"
      title="Policy Details"
      :footer="null"
      @cancel="() => (policyDetailVisible = false)"
      width="600px"
    >
      <div v-if="policyDetail">
        <h3>{{ policyDetail.title }}</h3>
        <p><b>Description:</b>{{ policyDetail.description }}</p>
        <p><b>Created Time:</b>{{ policyDetail.created_at }}</p>
        <div v-if="policyDetail.content">
          <b>Content:</b>
          <div style="white-space: pre-wrap;">{{ policyDetail.content }}</div>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { policiesApi } from '../../services/api'

const policies = ref([])
const policiesLoading = ref(false)
const policyDetail = ref(null)
const policyDetailVisible = ref(false)

const fetchPolicies = async () => {
  policiesLoading.value = true
  try {
    const res = await policiesApi.getPolicies()
    policies.value = Array.isArray(res.data) ? res.data : (res.data.items || [])
  } catch (e) {
    message.error('Failed to get policy list')
  } finally {
    policiesLoading.value = false
  }
}

const showPolicyDetail = async (record) => {
  try {
    const res = await policiesApi.getPolicy(record.id)
    policyDetail.value = res.data
    policyDetailVisible.value = true
  } catch (e) {
    message.error('Failed to get policy detail')
  }
}

const downloadFile = async (record) => {
  try {
    const response = await policiesApi.downloadPolicyFile(record.id);
    const blob = response.data;

    // 从Content-Disposition获取文件名
    let filename = `policy_${record.id}.pdf`;
    const contentDisposition = response.headers['content-disposition'];
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['\"]).*?\2|[^;\n]*)/);
      if (filenameMatch && filenameMatch[1]) {
        filename = filenameMatch[1].replace(/['"]/g, '');
      }
    }

    // 创建一个临时下载链接并触发它
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();

    // 清理
    window.URL.revokeObjectURL(downloadUrl);
    document.body.removeChild(link);

    message.success(`Downloading ${filename}`);
  } catch (error) {
    let errorMsg = 'Download failed';
    if (error.response?.data?.detail) {
      errorMsg = error.response.data.detail;
    } else if (error.message) {
      errorMsg = error.message;
    }
    message.error(errorMsg);
    console.error('Download error:', error);
  }
};

onMounted(() => {
  fetchPolicies()
})
</script> 