<script setup>
import { useCartStore } from '../stores/cart';
import { RouterLink } from 'vue-router';
import axios from 'axios'; // For image URL prefixing

const cartStore = useCartStore();

const updateItemQuantity = (productId, event) => {
  const newQuantity = parseInt(event.target.value, 10);
  cartStore.updateQuantity(productId, newQuantity);
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
  <div class="container mx-auto p-4">
    <h1 class="text-4xl font-bold text-center mb-8 text-gray-800">Your Shopping Cart ({{ cartStore.itemCount }} items)</h1>

    <div v-if="cartStore.items.length === 0" class="text-center text-gray-500 text-lg py-12 bg-white rounded-lg shadow-md">
      Your cart is empty. <RouterLink to="/products" class="text-blue-600 hover:underline font-semibold">Start shopping!</RouterLink>
    </div>

    <div v-else class="bg-white rounded-lg shadow-lg p-6">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantity</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="item in cartStore.items" :key="item.product.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <img :src="fullImageUrl(item.product.image_url)" alt="Product Image" class="w-16 h-16 object-cover rounded-md mr-4 border border-gray-100">
                  <RouterLink :to="{ name: 'ProductDetail', params: { id: item.product.id }}" class="text-blue-600 hover:underline font-medium">
                    {{ item.product.name }}
                  </RouterLink>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">Ksh {{ item.product.price.toFixed(2) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <input type="number" :value="item.quantity" min="1"
                       @change="updateItemQuantity(item.product.id, $event)"
                       class="w-20 border border-gray-300 rounded-md p-1 text-center focus:outline-none focus:ring-2 focus:ring-blue-400">
              </td>
              <td class="px-6 py-4 whitespace-nowrap">Ksh {{ (item.product.price * item.quantity).toFixed(2) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <button @click="cartStore.removeFromCart(item.product.id)"
                        class="text-red-600 hover:text-red-800 font-semibold transition-colors duration-200">Remove</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-8 flex flex-col md:flex-row justify-end items-center space-y-4 md:space-y-0 md:space-x-4">
        <span class="text-3xl font-bold text-gray-800">Total: Ksh {{ cartStore.cartTotal.toFixed(2) }}</span>
        <button @click="cartStore.clearCart()"
                class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-200">Clear Cart</button>
        <button class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-200">Proceed to Checkout</button>
      </div>
    </div>
  </div>
</template>