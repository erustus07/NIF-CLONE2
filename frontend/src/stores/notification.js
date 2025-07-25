// import { defineStore } from 'pinia';

// export const useNotificationStore = defineStore('notification', {
//   state: () => ({
//     message: '',
//     type: '', // 'success', 'error', 'info'
//     isVisible: false,
//     timeoutId: null
//   }),
//   actions: {
//     showNotification(message, type = 'info', duration = 3000) {
//       this.message = message;
//       this.type = type;
//       this.isVisible = true;

//       if (this.timeoutId) {
//         clearTimeout(this.timeoutId);
//       }

//       this.timeoutId = setTimeout(() => {
//         this.hideNotification();
//       }, duration);
//     },
//     hideNotification() {
//       this.isVisible = false;
//       this.message = '';
//       this.type = '';
//       if (this.timeoutId) {
//         clearTimeout(this.timeoutId);
//         this.timeoutId = null;
//       }
//     }
//   }
// });



import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    message: '',        // The message to display
    type: '',           // Type of notification: 'success', 'error', 'info'
    isVisible: false,   // Controls visibility of the toast
    timeoutId: null     // Stores the ID of the setTimeout for clearing
  }),
  actions: {
    showNotification(message, type = 'info', duration = 3000) {
      // Set the notification details
      this.message = message;
      this.type = type;
      this.isVisible = true;

      // Clear any existing timeout to prevent multiple toasts overlapping
      if (this.timeoutId) {
        clearTimeout(this.timeoutId);
      }

      // Set a new timeout to hide the notification after a duration
      this.timeoutId = setTimeout(() => {
        this.hideNotification();
      }, duration);
    },
    hideNotification() {
      // Hide the notification and reset its state
      this.isVisible = false;
      this.message = '';
      this.type = '';
      // Clear the timeout ID
      if (this.timeoutId) {
        clearTimeout(this.timeoutId);
        this.timeoutId = null;
      }
    }
  }
});