<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useNotificationStore } from '../stores/notification';

const notificationStore = useNotificationStore();

// --- Product Management ---
const products = ref([]);
const newProduct = ref({
  name: '',
  description: '',
  price: 0.0,
  image_url: '', // This will be the URL from backend
  category_id: null,
  image_file: null, // For frontend file object
  image_preview_url: null // For displaying image preview
});
const editingProduct = ref(null); // Stores the product being edited
const editingProductImageFile = ref(null); // File object for editing product
const editingProductImagePreviewUrl = ref(null); // Preview URL for editing product

const fetchProducts = async () => {
  try {
    const response = await axios.get('/products');
    products.value = response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    notificationStore.showNotification('Failed to load products.', 'error');
  }
};

const handleImageFileChange = (event, type = 'new') => {
  const file = event.target.files[0];
  if (file) {
    if (type === 'new') {
      newProduct.value.image_file = file;
      newProduct.value.image_preview_url = URL.createObjectURL(file);
    } else if (type === 'edit') {
      editingProductImageFile.value = file;
      editingProductImagePreviewUrl.value = URL.createObjectURL(file);
    }
  } else {
    if (type === 'new') {
      newProduct.value.image_file = null;
      newProduct.value.image_preview_url = null;
    } else if (type === 'edit') {
      editingProductImageFile.value = null;
      editingProductImagePreviewUrl.value = null;
    }
  }
};

const addProduct = async () => {
  if (!newProduct.value.name || !newProduct.value.price || !newProduct.value.category_id) {
    notificationStore.showNotification('Name, price, and category are required.', 'error');
    return;
  }

  const formData = new FormData();
  formData.append('name', newProduct.value.name);
  formData.append('description', newProduct.value.description || '');
  formData.append('price', newProduct.value.price);
  formData.append('category_id', newProduct.value.category_id);
  if (newProduct.value.image_file) {
    formData.append('image', newProduct.value.image_file);
  }

  try {
    await axios.post('/products', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    notificationStore.showNotification('Product added successfully!', 'success');
    // Clear form and refetch products
    newProduct.value = { name: '', description: '', price: 0.0, image_url: '', category_id: categories.value[0]?.id || null, image_file: null, image_preview_url: null };
    fetchProducts();
  } catch (error) {
    console.error('Error adding product:', error);
    notificationStore.showNotification('Error adding product: ' + (error.response?.data?.error || 'Unknown error'), 'error');
  }
};

const startEditProduct = (product) => {
  editingProduct.value = { ...product }; // Create a copy to edit
  editingProductImageFile.value = null; // Clear file input
  editingProductImagePreviewUrl.value = product.image_url ? `${axios.defaults.baseURL}${product.image_url}` : null;
};

const saveEditProduct = async () => {
  if (!editingProduct.value.name || !editingProduct.value.price || !editingProduct.value.category_id) {
    notificationStore.showNotification('Name, price, and category are required for editing.', 'error');
    return;
  }

  const formData = new FormData();
  formData.append('name', editingProduct.value.name);
  formData.append('description', editingProduct.value.description || '');
  formData.append('price', editingProduct.value.price);
  formData.append('category_id', editingProduct.value.category_id);
  formData.append('current_image_url', editingProduct.value.image_url || ''); // Send current URL for backend to preserve if no new file

  if (editingProductImageFile.value) {
    formData.append('image', editingProductImageFile.value);
  } else if (editingProductImagePreviewUrl.value === null && editingProduct.value.image_url) {
    // If preview cleared and product had an image, it means user wants to remove it
    // Send an empty 'image' field to signal removal
    formData.append('image', new Blob(), ''); // Sending an empty blob with empty filename
  }


  try {
    await axios.put(`/products/${editingProduct.value.id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    notificationStore.showNotification('Product updated successfully!', 'success');
    editingProduct.value = null; // Exit edit mode
    editingProductImageFile.value = null;
    editingProductImagePreviewUrl.value = null;
    fetchProducts();
  } catch (error) {
    console.error('Error updating product:', error);
    notificationStore.showNotification('Error updating product: ' + (error.response?.data?.error || 'Unknown error'), 'error');
  }
};

const cancelEditProduct = () => {
  editingProduct.value = null;
  editingProductImageFile.value = null;
  editingProductImagePreviewUrl.value = null;
};

const deleteProduct = async (id) => {
  if (confirm('Are you sure you want to delete this product?')) {
    try {
      await axios.delete(`/products/${id}`);
      notificationStore.showNotification('Product deleted successfully!', 'success');
      fetchProducts();
    } catch (error) {
      console.error('Error deleting product:', error);
      notificationStore.showNotification('Error deleting product: ' + (error.response?.data?.error || 'Unknown error'), 'error');
    }
  }
};

const removeEditingProductImage = () => {
  editingProductImageFile.value = null;
  editingProductImagePreviewUrl.value = null;
  editingProduct.value.image_url = null; // Mark for removal on save
};


// --- Category Management ---
const categories = ref([]);
const newCategoryName = ref('');
const editingCategory = ref(null);

const fetchCategories = async () => {
  try {
    const response = await axios.get('/categories');
    categories.value = response.data;
    if (categories.value.length > 0 && newProduct.value.category_id === null) {
      newProduct.value.category_id = categories.value[0].id; // Set default category for new product form
    }
  } catch (error) {
    console.error('Error fetching categories:', error);
    notificationStore.showNotification('Failed to load categories.', 'error');
  }
};

const addCategory = async () => {
  if (!newCategoryName.value.trim()) {
    notificationStore.showNotification('Category name cannot be empty.', 'error');
    return;
  }
  try {
    await axios.post('/categories', { name: newCategoryName.value.trim() });
    notificationStore.showNotification('Category added successfully!', 'success');
    newCategoryName.value = '';
    fetchCategories();
  } catch (error) {
    console.error('Error adding category:', error);
    notificationStore.showNotification('Error adding category: ' + (error.response?.data?.error || 'Unknown error'), 'error');
  }
};

const startEditCategory = (category) => {
  editingCategory.value = { ...category };
};

const saveEditCategory = async () => {
  if (!editingCategory.value.name.trim()) {
    notificationStore.showNotification('Category name cannot be empty.', 'error');
    return;
  }
  try {
    await axios.put(`/categories/${editingCategory.value.id}`, { name: editingCategory.value.name.trim() });
    notificationStore.showNotification('Category updated successfully!', 'success');
    editingCategory.value = null;
    fetchCategories();
    fetchProducts(); // Refresh products in case category name changed
  } catch (error) {
    console.error('Error updating category:', error);
    notificationStore.showNotification('Error updating category: ' + (error.response?.data?.error || 'Unknown error'), 'error');
  }
};

const cancelEditCategory = () => {
  editingCategory.value = null;
};

const deleteCategory = async (id) => {
  if (confirm('Are you sure you want to delete this category? This will fail if products are linked.')) {
    try {
      await axios.delete(`/categories/${id}`);
      notificationStore.showNotification('Category deleted successfully!', 'success');
      fetchCategories();
    } catch (error) {
      console.error('Error deleting category:', error);
      notificationStore.showNotification('Error deleting category: ' + (error.response?.data?.error || 'Unknown error'), 'error');
    }
  }
};

onMounted(() => {
  fetchProducts();
  fetchCategories();
});
</script>

<template>
  <div class="container mx-auto p-4">
    <h1 class="text-4xl font-bold text-center mb-8 text-gray-800">Admin Dashboard</h1>

    <!-- Category Management Section -->
    <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
      <h2 class="text-2xl font-semibold mb-4 text-gray-700">Category Management</h2>

      <!-- Add New Category Form -->
      <div class="mb-6 flex flex-col md:flex-row items-end md:space-x-4 space-y-4 md:space-y-0">
        <div class="flex-grow w-full">
          <label for="newCategoryName" class="block text-gray-700 text-sm font-bold mb-2">New Category Name:</label>
          <input type="text" id="newCategoryName" v-model="newCategoryName" class="form-input" placeholder="e.g., Smartphones">
        </div>
        <button @click="addCategory" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200 w-full md:w-auto">
          Add Category
        </button>
      </div>

      <!-- Category List -->
      <div v-if="categories.length === 0" class="text-center text-gray-500">No categories created yet.</div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="category in categories" :key="category.id">
              <td class="px-6 py-4 whitespace-nowrap">{{ category.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span v-if="editingCategory?.id !== category.id">{{ category.name }}</span>
                <input v-else type="text" v-model="editingCategory.name" class="form-input-sm">
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div v-if="editingCategory?.id === category.id" class="space-x-2">
                  <button @click="saveEditCategory" class="text-green-600 hover:text-green-900">Save</button>
                  <button @click="cancelEditCategory" class="text-gray-600 hover:text-gray-900">Cancel</button>
                </div>
                <div v-else class="space-x-2">
                  <button @click="startEditCategory(category)" class="text-indigo-600 hover:text-indigo-900">Edit</button>
                  <button @click="deleteCategory(category.id)" class="text-red-600 hover:text-red-900">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Product Management Section -->
    <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
      <h2 class="text-2xl font-semibold mb-4 text-gray-700">Product Management</h2>

      <!-- Add New Product Form -->
      <h3 class="text-xl font-semibold mb-3 text-gray-700">Add New Product</h3>
      <form @submit.prevent="addProduct" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8 p-4 border rounded-lg bg-gray-50">
        <div>
          <label for="newProductName" class="block text-gray-700 text-sm font-bold mb-2">Product Name:</label>
          <input type="text" id="newProductName" v-model="newProduct.name" class="form-input" required>
        </div>
        <div>
          <label for="newProductPrice" class="block text-gray-700 text-sm font-bold mb-2">Price:</label>
          <input type="number" id="newProductPrice" v-model.number="newProduct.price" class="form-input" step="0.01" required>
        </div>
        <div class="md:col-span-2">
          <label for="newProductDescription" class="block text-gray-700 text-sm font-bold mb-2">Description:</label>
          <textarea id="newProductDescription" v-model="newProduct.description" class="form-textarea"></textarea>
        </div>
        <div>
          <label for="newProductImage" class="block text-gray-700 text-sm font-bold mb-2">Image:</label>
          <input type="file" id="newProductImage" @change="handleImageFileChange($event, 'new')" class="form-input-file">
          <div v-if="newProduct.image_preview_url" class="mt-2">
            <img :src="newProduct.image_preview_url" alt="Image Preview" class="max-w-[150px] h-auto rounded-md shadow">
          </div>
        </div>
        <div>
          <label for="newProductCategory" class="block text-gray-700 text-sm font-bold mb-2">Category:</label>
          <select id="newProductCategory" v-model.number="newProduct.category_id" class="form-select" required>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>
        <div class="md:col-span-2">
          <button type="submit" class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-lg w-full transition-colors duration-200">Add Product</button>
        </div>
      </form>

      <!-- Product List -->
      <h3 class="text-xl font-semibold mb-3 text-gray-700">Existing Products</h3>
      <div v-if="products.length === 0" class="text-center text-gray-500">No products to display.</div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Image</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="product in products" :key="product.id">
              <td class="px-6 py-4 whitespace-nowrap">{{ product.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <img v-if="editingProduct?.id === product.id && editingProductImagePreviewUrl" :src="editingProductImagePreviewUrl" alt="Product Image" class="w-16 h-16 object-cover rounded-md">
                <img v-else-if="product.image_url" :src="`${axios.defaults.baseURL}${product.image_url}`" alt="Product Image" class="w-16 h-16 object-cover rounded-md">
                <span v-else class="text-gray-400">No Image</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span v-if="editingProduct?.id !== product.id">{{ product.name }}</span>
                <input v-else type="text" v-model="editingProduct.name" class="form-input-sm">
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span v-if="editingProduct?.id !== product.id">Ksh {{ product.price.toFixed(2)}}</span>
                <input v-else type="number" v-model.number="editingProduct.price" class="form-input-sm" step="0.01">
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span v-if="editingProduct?.id !== product.id">{{ product.category_name }}</span>
                <select v-else v-model.number="editingProduct.category_id" class="form-select-sm">
                  <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                  </option>
                </select>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div v-if="editingProduct?.id === product.id" class="flex flex-col space-y-2">
                  <button @click="saveEditProduct" class="text-green-600 hover:text-green-900">Save</button>
                  <button @click="cancelEditProduct" class="text-gray-600 hover:text-gray-900">Cancel</button>
                  <input type="file" @change="handleImageFileChange($event, 'edit')" class="form-input-file-sm">
                  <button v-if="editingProductImagePreviewUrl" @click="removeEditingProductImage" class="text-red-600 hover:text-red-900 text-xs">Remove Image</button>
                </div>
                <div v-else class="space-x-2">
                  <button @click="startEditProduct(product)" class="text-indigo-600 hover:text-indigo-900">Edit</button>
                  <button @click="deleteProduct(product.id)" class="text-red-600 hover:text-red-900">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Additional specific styling for Admin page forms */
.form-input-file {
  @apply block w-full text-sm text-gray-500
  file:mr-4 file:py-2 file:px-4
  file:rounded-full file:border-0
  file:text-sm file:font-semibold
  file:bg-blue-50 file:text-blue-700
  hover:file:bg-blue-100;
}
.form-input-file-sm {
  @apply block w-full text-xs text-gray-500
  file:mr-2 file:py-1 file:px-2
  file:rounded-full file:border-0
  file:text-xs file:font-semibold
  file:bg-blue-50 file:text-blue-700
  hover:file:bg-blue-100;
}
</style>