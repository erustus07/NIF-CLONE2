<script setup>
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router'; // To access route parameters
import axios from 'axios'; // For API calls
import { useCartStore } from '../stores/cart'; // For adding to cart
import { useNotificationStore } from '../stores/notification'; // For displaying notifications

const route = useRoute(); // Initialize route instance
const cartStore = useCartStore(); // Initialize cart store
const notificationStore = useNotificationStore(); // Initialize notification store

const productId = ref(route.params.id); // Get product ID from route parameters
const product = ref(null); // Reactive object to hold product details
const loading = ref(true); // Loading state indicator
const error = ref(null); // Error message state

// Function to fetch product details from the backend API
const fetchProduct = async (id) => {
  loading.value = true; // Set loading to true before fetching
  error.value = null; // Clear any previous errors
  try {
    const response = await axios.get(`/products/${id}`); // Make GET request to /products/:id
    product.value = response.data; // Update product with fetched data
  } catch (err) {
    error.value = 'Failed to load product details.'; // Set error message
    notificationStore.showNotification('Failed to load product details.', 'error'); // Show error toast
    console.error('Error fetching product:', err); // Log error to console
  } finally {
    loading.value = false; // Set loading to false after fetch completes
  }
};

// Function to handle adding the product to the cart
const handleAddToCart = () => {
  if (product.value) {
    cartStore.addToCart(product.value); // Call cart store action
  }
};

// Computed property to get the full image URL, handling local uploads and fallbacks
const fullImageUrl = (url) => {
  if (url && url.startsWith('/uploads/')) {
    return `${axios.defaults.baseURL}${url}`;
  }
  return '/src/assets/images/default-product.png'; // Fallback
};

// Watch for changes in the productId route parameter
// This ensures the page updates if the user navigates directly to another product detail page
watch(productId, (newId) => {
  if (newId) {
    fetchProduct(newId); // Fetch product details whenever the ID changes
  }
}, { immediate: true }); // 'immediate: true' fetches data on initial component mount
</script>

<template>
  <div class="container mx-auto p-4 py-12">
    <div v-if="loading" class="text-center text-xl text-blue-600 py-8">Loading product details...</div>
    <div v-else-if="error" class="text-center text-red-500 text-xl py-8">{{ error }}</div>
    <div v-else-if="product" class="flex flex-col md:flex-row gap-8 bg-white rounded-lg shadow-lg p-8">
      <!-- Product Image Section -->
      <div class="md:w-1/2 flex justify-center items-center p-4 bg-gray-50 rounded-lg border border-gray-100">
        <img :src="fullImageUrl(product.image_url)" :alt="product.name" class="max-w-full max-h-96 object-contain rounded-lg shadow-md">
      </div>
      <!-- Product Details Section -->
      <div class="md:w-1/2">
        <h1 class="text-4xl font-bold mb-4 text-gray-800">{{ product.name }}</h1>
        <p class="text-gray-700 text-lg mb-6 leading-relaxed">{{ product.description || 'No detailed description available.' }}</p>