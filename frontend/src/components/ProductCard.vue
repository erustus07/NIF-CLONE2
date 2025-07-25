<script setup>
import { RouterLink } from 'vue-router';
import { useCartStore } from '../stores/cart';
import axios from 'axios'; // Import axios to get base URL

const props = defineProps({
  product: Object
});

const cartStore = useCartStore();

const handleAddToCart = () => {
  cartStore.addToCart(props.product);
};

// Compute the full image URL
const fullImageUrl = (url) => {
  if (url && url.startsWith('/uploads/')) {
    return `${axios.defaults.baseURL}${url}`;
  }
  return '/src/assets/images/default-product.png'; // Fallback
};
</script>

<template>
  <div class="border border-gray-200 rounded-xl shadow-lg p-4 m-2 max-w-sm flex flex-col bg-white hover:shadow-xl transition-shadow duration-300">
    <RouterLink :to="{ name: 'ProductDetail', params: { id: product.id }}">
      <img :src="fullImageUrl(product.image_url)" :alt="product.name" class="w-full h-48 object-cover rounded-lg mb-4 border border-gray-100">
      <h3 class="text-xl font-semibold mb-2 text-gray-800 hover:text-blue-600 transition-colors duration-200">{{ product.name }}</h3>
    </RouterLink>
    <p class="text-gray-600 text-sm mb-2 flex-grow">{{ product.description ? product.description.substring(0, 100) + '...' : 'No description.' }}</p>
    <div class="flex justify-between items-center mt-4">
      <span class="text-lg font-bold text-blue-700">Ksh {{ product.price.toFixed(2) }}</span>
      <button @click="handleAddToCart" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg shadow-md hover:shadow-lg transition-all duration-200">Add to Cart</button>
    </div>
  </div>
</template>