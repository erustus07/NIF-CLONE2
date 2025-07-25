import { defineStore } from 'pinia';

export const useCartStore = defineStore('cart', {
  // State: The actual data that the store holds.
  state: () => ({
    items: [] // Array of { product: ProductObject, quantity: Number }
  }),

  // Getters: Computed properties for the store's state.
  getters: {
    cartTotal: (state) => {
      // Calculates the total price of all items in the cart.
      return state.items.reduce((total, item) => total + (item.product.price * item.quantity), 0);
    },
    itemCount: (state) => {
      // Calculates the total number of individual items (units) in the cart.
      return state.items.reduce((count, item) => count + item.quantity, 0);
    }
  },

  // Actions: Methods that can modify the state. They can be asynchronous.
  actions: {
    addToCart(product, quantity = 1) {
      // Check if the product already exists in the cart.
      const existingItem = this.items.find(item => item.product.id === product.id);
      if (existingItem) {
        // If it exists, just increase the quantity.
        existingItem.quantity += quantity;
      } else {
        // If it's a new product, add it to the cart.
        this.items.push({ product, quantity });
      }
      // In a real app, you might use a notification store here.
      // For now, a simple alert.
      alert(`${quantity} x ${product.name} added to cart!`);
    },
    removeFromCart(productId) {
      // Removes an item from the cart based on product ID.
      this.items = this.items.filter(item => item.product.id !== productId);
    },
    updateQuantity(productId, newQuantity) {
      // Updates the quantity of a specific item in the cart.
      const item = this.items.find(item => item.product.id === productId);
      if (item) {
        if (newQuantity <= 0) {
          // If quantity is 0 or less, remove the item.
          this.removeFromCart(productId);
        } else {
          // Otherwise, update the quantity.
          item.quantity = newQuantity;
        }
      }
    },
    clearCart() {
      // Empties the entire cart.
      this.items = [];
    }
  },
});