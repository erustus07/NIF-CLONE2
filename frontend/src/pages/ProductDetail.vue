<script setup>
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useCartStore } from '../stores/cart';
import { useNotificationStore } from '../stores/notification';

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
    console.error('Error fetching product:', err);
  } finally {
    loading.value = false;
  }
};

const handleAddToCart = () => {
  if (product.value) {
    cartStore.addToCart(product.value);
  }
};

const fullImageUrl = (url) => {
  if (url && url.startsWith('/uploads/')) {
    return `${axios.defaults.baseURL}${url}`;
  }
  return '/src/assets/images/default-product.png';
};

watch(productId, (newId) => {
  if (newId) {
    fetchProduct(newId);
  }
}, { immediate: true });
</script>

<template>
  <div class="container mx-auto p-4 py-12">
    <div v-if="loading" class="text-center text-xl text-blue-600 py-8">
      Loading product details...
    </div>

    <div v-else-if="error" class="text-center text-red-500 text-xl py-8">
      {{ error }}
    </div>

    <div v-else-if="product" class="flex flex-col md:flex-row gap-8 bg-white rounded-lg shadow-lg p-8">
      <!-- Product Image Section -->
      <div class="md:w-1/2 flex justify-center items-center p-4 bg-gray-50 rounded-lg border border-gray-100">
        <img :src="fullImageUrl(product.image_url)" :alt="product.name" class="max-w-full max-h-96 object-contain rounded-lg shadow-md">
      </div>

      <!-- Product Details Section -->
      <div class="md:w-1/2">
        <h1 class="text-4xl font-bold mb-4 text-gray-800">{{ product.name }}</h1>
        <p class="text-gray-700 text-lg mb-6 leading-relaxed">
          {{ product.description || 'No detailed description available.' }}
        </p>
        <p class="text-2xl text-green-600 font-semibold mb-6">${{ product.price }}</p>
        <button @click="handleAddToCart" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded shadow">
          Add to Cart
        </button>
      </div>
    </div>
  </div>
</template>
