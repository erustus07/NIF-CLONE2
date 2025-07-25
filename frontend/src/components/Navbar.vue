<script setup>
import { RouterLink, useRouter } from 'vue-router';
import { ref } from 'vue';
import axios from 'axios';

const router = useRouter();
const categories = ref([]);
const searchTerm = ref('');

const fetchCategories = async () => {
  try {
    const response = await axios.get('/categories');
    categories.value = response.data;
  } catch (error) {
    console.error('Error fetching categories:', error);
  }
};

const performSearch = () => {
  if (searchTerm.value.trim()) {
    router.push({ name: 'Products', query: { search: searchTerm.value.trim() } });
  } else {
    router.push({ name: 'Products' }); // Clear search if empty
  }
};

fetchCategories();
</script>

<template>
  <nav class="bg-gray-800 p-4 text-white shadow-md">
    <div class="container mx-auto flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
      <RouterLink to="/" class="text-3xl font-extrabold text-blue-300 hover:text-blue-200 transition-colors duration-200">NIFTAZ</RouterLink>

      <div class="flex flex-col md:flex-row items-center space-y-2 md:space-y-0 md:space-x-6">
        <RouterLink to="/" class="hover:text-blue-300 transition-colors duration-200">Home</RouterLink>
        <RouterLink to="/products" class="hover:text-blue-300 transition-colors duration-200">Products</RouterLink>
        <RouterLink to="/about" class="hover:text-blue-300 transition-colors duration-200">About</RouterLink>
        <RouterLink to="/contact" class="hover:text-blue-300 transition-colors duration-200">Contact</RouterLink>
        <RouterLink to="/cart" class="hover:text-blue-300 transition-colors duration-200">Cart</RouterLink>
        <RouterLink to="/admin" class="hover:text-blue-300 transition-colors duration-200">Admin</RouterLink>

        <!-- Category Dropdown -->
        <div class="relative inline-block group">
          <button class="hover:text-blue-300 transition-colors duration-200 flex items-center">
            Categories
            <svg class="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </button>
          <div class="absolute hidden group-hover:block bg-gray-700 text-white p-2 rounded-lg shadow-xl min-w-[160px] top-full left-1/2 -translate-x-1/2 mt-2">
            <RouterLink v-for="category in categories" :key="category.id"
                        :to="{ name: 'Products', query: { category_id: category.id }}"
                        class="block px-4 py-2 hover:bg-gray-600 rounded-md transition-colors duration-200">
              {{ category.name }}
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Search Bar -->
      <div class="flex items-center">
        <input type="text" v-model="searchTerm" @keyup.enter="performSearch"
               placeholder="Search products..."
               class="p-2 rounded-l-md text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-400">
        <button @click="performSearch"
                class="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-r-md transition-colors duration-200">
          Search
        </button>
      </div>
    </div>
  </nav>
</template>