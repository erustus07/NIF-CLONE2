<script setup>
import { ref, watch } from 'vue';
import ProductCard from '../components/ProductCard.vue';
import axios from 'axios';
import { useRoute } from 'vue-router';

const products = ref([]);
const categories = ref([]);
const loading = ref(true);
const error = ref(null);
const route = useRoute();
const selectedCategoryId = ref(route.query.category_id || null);
const currentSearchTerm = ref(route.query.search || '');

const fetchProducts = async () => {
  loading.value = true;
  error.value = null;
  try {
    let url = '/products';
    const params = {};
    if (selectedCategoryId.value) {
      params.category_id = selectedCategoryId.value;
    }
    if (currentSearchTerm.value) {
      params.search = currentSearchTerm.value;
    }
    const response = await axios.get(url, { params });
    products.value = response.data;
  } catch (err) {
    error.value = 'Failed to load products.';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const fetchCategories = async () => {
  try {
    const response = await axios.get('/categories');
    categories.value = response.data;
  } catch (err) {
    console.error('Error fetching categories:', err);
  }
};

// Watch for changes in query parameters
watch(() => route.query.category_id, (newCategoryId) => {
  selectedCategoryId.value = newCategoryId;
  fetchProducts();
}, { immediate: true }); // Fetch initially on component mount

watch(() => route.query.search, (newSearchTerm) => {
  currentSearchTerm.value = newSearchTerm;
  fetchProducts();
}, { immediate: true }); // Fetch initially on component mount

fetchCategories(); // Fetch categories on component mount
</script>

<template>
  <div class="container mx-auto p-4">
    <h1 class="text-4xl font-bold text-center mb-8">Our Products</h1>

    <!-- Category Filter -->
    <div class="mb-6 flex flex-wrap justify-center gap-4">
      <select v-model="selectedCategoryId" @change="fetchProducts"
              class="border rounded-md p-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400">
        <option :value="null">All Categories</option>
        <option v-for="category in categories" :key="category.id" :value="category.id">
          {{ category.name }}
        </option>
      </select>
    </div>

    <div v-if="loading" class="text-center text-xl text-blue-600">Loading products...</div>
    <div v-else-if="error" class="text-center text-red-500 text-xl">{{ error }}</div>
    <div v-else-if="products.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <ProductCard v-for="product in products" :key="product.id" :product="product" />
    </div>
    <div v-else class="text-center text-gray-500 text-lg">
      No products found matching your criteria.
    </div>
  </div>
</template>