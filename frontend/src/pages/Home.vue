<script setup>
import { ref } from 'vue';
import ProductCard from '../components/ProductCard.vue';
import Carousel from '../components/Carousel.vue';
import CategoryGrid from '../components/CategoryGrid.vue';
import axios from 'axios';

const featuredProducts = ref([]);
const heroImages = ref([
  { src: '/src/assets/images/hero-laptop.png', alt: 'Powerful Laptops' },
  { src: '/src/assets/images/hero-phone.png', alt: 'Latest Smartphones' },
  { src: '/src/assets/images/hero-tv.png', alt: 'High Definition TVs' }
]);
const promotionalBanners = ref([
  { src: '/src/assets/images/banner1.png', alt: 'Sale on Electronics', link: '/products?sale=true' },
  { src: '/src/assets/images/banner2.png', alt: 'New Arrivals', link: '/products?new=true' }
]);

const fetchFeaturedProducts = async () => {
  try {
    const response = await axios.get('/products');
    // For featured, let's just take the first few or randomize
    featuredProducts.value = response.data.slice(0, 4);
  } catch (error) {
    console.error('Error fetching featured products:', error);
  }
};

fetchFeaturedProducts();
</script>

<template>
  <div class="container mx-auto p-4">
    <!-- Hero Section with Carousel -->
    <section class="mb-12">
      <h1 class="text-5xl font-extrabold text-center mb-8 text-gray-800">Welcome to NIFTAZ AFRICA ELECTRONICS</h1>
      <Carousel :images="heroImages" :interval="4000" />
    </section>

    <!-- Featured Categories -->
    <section class="mb-12">
      <h2 class="text-4xl font-bold text-center mb-8 text-gray-800">Explore Our Categories</h2>
      <CategoryGrid />
    </section>

    <!-- Featured Products -->
    <section class="mb-12">
      <h2 class="text-4xl font-bold text-center mb-8 text-gray-800">Featured Products</h2>
      <div v-if="featuredProducts.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <ProductCard v-for="product in featuredProducts" :key="product.id" :product="product" />
      </div>
      <div v-else class="text-center text-gray-500 text-lg">
        No featured products available.
      </div>
    </section>

    <!-- Promotional Banners -->
    <section class="mb-12 grid grid-cols-1 md:grid-cols-2 gap-6">
      <div v-for="(banner, index) in promotionalBanners" :key="index" class="relative">
        <RouterLink :to="banner.link" class="block rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300">
          <img :src="banner.src" :alt="banner.alt" class="w-full h-auto object-cover">
          <div class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-40 text-white text-2xl font-bold rounded-lg opacity-0 hover:opacity-100 transition-opacity duration-300 p-4">
            {{ banner.alt }}
          </div>
        </RouterLink>
      </div>
    </section>
  </div>
</template>