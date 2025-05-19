<template>
  <a-tabs v-model="activeTab">
    <a-tab-pane key="course" tab="Course Management">
      <CourseManagement :organization-id="organizationId" />
    </a-tab-pane>
    <a-tab-pane
      v-if="permissionLevel >= 2"
      key="student"
      tab="Student Services"
    >
      <StudentServices :organization-id="organizationId" />
    </a-tab-pane>
    <a-tab-pane key="thesis" tab="Thesis Management">
      <ThesisService :organization-id="organizationId" />
    </a-tab-pane>
    <a-tab-pane
      v-if="permissionLevel === 3 && Number(organizationId) === activeOrganizationId"
      key="service"
      tab="Service Management"
    >
      <ServiceConfiguration :organization-id="organizationId" />
    </a-tab-pane>
  </a-tabs>
</template>

<script setup>
import { ref } from 'vue'
import CourseManagement from '../management/CourseManagement.vue'
import StudentServices from './StudentServices.vue'
import ThesisService from './ThesisService.vue'
import ServiceConfiguration from '../management/ServiceConfiguration.vue'

const permissionLevel = Number(localStorage.getItem('permission_level'))
const organizationId = Number(localStorage.getItem('organization_id'))
const activeOrganizationId = Number(localStorage.getItem('active_organization_id'))

defineProps({
  organizationId: {
    type: [String, Number],
    required: true
  }
})

const activeTab = ref('course')
</script> 