<script setup>
import { useNotificationStore } from '../stores/notification';
import { computed } from 'vue';

const notificationStore = useNotificationStore();

// Computed property to determine the CSS class based on notification type
const notificationClass = computed(() => {
  switch (notificationStore.type) {
    case 'success':
      return 'bg-green-500'; // Green for success
    case 'error':
      return 'bg-red-500';   // Red for error
    case 'info':
    default:
      return 'bg-blue-500';  // Blue for general info
  }
});
</script>

<template>
  <!-- Transition for fade-in/fade-out effect -->
  <transition name="fade">
    <div v-if="notificationStore.isVisible"
         :class="notificationClass"
         class="fixed bottom-4 right-4 z-50 p-4 rounded-lg shadow-lg text-white text-center min-w-[250px] max-w-sm flex items-center justify-between">
      <p class="flex-grow">{{ notificationStore.message }}</p>
      <!-- Close button -->
      <button @click="notificationStore.hideNotification" class="ml-4 text-white text-lg font-bold leading-none">&times;</button>
    </div>
  </transition>
</template>

<style scoped>
/* CSS for fade transition */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>