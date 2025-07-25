import { createRouter, createWebHistory } from 'vue-router'

// Import all page components
import Home from '../pages/Home.vue'
import Products from '../pages/Products.vue'
import ProductDetail from '../pages/ProductDetail.vue'
import About from '../pages/About.vue'
import Contact from '../pages/Contact.vue'
import Cart from '../pages/Cart.vue'
import Admin from '../pages/Admin.vue' // For product and category management

// Define the routes for the application
const routes = [
  {
    path: '/', // The URL path
    name: 'Home', // A unique name for the route
    component: Home // The component to render when this path is active
  },
  {
    path: '/products',
    name: 'Products',
    component: Products
  },
  {
    path: '/products/:id', // Dynamic segment for product ID
    name: 'ProductDetail',
    component: ProductDetail,
    props: true // Pass route params as component props
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/contact',
    name: 'Contact',
    component: Contact
  },
  {
    path: '/cart',
    name: 'Cart',
    component: Cart
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  }
]

// Create the router instance
const router = createRouter({
  history: createWebHistory(), // Use HTML5 History API for clean URLs
  routes // Pass our defined routes
})

export default router // Export the router instance for use in main.js