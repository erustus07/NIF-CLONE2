<script setup>
import { RouterLink } from 'vue-router';
import { useCartStore } from '../stores/cart'; // Import cart store
import axios from 'axios'; // Import axios to get base URL for images

// Define props: expects a 'product' object
const props = defineProps({
  product: Object
});

const cartStore = useCartStore(); // Initialize cart store

// Function to add the product to the cart
const handleAddToCart = () => {
  cartStore.addToCart(props.product);
};

// Computed property to get the full image URL, handling local uploads and fallbacks
const fullImageUrl = (url) => {
  if (url && url.startsWith('/uploads/')) {
    // If it's an uploaded image, prepend the backend base URL
    return `${axios.defaults.baseURL}${url}`;
  }
  // Fallback to a local placeholder image if no valid URL or not an uploaded image
  return '/src/assets/images/default-product.png';
};
</script>

<template>
  <div class="border border-gray-200 rounded-xl shadow-lg p-4 m-2 max-w-sm flex flex-col bg-white hover:shadow-xl transition-shadow duration-300">
    <!-- Link to Product Detail Page -->
    <RouterLink :to="{ name: 'ProductDetail', params: { id: product.id }}">
      <img :src="fullImageUrl(product.image_url)" :alt="product.name" class="w-full h-48 object-cover rounded-lg mb-4 border border-gray-100">
      <h3 class="text-xl font-semibold mb-2 text-gray-800 hover:text-blue-600 transition-colors duration-200">{{ product.name }}</h3>
    </RouterLink>
    <!-- Product Description (truncated) -->
    <p class="text-gray-600 text-sm mb-2 flex-grow">{{ product.description ? product.description.substring(0, 100) + '...' : 'No description.' }}</p>
    <div class="flex justify-between items-center mt-4">
      <!-- Product Price -->
      <span class="text-lg font-bold text-blue-700">Ksh {{ product.price.toFixed(2) }}</span>
      <!-- Add to Cart Button -->
      <button @click="handleAddToCart" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg shadow-md hover:shadow-lg transition-all duration-200">Add to Cart</button>
    </div>
  </div>
</template>