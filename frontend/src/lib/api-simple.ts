import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

// Helper to extract array from paginated response
const extractData = (response: any) => {
  if (Array.isArray(response)) return response;
  if (response.results && Array.isArray(response.results)) return response.results;
  return response;
};

export const apiClient = {
  // Products
  getProducts: (filters?: any) => client.get('/products/', { params: filters }).then(r => extractData(r.data)),
  getProduct: (id: number) => client.get(`/products/${id}/`).then(r => r.data),

  // Categories
  getCategories: () => client.get('/categories/').then(r => extractData(r.data)),

  // Cart
  getCart: () => client.get('/cart/').then(r => r.data),
  addToCart: (productId: number, quantity: number) => 
    client.post('/cart/add/', { product_id: productId, quantity }).then(r => r.data),
  updateCartItem: (itemId: number, quantity: number) => 
    client.put(`/cart/items/${itemId}/`, { quantity }).then(r => r.data),
  removeFromCart: (itemId: number) => client.delete(`/cart/items/${itemId}/`).then(r => r.data),
  clearCart: () => client.post('/cart/clear/').then(r => r.data),

  // Orders
  getOrders: () => client.get('/orders/').then(r => r.data),
  getOrder: (id: number) => client.get(`/orders/${id}/`).then(r => r.data),

  // Checkout
  createCheckoutSession: () => client.post('/checkout/session/').then(r => r.data),
  getPaymentStatus: (sessionId: string) => 
    client.get(`/checkout/status/${sessionId}/`).then(r => r.data),

  // Auth
  login: (email: string, password: string) => 
    client.post('/auth/login/', { email, password }).then(r => r.data),
  register: (data: any) => client.post('/auth/register/', data).then(r => r.data),
  logout: () => {
    localStorage.removeItem('auth_token');
    return Promise.resolve();
  },
  getCurrentUser: () => client.get('/auth/me/').then(r => r.data),
  isAuthenticated: () => !!localStorage.getItem('auth_token'),
};

