import './assets/css/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import { createPinia } from 'pinia'

axios.defaults.baseURL = 'http://127.0.0.1:5000'

const app = createApp(App)
const pinia = createPinia()

app.use(router)
app.use(pinia) // Use Pinia
app.mount('#app')

// Make axios available globally (optional, for convenience in components)
app.config.globalProperties.$axios = axios