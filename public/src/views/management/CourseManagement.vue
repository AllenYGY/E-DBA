<template>
  <div class="course-management">
    <a-tabs :activeKey="activeTab" @update:activeKey="val => activeTab = val">
      <a-tab-pane key="all" tab="All Courses">
        <div style="display: flex; gap: 16px; margin-bottom: 16px;">
          <a-input-search
            :value="searchKeyword"
            @update:value="val => searchKeyword = val"
            placeholder="Search all courses..."
            style="width: 300px;"
            allow-clear
          />
          <a-button type="primary" @click="handleSearch">Search</a-button>
        </div>
        <a-table
          :data-source="allCourses"
          :loading="searchLoading"
          rowKey="id"
          :pagination="{
            current: currentPage,
            pageSize: pageSize,
            total: totalCourses,
            showSizeChanger: true,
            showTotal: (total) => `Total ${total} items`
          }"
          @change="handleTableChange"
        >
          <a-table-column title="Course Name" dataIndex="title" key="title" />
          <a-table-column title="Description" dataIndex="description" key="description" />
          <a-table-column title="Credits" dataIndex="credits" key="credits" />
          <a-table-column title="Public" key="is_public">
            <template #default="{ record }">
              <a-tag :color="record.is_public ? 'green' : 'orange'">
                {{ record.is_public ? 'Yes' : 'No' }}
              </a-tag>
            </template>
          </a-table-column>
          <a-table-column title="Organization" dataIndex="organization_name" key="organization_name" />
          <a-table-column title="Created By" dataIndex="created_by" key="created_by" />
          <a-table-column title="Created At" key="created_at">
            <template #default="{ record }">
              {{ record.created_at ? new Date(record.created_at).toLocaleString() : '' }}
            </template>
          </a-table-column>
          <a-table-column title="Updated At" key="updated_at">
            <template #default="{ record }">
              {{ record.updated_at ? new Date(record.updated_at).toLocaleString() : '' }}
            </template>
          </a-table-column>
        </a-table>
      </a-tab-pane>
      <a-tab-pane
        v-if="permissionLevel === 3 && Number(organizationId) === activeOrganizationId"
        key="my"
        tab="My Courses"
      >
        <div style="margin-bottom: 16px;">
          <a-button type="primary" @click="showAddCourseModal">
            Add Course
          </a-button>
        </div>
        <a-table
          :data-source="myCourses"
          :loading="myCoursesLoading"
          rowKey="id"
          :pagination="{ pageSize: 10 }"
        >
          <a-table-column title="Course Name" dataIndex="title" key="title" />
          <a-table-column title="Description" dataIndex="description" key="description" />
          <a-table-column title="Credits" dataIndex="credits" key="credits" />
          <a-table-column title="Public" key="is_public">
            <template #default="{ record }">
              <a-tag :color="record.is_public ? 'green' : 'orange'">
                {{ record.is_public ? 'Yes' : 'No' }}
              </a-tag>
            </template>
          </a-table-column>
          <a-table-column title="Actions" key="actions">
            <template #default="{ record }">
              <a @click="showEditCourseModal(record)">Edit</a>
              <a-divider type="vertical" />
              <a-popconfirm 
                title="Are you sure to delete this course?" 
                @confirm="handleDeleteCourse(record)"
              >
                <a style="color: red;">Delete</a>
              </a-popconfirm>
            </template>
          </a-table-column>
        </a-table>
      </a-tab-pane>
    </a-tabs>

    <!-- Course Form Modal -->
    <a-modal 
      :open="courseModalVisible" 
      @update:open="val => courseModalVisible = val"
      :title="courseModalType === 'add' ? 'Add Course' : 'Edit Course'" 
      :confirmLoading="courseFormLoading"
      @ok="handleCourseModalOk" 
      @cancel="() => (courseModalVisible = false)" 
      destroyOnClose
    >
      <a-form :model="courseForm" layout="vertical">
        <a-form-item label="Course Name" required>
          <a-input 
            :value="courseForm.title"
            @update:value="val => courseForm.title = val"
            placeholder="Please enter the course name" 
          />
        </a-form-item>
        <a-form-item label="Description">
          <a-input 
            :value="courseForm.description"
            @update:value="val => courseForm.description = val"
            placeholder="Please enter the description" 
          />
        </a-form-item>
        <a-form-item label="Credits" required>
          <a-input-number 
            :value="courseForm.credits"
            @update:value="val => courseForm.credits = val"
            :min="0"
            style="width: 100%;" 
          />
        </a-form-item>
        <a-form-item label="Public">
          <a-switch 
            :checked="courseForm.is_public"
            @update:checked="val => courseForm.is_public = val"
            checked-children="Yes" 
            un-checked-children="No" 
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, reactive } from 'vue'
import { message } from 'ant-design-vue'
import { coursesApi, servicesApi } from '../../services/api'

// Tab and search state
const activeTab = ref('all')
const searchKeyword = ref('')
const searchOrganizationId = ref(null)
const allCourses = ref([])
const totalCourses = ref(0)
const searchLoading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)

// Course form modal state
const courseModalVisible = ref(false)
const courseModalType = ref('add') // 'add' or 'edit'
const courseFormLoading = ref(false)
const courseForm = reactive({
  id: null,
  title: '',
  description: '',
  credits: 0,
  is_public: true,
})

// 新增本地 state
const myCourses = ref([])
const myCoursesLoading = ref(false)

const permissionLevel = Number(localStorage.getItem('permission_level'))
const organizationId = Number(localStorage.getItem('organization_id'))
const activeOrganizationId = Number(localStorage.getItem('active_organization_id'))

// 获取我的课程
const fetchMyCourses = async () => {
  myCoursesLoading.value = true
  try {
    const res = await coursesApi.getMyCourses()
    myCourses.value = Array.isArray(res.data) ? res.data : []
  } catch (e) {
    message.error('Failed to fetch my courses')
    myCourses.value = []
  } finally {
    myCoursesLoading.value = false
  }
}

// 组装搜索参数
function buildSearchParams(keyword, skip, limit) {
  return {
    skip,
    limit,
    organization_id: activeOrganizationId,  // 固定使用 activeOrganizationId
    ...(keyword && keyword.trim() !== '' ? { keyword } : {})
  }
}

// 搜索课程（点击按钮或回车时调用）
const handleSearch = (value) => {
  searchKeyword.value = value
  if (currentPage.value !== 1) {
    currentPage.value = 1
  } else {
    fetchCourses()
  }
}

// 分页变化
const handleTableChange = (pagination) => {
  currentPage.value = pagination.current
  fetchCourses()
}

// 统一的获取课程方法
const fetchCourses = async () => {
  searchLoading.value = true
  try {
    console.log('activeOrganizationId:', activeOrganizationId)
    const serviceRes = await servicesApi.getOrganizationServices({
      organization_id: activeOrganizationId,
    })
    console.log('serviceRes:', serviceRes)  
    const hasCourseSharing = Array.isArray(serviceRes.data)
      ? serviceRes.data.some(s => s.service_type === 'course_sharing')
      : false

    if (!hasCourseSharing) {
      message.warning('This organization does not have Course Sharing service')
      allCourses.value = []
      totalCourses.value = 0
      return
    }

    // 2. 再查课程
    const response = await coursesApi.searchCourses(
      buildSearchParams(
        searchKeyword.value,
        (currentPage.value - 1) * pageSize.value,
        pageSize.value
      )
    )
    allCourses.value = Array.isArray(response.items) ? response.items : []
    totalCourses.value = typeof response.total === 'number' ? response.total : 0
  } catch (error) {
    message.error('Failed to fetch courses')
    allCourses.value = []
    totalCourses.value = 0
  } finally {
    searchLoading.value = false
  }
}
// 打开新增课程弹窗
const showAddCourseModal = () => {
  courseModalType.value = 'add'
  Object.assign(courseForm, {
    id: null,
    title: '',
    description: '',
    credits: 0,
    is_public: true,
  })
  courseModalVisible.value = true
}

// 打开编辑课程弹窗
const showEditCourseModal = (record) => {
  courseModalType.value = 'edit'
  Object.assign(courseForm, record)
  courseModalVisible.value = true
}

// 提交新增/编辑课程
const handleCourseModalOk = async () => {
  courseFormLoading.value = true
  try {
    if (courseModalType.value === 'add') {
      await coursesApi.createCourse({
        title: courseForm.title,
        description: courseForm.description,
        credits: courseForm.credits,
        is_public: courseForm.is_public,
      })
      message.success('Course created successfully')
    } else {
      await coursesApi.updateCourse(courseForm.id, {
        title: courseForm.title,
        description: courseForm.description,
        credits: courseForm.credits,
        is_public: courseForm.is_public,
      })
      message.success('Course updated successfully')
    }
    courseModalVisible.value = false
    // 刷新课程列表
    if (activeTab.value === 'my') {
      fetchMyCourses()
    } else {
      fetchCourses()
    }
  } catch (e) {
    message.error('Operation failed')
  } finally {
    courseFormLoading.value = false
  }
}

// 删除课程
const handleDeleteCourse = async (record) => {
  try {
    await coursesApi.deleteCourse(record.id)
    message.success('Course deleted successfully')
    // 刷新课程列表
    fetchMyCourses()
  } catch (e) {
    message.error('Delete failed')
  }
}

// tab 切换时加载
watch(activeTab, (val) => {
  if (val === 'my') fetchMyCourses()
})

// 组件挂载时加载第一页
onMounted(() => {
  fetchCourses()
})

// 实时搜索 keyword
watch(searchKeyword, () => {
  if (currentPage.value !== 1) {
    currentPage.value = 1
  } else {
    fetchCourses()
  }
})

// 实时搜索 organizationId
watch(searchOrganizationId, () => {
  if (currentPage.value !== 1) {
    currentPage.value = 1
  } else {
    fetchCourses()
  }
})

watch(currentPage, () => {
  fetchCourses()
})
</script>

<style scoped>
.course-management {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.ant-tabs {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.ant-table {
  border-radius: 8px;
  overflow: hidden;
}

@media (max-width: 768px) {
  .course-management {
    gap: 16px;
  }
  .ant-tabs {
    padding: 8px;
  }
}
</style> 