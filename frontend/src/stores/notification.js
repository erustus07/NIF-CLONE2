import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    message: '',
    type: '', // 'success', 'error', 'info'
    isVisible: false,
    timeoutId: null
  }),
  actions: {
    showNotification(message, type = 'info', duration = 3000) {
      this.message = message;
      this.type = type;
      this.isVisible = true;

      if (this.timeoutId) {
        clearTimeout(this.timeoutId);
      }

      this.timeoutId = setTimeout(() => {
        this.hideNotification();
      }, duration);
    },
    hideNotification() {
      this.isVisible = false;
      this.message = '';
      this.type = '';
      if (this.timeoutId) {
        clearTimeout(this.timeoutId);
        this.timeoutId = null;
      }
    }
  }
});