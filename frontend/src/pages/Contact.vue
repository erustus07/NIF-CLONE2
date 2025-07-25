<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useNotificationStore } from '../stores/notification';

const notificationStore = useNotificationStore();

const form = ref({
  name: '',
  email: '',
  message: ''
});

const submitForm = async () => {
  // Basic validation
  if (!form.value.name || !form.value.email || !form.value.message) {
    notificationStore.showNotification('Please fill in all fields.', 'error');
    return;
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    notificationStore.showNotification('Please enter a valid email address.', 'error');
    return;
  }

  try {
    await axios.post('/contact', form.value);
    notificationStore.showNotification('Your message has been sent successfully!', 'success');
    // Clear form
    form.value = { name: '', email: '', message: '' };
  } catch (error) {
    console.error('Error sending contact message:', error);
    notificationStore.showNotification('Failed to send message. Please try again later.', 'error');
  }
};
</script>

<template>
  <div class="container mx-auto p-4 max-w-lg">
    <h1 class="text-4xl font-bold text-center mb-8 text-gray-800">Contact Us</h1>
    <form @submit.prevent="submitForm" class="bg-white rounded-lg shadow-lg p-8">
      <div class="mb-4">
        <label for="name" class="block text-gray-700 text-sm font-bold mb-2">Name:</label>
        <input type="text" id="name" v-model="form.name"
               class="form-input"
               required>
      </div>
      <div class="mb-4">
        <label for="email" class="block text-gray-700 text-sm font-bold mb-2">Email:</label>
        <input type="email" id="email" v-model="form.email"
               class="form-input"
               required>
      </div>
      <div class="mb-6">
        <label for="message" class="block text-gray-700 text-sm font-bold mb-2">Message:</label>
        <textarea id="message" v-model="form.message" rows="5"
                  class="form-textarea"
                  required></textarea>
      </div>
      <button type="submit"
              class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg focus:outline-none focus:shadow-outline w-full transition-colors duration-200">
        Send Message
      </button>
    </form>
  </div>
</template>