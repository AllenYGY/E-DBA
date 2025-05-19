<template>
  <div class="course-form">
    <h2>Create New Course</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="name">Course Name</label>
        <input 
          type="text" 
          id="name" 
          v-model="form.name" 
          required
        />
      </div>
      
      <div class="form-group">
        <label for="instructor">Instructor</label>
        <input 
          type="text" 
          id="instructor" 
          v-model="form.instructor" 
          required
        />
      </div>
      
      <div class="form-group">
        <label for="credit">Credit</label>
        <input 
          type="number" 
          id="credit" 
          v-model="form.credit" 
          min="1"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="description">Description</label>
        <textarea 
          id="description" 
          v-model="form.description"
        ></textarea>
      </div>
      
      <div class="form-group">
        <label for="department">Department</label>
        <input 
          type="text" 
          id="department" 
          v-model="form.department"
        />
      </div>
      
      <button type="submit" class="submit-btn">
        Create Course
      </button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import { coursesAPI } from '../services/api';

export default {
  setup() {
    const form = ref({
      name: '',
      instructor: '',
      credit: 3,
      description: '',
      department: 'School of Computer Science'
    });

    const handleSubmit = async () => {
      try {
        const response = await coursesAPI.createCourse(form.value);
        alert(`Course created successfully: ${response.data.id}`);
        // Reset form after successful submission
        form.value = {
          name: '',
          instructor: '',
          credit: 3,
          description: '',
          department: 'School of Computer Science'
        };
      } catch (error) {
        console.error('Error creating course:', error);
        alert('Failed to create course');
      }
    };

    return {
      form,
      handleSubmit
    };
  }
};
</script>

<style scoped>
.course-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input, textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

textarea {
  height: 100px;
}

.submit-btn {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #45a049;
}
</style>