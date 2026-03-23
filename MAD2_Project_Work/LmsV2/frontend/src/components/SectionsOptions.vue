<template>
  <div><br>
    <div class="d-flex flex-row">
      <table class="table table-striped container" style="text-align: center; max-height: 150px; overflow: auto;">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Section</th>
            <th scope="col">Description / Book ID's</th>
            <th scope="col">Creation Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(section, index) in sections" :key="index">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ section.sect_name }}</td>
            <td>
              <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" @click="toggleDropdown(index)">
                  Click Me
                </button>
                <div :id="'dropdown-menu-' + index" class="dropdown-menu" :class="{ show: dropdowns[index] }">
                  <p class="dropdown-item"><strong>Description:</strong> {{ section.sect_desc }}</p>
                  <p class="dropdown-item"><strong>Book IDs:</strong> {{ section.books_ids.join(', ') }}</p>
                </div>
              </div>
            </td>
            <td>{{ section.create_date }}</td>
          </tr>
        </tbody>
      </table>

  <!-- SIDE BAR -->
  <div class="d-flex flex-column flex-shrink-0 p-3 bg-light" style="max-width: 250px; height: 330px;">
        <a href="#" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-dark text-decoration-none">
          <svg class="bi me-2" width="40" height="32"><use xlink:href="#bootstrap"></use></svg>
          <span class="fs-4">Menu</span>
        </a>
        <hr>
        <ul class="nav nav-pills flex-column mb-auto">
          <li class="nav-item">
            <router-link :to="`/admin_home`" class="nav-link link-dark">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#home"></use></svg>
              Home
            </router-link>
          </li>
          <li>
            <router-link :to="`/GotoLibrary`" class="nav-link link-dark">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#speedometer2"></use></svg>
              GoTo Library
            </router-link>
          </li>
          <li>
            <a href="#" class="nav-link active" aria-current="page">              
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#speedometer2"></use></svg>
              Sections Options
            </a>
          </li>
          <li>
            <router-link :to="`/PendingReturns`" class="nav-link link-dark">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#table"></use></svg>
              Pending Returns
            </router-link>
          </li>
          <li>
            <router-link :to="`/StatisticsHome`" class="nav-link link-dark">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#grid"></use></svg>
              Statistics
            </router-link>
          </li>
          <li>
            <a @click.prevent="logout" href="#" class="nav-link link-dark">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#people-circle"></use></svg>
              Sign Out
            </a>
          </li>
        </ul>
        <hr>
      </div>
    </div>

    <ul class="nav nav-pills nav-fill container">
      <li class="nav-item">
        <button class="btn btn-warning" @click="showForm('add')">Add</button>
      </li>
      <li class="nav-item">
        <button class="btn btn-warning" @click="showForm('update')">Update</button>
      </li>
      <li class="nav-item">
        <button class="btn btn-warning" @click="showForm('delete')">Delete</button>
      </li>
    </ul><br>
    <div v-if="formType === 'add'" class="form-container">
      <h3 class="err_msg">Add Section</h3>
      <form @submit.prevent="addSection">
        <div class="form-group">
          <label for="sectionName"><b>Section Name</b></label>
          <input type="text" v-model="form.sectionName" required>
        </div>
        <div class="form-group">
          <label for="sectionDesc"><b>Section Description</b></label>
          <input type="text" v-model="form.sectionDesc" required>
        </div><br>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
    <div v-if="formType === 'update'" class="form-container">
      <h3 class="err_msg">Update Section</h3>
      <form @submit.prevent="updateSection">
        <div class="form-group">
          <label for="sectionSelect"><b>Select Section</b></label>
          <select v-model="form.selectedSection" required>
            <option v-for="section in sections" :key="section.sect_name" :value="section">
              {{ section.sect_name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="sectionName"><b>Section Name</b></label>
          <input type="text" v-model="form.sectionName" required>
        </div>
        <div class="form-group">
          <label for="sectionDesc"><b>Section Description</b></label>
          <input type="text" v-model="form.sectionDesc" required>
        </div><br>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
    <div v-if="formType === 'delete'" class="form-container">
      <h3 class="err_msg">Delete Section</h3>
      <form @submit.prevent="deleteSection">
        <div class="form-group">
          <label for="sectionSelect"><b>Select Section</b></label>
          <select v-model="form.selectedSection" required>
            <option v-for="section in sections" :key="section.sect_name" :value="section">
              {{ section.sect_name }}
            </option>
          </select>
        </div>
        <button type="submit" class="btn btn-danger">Delete</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from '../axiosConfig';
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'SectionsOptions',
  setup() {
    const sections = ref([]);
    const dropdowns = reactive({});
    const router = useRouter();
    const formType = ref('');
    const form = reactive({
      sectionName: '',
      sectionDesc: '',
      selectedSection: null
    });

    const fetchSections = async () => {
      try {
        const response = await axios.get('/getSectionDetails');
        sections.value = response.data;
        response.data.forEach((_, index) => {
          dropdowns[index] = false;
        });
      } catch (error) {
        console.error("There is an error fetching Sections", error);
      }
    };

    const toggleDropdown = (index) => {
      dropdowns[index] = !dropdowns[index];
    };

    const showForm = (type) => {
      formType.value = type;
      form.sectionName = '';
      form.sectionDesc = '';
      form.selectedSection = null;
    };

    const addSection = async () => {
      try {
        await axios.post('/addSection', {
          section_name: form.sectionName,
          section_description: form.sectionDesc
        });
        alert('New Section added successfully');
        fetchSections();
        formType.value = '';
      } catch (error) {
        alert(error.response.data.message);
      }
    };

    const updateSection = async () => {
      try {
        await axios.put(`/updateSection/${form.selectedSection.sect_name}`, {
          section_name: form.sectionName,
          section_description: form.sectionDesc
        });
        alert('Section updated successfully');
        fetchSections();
        formType.value = '';
      } catch (error) {
        alert(error.response.data.message);
      }
    };

    const deleteSection = async () => {
      try {
        await axios.delete(`/deleteSection/${form.selectedSection.sect_name}`);
        alert('Section deleted successfully');
        fetchSections();
        formType.value = '';
      } catch (error) {
        alert(error.response.data.message);
      }
    };

    const logout = () => {
      localStorage.removeItem('adm_token');
      delete axios.defaults.headers.common['Authorization'];
      router.push('/');
    };

    onMounted(() => {
      fetchSections();
    });

    return {
      sections,
      dropdowns,
      formType,
      form,
      logout,
      toggleDropdown,
      showForm,
      addSection,
      updateSection,
      deleteSection
    };
  }
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}
.dropdown-menu {
  display: none;
}
.dropdown-menu.show {
  display: block;
}
.form-group {
  max-width: 300px;
    margin: 0 auto;
    padding: 1em;
    border: 1px solid #ccc;
    border-radius: 10px;
    background-color: #fff;
    justify-content: center;
    text-align: center;
}

</style>
