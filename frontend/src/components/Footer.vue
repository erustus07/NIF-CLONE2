<template>
  <footer class="bg-gray-900 text-white p-6 mt-8 shadow-inner">
    <div class="container mx-auto text-center">
      <p class="text-lg mb-2">&copy; {{ new Date().getFullYear() }} NIFTAZ AFRICA ELECTRONICS. All rights reserved.</p>
      <div class="flex justify-center space-x-6 mt-4">
        <a href="#" class="hover:text-blue-400 transition-colors duration-200">Privacy Policy</a>
        <a href="#" class="hover:text-blue-400 transition-colors duration-200">Terms of Service</a>
        <a href="#" class="hover:text-blue-400 transition-colors duration-200">Sitemap</a>
      </div>
      <p class="text-sm text-gray-400 mt-4">Built with Vue 3, Flask, and PostgreSQL</p>
    </div>
  </footer>
</template>