<script setup>
import { RouterLink, useRouter } from 'vue-router'; // useRouter for programmatic navigation
import { ref } from 'vue';
import axios from 'axios'; // For fetching categories

const router = useRouter(); // Initialize router instance
const categories = ref([]); // Reactive array for categories in dropdown
const searchTerm = ref(''); // Reactive model for the search input

// Function to fetch categories for the dropdown
const fetchCategories = async () => {
  try {
    const response = await axios.get('/categories');
    categories.value = response.data;
  } catch (error) {
    console.error('Error fetching categories for navbar:', error);
    // Could use notificationStore here if desired
  }
};

// Function to handle search submission
const performSearch = () => {
  if (searchTerm.value.trim()) {
    // Navigate to products page with search query parameter
    router.push({ name: 'Products', query: { search: searchTerm.value.trim() } });
  } else {
    // If search term is empty, navigate to products page without search filter
    router.push({ name: 'Products' });
  }
};

// Fetch categories when the component is mounted
fetchCategories();
</script>

<template>
  <nav class="bg-gray-800 p-4 text-white shadow-md">
    <div class="container mx-auto flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
      <!-- Logo/Home Link -->
      <RouterLink to="/" class="text-3xl font-extrabold text-blue-300 hover:text-blue-200 transition-colors duration-200">NIFTAZ</RouterLink>

      <!-- Navigation Links -->
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
            <!-- Dropdown arrow icon -->
            <svg class="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </button>
          <!-- Dropdown content -->
          <div class="absolute hidden group-hover:block bg-gray-700 text-white p-2 rounded-lg shadow-xl min-w-[160px] top-full left-1/2 -translate-x-1/2 mt-2 z-10">
            <RouterLink v-for="category in categories" :key="category.id"
                        :to="{ name: 'Products', query: { category_id: category.id }}"
                        class="block px-4 py-2 hover:bg-gray-600 rounded-md transition-colors duration-200">
              {{ category.name }}
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Search Bar -->
      <div class="flex items-center w-full md:w-auto">
        <input type="text" v-model="searchTerm" @keyup.enter="performSearch"
               placeholder="Search products..."
               class="p-2 rounded-l-md text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-400 w-full">
        <button @click="performSearch"
                class="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-r-md transition-colors duration-200">
          Search
        </button>
      </div>
    </div>
  </nav>
</template>