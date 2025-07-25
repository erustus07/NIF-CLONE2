<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

// Define props for the component
const props = defineProps({
  images: {
    type: Array, // Expects an array of image objects: [{ src: 'url', alt: 'description' }]
    required: true,
    default: () => []
  },
  interval: {
    type: Number, // Time in milliseconds between slides
    default: 5000 // Default to 5 seconds
  }
});

// Reactive state for the current slide index
const currentIndex = ref(0);
// Variable to hold the interval ID for auto-play
let carouselInterval = null;

// Function to move to the next slide
const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % props.images.length;
};

// Function to move to the previous slide
const prevSlide = () => {
  currentIndex.value = (currentIndex.value - 1 + props.images.length) % props.images.length;
};

// Function to jump to a specific slide
const goToSlide = (index) => {
  currentIndex.value = index;
};

// Function to start the auto-play carousel
const startCarousel = () => {
  if (props.images.length > 1 && props.interval > 0) {
    carouselInterval = setInterval(nextSlide, props.interval);
  }
};

// Function to stop the auto-play carousel
const stopCarousel = () => {
  if (carouselInterval) {
    clearInterval(carouselInterval);
  }
};

// Lifecycle hook: When the component is mounted to the DOM
onMounted(() => {
  startCarousel(); // Start auto-play
});

// Lifecycle hook: When the component is unmounted from the DOM
onUnmounted(() => {
  stopCarousel(); // Stop auto-play to prevent memory leaks
});
</script>

<template>
  <div v-if="images.length > 0" class="relative w-full overflow-hidden rounded-lg shadow-xl">
    <!-- Image Display Area -->
    <div class="relative h-64 md:h-96">
      <!-- Transition group for smooth slide changes -->
      <transition-group name="slide-fade" tag="div">
        <img v-for="(image, index) in images" :key="index"
             :src="image.src" :alt="image.alt"
             v-show="currentIndex === index"
             class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700 ease-in-out">
      </transition-group>
    </div>

    <!-- Navigation Buttons (Previous/Next) -->
    <button @click="prevSlide"
            class="absolute top-1/2 left-4 transform -translate-y-1/2 bg-black bg-opacity-50 text-white p-2 rounded-full hover:bg-opacity-75 focus:outline-none transition-colors duration-200">
      &lt;
    </button>
    <button @click="nextSlide"
            class="absolute top-1/2 right-4 transform -translate-y-1/2 bg-black bg-opacity-50 text-white p-2 rounded-full hover:bg-opacity-75 focus:outline-none transition-colors duration-200">
      &gt;
    </button>

    <!-- Indicators (Dots at the bottom) -->
    <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
      <span v-for="(image, index) in images" :key="index"
            @click="goToSlide(index)"
            :class="['block w-3 h-3 rounded-full cursor-pointer transition-colors duration-200', currentIndex === index ? 'bg-white' : 'bg-gray-400 bg-opacity-70']">
      </span>
    </div>
  </div>

  <div v-else class="text-center p-8 text-gray-500 bg-gray-100 rounded-lg shadow-md">
    No images available for carousel.
  </div>
</template>

<style scoped>
/* CSS for fade transition */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: opacity 0.7s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
}
</style>