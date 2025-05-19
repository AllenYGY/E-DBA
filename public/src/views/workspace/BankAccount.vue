<template>
  <div class="bank-account-container">
    <a-card class="bank-account-card" title="Bank Account Information" :bordered="false">
      <div v-if="paymentAccount">
        <a-descriptions bordered :column="1" size="middle" style="margin-bottom: 24px;">
          <a-descriptions-item label="Bank Name">{{ paymentAccount.bank }}</a-descriptions-item>
          <a-descriptions-item label="Account Name">{{ paymentAccount.account_name }}</a-descriptions-item>
          <a-descriptions-item label="Account Number">{{ paymentAccount.account_number }}</a-descriptions-item>
        </a-descriptions>
        <a-collapse v-model:activeKey="collapseActiveKey">
          <a-collapse-panel key="form" header="Modify Bank Information">
            <a-form
              :model="formState"
              name="bankAccount"
              @finish="onFinish"
              @finishFailed="onFinishFailed"
              layout="vertical"
            >
              <a-form-item
                label="Bank Name"
                name="bankName"
                :rules="[{ required: true, message: 'Please enter bank name!' }]"
              >
                <a-input
                  v-model:value="formState.bankName"
                  placeholder="Enter bank name"
                  size="large"
                >
                  <template #prefix>
                    <BankOutlined />
                  </template>
                </a-input>
              </a-form-item>

              <a-form-item
                label="Account Number"
                name="accountNo"
                :rules="[{ required: true, message: 'Please enter account number!' }]"
              >
                <a-input
                  v-model:value="formState.accountNo"
                  placeholder="Enter account number"
                  size="large"
                >
                  <template #prefix>
                    <AccountBookOutlined />
                  </template>
                </a-input>
              </a-form-item>

              <a-form-item
                label="Account Name"
                name="accountName"
                :rules="[{ required: true, message: 'Please enter account name!' }]"
              >
                <a-input
                  v-model:value="formState.accountName"
                  placeholder="Enter account name"
                  size="large"
                >
                  <template #prefix>
                    <UserOutlined />
                  </template>
                </a-input>
              </a-form-item>

              <a-form-item
                label="Password"
                name="password"
                :rules="[{ required: true, message: 'Please enter password!' }]"
              >
                <a-input-password
                  v-model:value="formState.password"
                  placeholder="Enter password"
                  size="large"
                >
                  <template #prefix>
                    <LockOutlined />
                  </template>
                </a-input-password>
              </a-form-item>

              <a-form-item>
                <a-button
                  type="primary"
                  html-type="submit"
                  size="large"
                  :loading="loading"
                  block
                >
                  Submit
                </a-button>
              </a-form-item>
            </a-form>
          </a-collapse-panel>
        </a-collapse>
      </div>
      <div v-else style="margin-bottom: 24px; color: #faad14; text-align: center; font-weight: 500;">
        No bank account information set, please configure
        <div style="margin-top: 16px;">
          <a-form
            :model="formState"
            name="bankAccount"
            @finish="onFinish"
            @finishFailed="onFinishFailed"
            layout="vertical"
          >
            <a-form-item
              label="Bank Name"
              name="bankName"
              :rules="[{ required: true, message: 'Please enter bank name!' }]"
            >
              <a-input
                v-model:value="formState.bankName"
                placeholder="Enter bank name"
                size="large"
              >
                <template #prefix>
                  <BankOutlined />
                </template>
              </a-input>
            </a-form-item>

            <a-form-item
              label="Account Number"
              name="accountNo"
              :rules="[{ required: true, message: 'Please enter account number!' }]"
            >
              <a-input
                v-model:value="formState.accountNo"
                placeholder="Enter account number"
                size="large"
              >
                <template #prefix>
                  <AccountBookOutlined />
                </template>
              </a-input>
            </a-form-item>

            <a-form-item
              label="Account Name"
              name="accountName"
              :rules="[{ required: true, message: 'Please enter account name!' }]"
            >
              <a-input
                v-model:value="formState.accountName"
                placeholder="Enter account name"
                size="large"
              >
                <template #prefix>
                  <UserOutlined />
                </template>
              </a-input>
            </a-form-item>

            <a-form-item
              label="Password"
              name="password"
              :rules="[{ required: true, message: 'Please enter password!' }]"
            >
              <a-input-password
                v-model:value="formState.password"
                placeholder="Enter password"
                size="large"
              >
                <template #prefix>
                  <LockOutlined />
                </template>
              </a-input-password>
            </a-form-item>

            <a-form-item>
              <a-button
                type="primary"
                html-type="submit"
                size="large"
                :loading="loading"
                block
              >
                Submit
              </a-button>
            </a-form-item>
          </a-form>
        </div>
      </div>
    </a-card>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { 
  BankOutlined, 
  AccountBookOutlined, 
  UserOutlined, 
  LockOutlined 
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { bankApi } from '../../services/api'

const loading = ref(false)
const paymentAccount = ref(null)
const collapseActiveKey = ref([])

const formState = reactive({
  bankName: '',
  accountNo: '',
  accountName: '',
  password: ''
})

const fetchPaymentAccount = async () => {
  try {
    const res = await bankApi.getPaymentAccount()
    paymentAccount.value = res.data
  } catch (error) {
    paymentAccount.value = null
  }
}

onMounted(() => {
  fetchPaymentAccount()
})

const onFinish = async () => {
  loading.value = true
  try {
    await bankApi.updateBankAccount({
      bank: formState.bankName,
      account_number: formState.accountNo,
      account_name: formState.accountName,
      password: formState.password
    })
    message.success('Bank account information saved successfully')
    fetchPaymentAccount()
  } catch (error) {
    console.error('Failed to save bank account:', error)
    message.error(error.response?.data?.detail || 'Failed to save bank account information')
  } finally {
    loading.value = false
  }
}

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo)
  message.error('Please check your input and try again')
}
</script>

<style scoped>
.bank-account-container {
  padding: 24px;
  min-height: 100%;
  background: #f0f2f5;
}

.bank-account-card {
  max-width: 800px;
  margin: 0 auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.bank-account-card :deep(.ant-card-head) {
  border-bottom: 1px solid #f0f0f0;
}

.bank-account-card :deep(.ant-card-head-title) {
  font-size: 18px;
  font-weight: 600;
  color: #1f1f1f;
}

.bank-account-card :deep(.ant-form-item-label) {
  font-weight: 500;
}

.bank-account-card :deep(.ant-input-affix-wrapper) {
  border-radius: 6px;
}

.bank-account-card :deep(.ant-input-affix-wrapper:hover) {
  border-color: #40a9ff;
}

.bank-account-card :deep(.ant-input-affix-wrapper-focused) {
  border-color: #40a9ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.bank-account-card :deep(.ant-btn-primary) {
  height: 40px;
  border-radius: 6px;
  font-weight: 500;
  background: linear-gradient(90deg, #1890ff 0%, #40a9ff 100%);
  border: none;
  transition: all 0.3s;
}

.bank-account-card :deep(.ant-btn-primary:hover) {
  background: linear-gradient(90deg, #40a9ff 0%, #1890ff 100%);
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
}
</style>
