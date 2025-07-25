<script setup>
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import axios from 'axios';

const categories = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchCategories = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await axios.get('/categories');
    categories.value = response.data;
  } catch (err) {
    error.value = 'Failed to load categories.';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

fetchCategories();
</script>

<template>
  <div v-if="loading" class="text-center text-xl">Loading categories...</div>
  <div v-else-if="error" class="text-center text-red-500 text-xl">{{ error }}</div>
  <div v-else-if="categories.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <RouterLink v-for="category in categories" :key="category.id"
                :to="{ name: 'Products', query: { category_id: category.id }}"
                class="block bg-white rounded-lg shadow-md p-6 text-center hover:shadow-lg transition-shadow duration-300">
      <h3 class="text-2xl font-semibold text-blue-700 mb-2">{{ category.name }}</h3>
      <p class="text-gray-600">Explore our {{ category.name.toLowerCase() }} collection.</p>
    </RouterLink>
  </div>
  <div v-else class="text-center text-gray-500 text-lg">
    No categories found.
  </div>
</template>