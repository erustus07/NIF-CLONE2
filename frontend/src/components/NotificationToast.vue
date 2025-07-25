<script setup>
import { useNotificationStore } from '../stores/notification';
import { computed } from 'vue';

const notificationStore = useNotificationStore();

const notificationClass = computed(() => {
  switch (notificationStore.type) {
    case 'success':
      return 'bg-green-500';
    case 'error':
      return 'bg-red-500';
    case 'info':
    default:
      return 'bg-blue-500';
  }
});
</script>

<template>
  <transition name="fade">
    <div v-if="notificationStore.isVisible"
         :class="notificationClass"
         class="fixed bottom-4 right-4 z-50 p-4 rounded-lg shadow-lg text-white text-center min-w-[250px] max-w-sm">
      <p>{{ notificationStore.message }}</p>
      <button @click="notificationStore.hideNotification" class="absolute top-1 right-2 text-white text-lg font-bold">&times;</button>
    </div>
  </transition>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>