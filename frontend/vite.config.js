import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  // Optional: If you want to configure the dev server for specific ports or host
  server: {
    port: 5173, // Ensure this matches the port you expect
    // host: '0.0.0.0' // Uncomment if you need to access from other devices on your network
  }
})