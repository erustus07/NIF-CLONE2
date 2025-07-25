<script setup>
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useCartStore } from '../stores/cart'; // Import cart store
import { useNotificationStore } from '../stores/notification'; // Import notification store

const route = useRoute();
const cartStore = useCartStore();
const notificationStore = useNotificationStore();

const productId = ref(route.params.id);
const product = ref(null);
const loading = ref(true);
const error = ref(null);

const fetchProduct = async (id) => {
  loading.value = true;
  error.value = null;
  try {
    const response = await axios.get(`/products/${id}`);
    product.value = response.data;
  } catch (err) {
    error.value = 'Failed to load product details.';
    notificationStore.showNotification('Failed to load product details.', 'error');
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const handleAddToCart = () => {
  if (product.value) {
    cartStore.addToCart(product.value);
  }
};

// Compute the full image URL
const fullImageUrl = (url) => {
  if (url && url.startsWith('/uploads/')) {
    return `${axios.defaults.baseURL}${url}`;
  }
  return '/src/assets/images/default-product.png'; // Fallback
};

watch(productId, (newId) => {
  if (newId) {
    fetchProduct(newId);
  }
}, { immediate: true });
</script>

<template>
  <div class="container mx-auto p-4">
    <div v-if="loading" class="text-center text-xl text-blue-600">Loading product details...</div>
    <div v-else-if="error" class="text-center text-red-500 text-xl">{{ error }}</div>
    <div v-else-if="product" class="flex flex-col md:flex-row gap-8 bg-white rounded-lg shadow-lg p-8">
      <div class="md:w-1/2 flex justify-center items-center p-4 bg-gray-50 rounded-lg">
        <img :src="fullImageUrl(product.image_url)" :alt="product.name" class="max-w-full max-h-96 object-contain rounded-lg shadow-md">
      </div>
      <div class="md:w-1/2">
        <h1 class="text-4xl font-bold mb-4 text-gray-800">{{ product.name }}</h1>
        <p class="text-gray-700 text-lg mb-6 leading-relaxed">{{ product.description || 'No detailed description available.' }}</p>
        <div class="text-3xl font-bold text-blue-700 mb-6">Ksh {{ product.price.toFixed(2) }}</div>
        <div class="mb-6 text-gray-600">
          <span class="font-semibold">Category:</span> {{ product.category_name || 'N/A' }}
        </div>
        <button @click="handleAddToCart" class="bg-green-500 hover:bg-green-600 text-white px-8 py-4 rounded-lg text-xl font-semibold shadow-md hover:shadow-lg transition-all duration-200">Add to Cart</button>
      </div>
    </div>
    <div v-else class="text-center text-xl text-gray-500">Product not found.</div>
  </div>
</template>