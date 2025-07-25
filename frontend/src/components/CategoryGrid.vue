<script setup>
import { ref } from 'vue';
import { RouterLink } from 'vue-router'; // For navigation
import axios from 'axios'; // For API calls
import { useNotificationStore } from '../stores/notification'; // For displaying notifications

const notificationStore = useNotificationStore(); // Initialize notification store

const categories = ref([]); // Reactive array to store fetched categories
const loading = ref(true); // Loading state indicator
const error = ref(null); // Error message state

// Function to fetch categories from the backend API
const fetchCategories = async () => {
  loading.value = true; // Set loading to true before fetching
  error.value = null; // Clear any previous errors
  try {
    const response = await axios.get('/categories'); // Make GET request to /categories endpoint
    categories.value = response.data; // Update categories with fetched data
  } catch (err) {
    error.value = 'Failed to load categories.'; // Set error message
    notificationStore.showNotification('Failed to load categories.', 'error'); // Show error toast
    console.error('Error fetching categories:', err); // Log error to console
  } finally {
    loading.value = false; // Set loading to false after fetch completes (success or failure)
  }
};

// Call fetchCategories when the component is first loaded
fetchCategories();
</script>

<template>
  <div v-if="loading" class="text-center text-xl text-blue-600 py-8">Loading categories...</div>
  <div v-else-if="error" class="text-center text-red-500 text-xl py-8">{{ error }}</div>
  <div v-else-if="categories.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <RouterLink v-for="category in categories" :key="category.id"
                :to="{ name: 'Products', query: { category_id: category.id }}"
                class="block bg-white rounded-xl shadow-md p-6 text-center hover:shadow-lg transition-shadow duration-300 transform hover:-translate-y-1">
      <h3 class="text-2xl font-semibold text-blue-700 mb-2">{{ category.name }}</h3>
      <p class="text-gray-600">Explore our {{ category.name.toLowerCase() }} collection.</p>
    </RouterLink>
  </div>
  <div v-else class="text-center text-gray-500 text-lg py-8 bg-gray-100 rounded-lg shadow-md">
    No categories found.
  </div>
</template>