<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  images: {
    type: Array,
    required: true,
    default: () => []
  },
  interval: {
    type: Number,
    default: 5000 // milliseconds
  }
});

const currentIndex = ref(0);
let carouselInterval = null;

const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % props.images.length;
};

const prevSlide = () => {
  currentIndex.value = (currentIndex.value - 1 + props.images.length) % props.images.length;
};

const goToSlide = (index) => {
  currentIndex.value = index;
};

const startCarousel = () => {
  if (props.images.length > 1 && props.interval > 0) {
    carouselInterval = setInterval(nextSlide, props.interval);
  }
};

const stopCarousel = () => {
  if (carouselInterval) {
    clearInterval(carouselInterval);
  }
};

onMounted(() => {
  startCarousel();
});

onUnmounted(() => {
  stopCarousel();
});
</script>

<template>
  <div v-if="images.length > 0" class="relative w-full overflow-hidden rounded-lg shadow-xl">
    <div class="relative h-64 md:h-96">
      <transition-group name="slide-fade" tag="div">
        <img v-for="(image, index) in images" :key="index"
             :src="image.src" :alt="image.alt"
             v-show="currentIndex === index"
             class="absolute inset-0 w-full h-full object-cover transition-opacity duration-700 ease-in-out">
      </transition-group>
    </div>

    <button @click="prevSlide"
            class="absolute top-1/2 left-4 transform -translate-y-1/2 bg-black bg-opacity-50 text-white p-2 rounded-full hover:bg-opacity-75 focus:outline-none">
      &lt;
    </button>
    <button @click="nextSlide"
            class="absolute top-1/2 right-4 transform -translate-y-1/2 bg-black bg-opacity-50 text-white p-2 rounded-full hover:bg-opacity-75 focus:outline-none">
      &gt;
    </button>

    <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
      <span v-for="(image, index) in images" :key="index"
            @click="goToSlide(index)"
            :class="['block w-3 h-3 rounded-full cursor-pointer', currentIndex === index ? 'bg-white' : 'bg-gray-400 bg-opacity-70']">
      </span>
    </div>
  </div>

  <div v-else class="text-center p-8 text-gray-500">
    No images available for carousel.
  </div>
</template>

<style scoped>
/* Fade transition for images */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: opacity 0.7s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
}
</style>