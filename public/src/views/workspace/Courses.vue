<template>
  <div class="courses-container">
    <a-page-header
      title="Course Information"
      sub-title="Search and browse course information"
      class="mb-20"
    />
    
    <a-card>
      <a-form layout="inline" :model="searchForm" @finish="handleSearch" class="mb-20">
        <a-form-item label="Keyword">
          <a-input v-model:value="searchForm.keyword" placeholder="Course Name/ID" allowClear />
        </a-form-item>
        <a-form-item label="Instructor">
          <a-input v-model:value="searchForm.instructor" placeholder="Instructor Name" allowClear />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit" :loading="loading">
            <template #icon><SearchOutlined /></template>
            Search
          </a-button>
          <a-button type="primary" @click="createModalVisible = true" style="margin-left: 8px">
            <template #icon><PlusOutlined /></template>
            Create Course
          </a-button>
        </a-form-item>
      </a-form>
      
      <a-table
        :columns="columns"
        :data-source="courses"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        row-key="id"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <a-button type="link" size="small" @click="viewCourse(record)">
              <template #icon><EyeOutlined /></template>
              View Details
            </a-button>
          </template>
        </template>
      </a-table>
    </a-card>
    
    <!-- Course Details Drawer -->
    <a-drawer
      v-model:visible="drawerVisible"
      :title="drawerTitle"
      :width="640"
      @close="closeDrawer"
    >
      <course-details :course="selectedCourse" />
    </a-drawer>

    <!-- Create Course Modal -->
    <a-modal
      v-model:visible="createModalVisible"
      title="Create New Course"
      :footer="null"
      width="800px"
    >
      <course-form @submit="handleCreateSuccess" />
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { SearchOutlined, EyeOutlined, PlusOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'
import { coursesAPI } from '../../services/api'
import CourseForm from '../../components/CourseForm.vue'

const router = useRouter()
const loading = ref(false)
const drawerVisible = ref(false)
const drawerTitle = ref('Course Details')
const selectedCourse = ref(null)
const createModalVisible = ref(false)

const searchForm = reactive({
  keyword: '',
  instructor: ''
})

const columns = [
  { title: 'Course Name', dataIndex: 'name', key: 'name' },
  { title: 'Course ID', dataIndex: 'id', key: 'id' },
  { title: 'Instructor', dataIndex: 'instructor', key: 'instructor' },
  { title: 'Action', key: 'action', scopedSlots: { customRender: 'action' } }
]

const courses = ref([])
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0
})

const handleSearch = async () => {
  loading.value = true
  try {
    const response = await coursesAPI.searchCourses(searchForm)
    courses.value = response.courses
    pagination.total = response.total
    message.success('Search completed')
  } catch (error) {
    console.error('Search failed:', error)
    message.error('Search failed, please try again later')
  } finally {
    loading.value = false
  }
}

const handleTableChange = (pagination) => {
  pagination.current = pagination.current
  pagination.pageSize = pagination.pageSize
  handleSearch()
}

const viewCourse = (record) => {
  selectedCourse.value = record
  drawerVisible.value = true
}

const closeDrawer = () => {
  drawerVisible.value = false
}

const handleCreateSuccess = () => {
  createModalVisible.value = false
  handleSearch()
  message.success('Course created successfully')
}
</script>

<style scoped>
.courses-container {
  padding: 24px;
}

.courses-container .ant-card {
  margin-bottom: 24px;
}

.courses-container .ant-table {
  margin-top: 24px;
}
</style>