<template>
  <div class="workspace-container">
    <a-card :bordered="false">
      <!-- 查看其他组织的工作空间时 -->
      <template v-if="activeOrgId && activeOrgId !== currentOrgId">
        <div class="org-header">
          <a-alert
            type="info"
            :message="`Viewing ${getActiveOrgName()}'s Workspace`"
            show-icon
          >
            <template #action>
              <a-button type="link" @click="returnToMyWorkspace">
                Return to My Workspace
              </a-button>
            </template>
          </a-alert>
        </div>
        <WorkspaceServices 
          :key="activeOrgId" 
          :organization-id="activeOrgId" 
        />
      </template>

      <!-- 查看自己的工作空间时 -->
      <template v-else>
        <a-tabs v-model="mainTab">
          <a-tab-pane key="my-org" tab="My Workspace">
            <WorkspaceServices 
              v-if="activeOrgId" 
              :key="activeOrgId" 
              :organization-id="activeOrgId" 
            />
          </a-tab-pane>
          <a-tab-pane key="other-orgs" tab="Other Workspaces">
            <div class="org-cards">
              <a-card
                v-for="org in pagedOrganizations"
                :key="org.id"
                class="org-card"
                :title="org.name"
                hoverable
                @click="showOrgServices(org)"
              >
                <div><b>Email Domain:</b> {{ org.email_domain }}</div>
                <div style="margin: 8px 0;">
                  <a-tag :color="org.is_verified ? 'green' : 'orange'">
                    {{ org.is_verified ? 'Verified' : 'Unverified' }}
                  </a-tag>
                  <a-tag :color="org.is_active ? 'blue' : 'red'">
                    {{ org.is_active ? 'Active' : 'Inactive' }}
                  </a-tag>
                </div>
                <div style="font-size: 12px; color: #888;">ID: {{ org.id }}</div>
              </a-card>
            </div>
            <a-pagination
              :current="orgPagination.current"
              :page-size="orgPagination.pageSize"
              :total="orgPagination.total"
              :show-size-changer="orgPagination.showSizeChanger"
              :page-size-options="orgPagination.pageSizeOptions"
              :show-total="orgPagination.showTotal"
              :show-quick-jumper="orgPagination.showQuickJumper"
              :loading="orgLoading"
              style="margin-top: 24px; text-align: right;"
              @change="handleOrgPageChange"
              @showSizeChange="handleOrgPageSizeChange"
            />
          </a-tab-pane>
        </a-tabs>
      </template>
    </a-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { message } from 'ant-design-vue'
import { usersApi, organizationApi } from '../../services/api'
import WorkspaceServices from '../workspace/WorkspaceServices.vue'

const mainTab = ref('my-org')
const organizations = ref([])
const myOrgId = Number(localStorage.getItem('organization_id'))
const currentOrgId = ref(myOrgId)
const activeOrgId = ref(Number(localStorage.getItem('active_organization_id')) || myOrgId)

const orgLoading = ref(false)
const orgPagination = ref({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showTotal: total => `Total ${total} organizations`,
  showQuickJumper: true,
  pageSizeOptions: ['10', '20', '50', '100']
})

const pagedOrganizations = computed(() => {
  return organizations.value.filter(org => org.id !== currentOrgId.value)
})

const getActiveOrgName = () => {
  const org = organizations.value.find(org => org.id === activeOrgId.value)
  return org ? org.name : 'Unknown Organization'
}

const returnToMyWorkspace = () => {
  activeOrgId.value = myOrgId
  mainTab.value = 'my-org'
  console.log('[Workspace] Return to My Workspace, activeOrgId:', activeOrgId.value)
}

const fetchOrganizations = async (myOrgId) => {
  try {
    orgLoading.value = true
    const params = {
      skip: (orgPagination.value.current - 1) * orgPagination.value.pageSize,
      limit: orgPagination.value.pageSize
    }
    const res = await organizationApi.getOrganizations(params)
    let orgs = res.data
    if (Array.isArray(orgs)) {
      organizations.value = orgs
      orgPagination.value.total = orgs.length
    } else if (orgs.items) {
      organizations.value = orgs.items
      orgPagination.value.total = orgs.total || orgs.items.length
    }
    if (pagedOrganizations.value.length === 0 && orgPagination.value.current > 1) {
      orgPagination.value.current--
      await fetchOrganizations(myOrgId)
    }
    if (orgPagination.value.total > 0 && organizations.value.some(org => org.id === myOrgId)) {
      orgPagination.value.total = orgPagination.value.total - 1
    }
  } catch (e) {
    message.error('Failed to get organizations')
  } finally {
    orgLoading.value = false
  }
}

const handleOrgPageChange = (page) => {
  orgPagination.value.current = page
  fetchOrganizations(currentOrgId.value)
}

const handleOrgPageSizeChange = (current, size) => {
  orgPagination.value.pageSize = size
  orgPagination.value.current = 1
  fetchOrganizations(currentOrgId.value)
}

const showOrgServices = (org) => {
  activeOrgId.value = org.id
  mainTab.value = 'my-org'
  console.log('[Workspace] Show Org Services, clicked org.id:', org.id, 'activeOrgId:', activeOrgId.value)
}

// 监听activeOrgId变化，写入localStorage
watch(activeOrgId, (val) => {
  localStorage.setItem('active_organization_id', val)
  console.log('[Workspace] activeOrgId changed:', val)
})

onMounted(async () => {
  try {
    const userRes = await usersApi.getCurrentUser()
    currentOrgId.value = userRes.data.organization_id
    await fetchOrganizations(currentOrgId.value)
    console.log('[Workspace] onMounted: myOrgId:', myOrgId, 'activeOrgId:', activeOrgId.value, 'currentOrgId:', currentOrgId.value)
  } catch (e) {
    message.error('Failed to load workspace data')
  }
})
</script>

<style scoped>
.workspace-container {
  padding: 24px;
}

.org-header {
  margin-bottom: 16px;
}

.org-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  margin-top: 24px;
}

.org-card {
  width: 260px;
  min-height: 120px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  cursor: pointer;
  transition: all 0.3s ease;
}

.org-card:hover {
  box-shadow: 0 4px 16px rgba(24,144,255,0.18);
  transform: translateY(-2px);
}
</style> 