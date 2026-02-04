import axios from 'axios';
import type { AxiosInstance, AxiosError } from 'axios';
import { Product, Category, Cart, CartItem, Order, CheckoutSession, User, LoginRequest, RegisterRequest } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

class APIClient {
  private client: AxiosInstance;
  private token: string | null = localStorage.getItem('auth_token');

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token to requests if available
    this.client.interceptors.request.use((config) => {
      if (this.token) {
        config.headers.Authorization = `Bearer ${this.token}`;
      }
      return config;
    });

    // Handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Clear token and redirect to login
          this.clearAuth();
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  setToken(token: string) {
    this.token = token;
    localStorage.setItem('auth_token', token);
  }

  clearAuth() {
    this.token = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
  }

  // ===== PRODUCTS =====
  async getProducts(params?: {
    page?: number;
    page_size?: number;
    search?: string;
    category?: number;
    min_price?: number;
    max_price?: number;
    is_featured?: boolean;
    ordering?: string;
  }) {
    const { data } = await this.client.get<{
      count: number;
      next: string | null;
      previous: string | null;
      results: Product[];
    }>('/shop/products/', { params });
    return data;
  }

  async getProduct(id: number) {
    const { data } = await this.client.get<Product>(`/shop/products/${id}/`);
    return data;
  }

  // ===== CATEGORIES =====
  async getCategories() {
    const { data } = await this.client.get<Category[]>('/shop/categories/');
    return data;
  }

  async getCategory(id: number) {
    const { data } = await this.client.get<Category>(`/shop/categories/${id}/`);
    return data;
  }

  // ===== CART =====
  async getCart() {
    const { data } = await this.client.get<Cart>('/cart/');
    return data;
  }

  async addToCart(productId: number, quantity: number = 1) {
    const { data } = await this.client.post<CartItem>('/cart/', {
      product_id: productId,
      quantity,
    });
    return data;
  }

  async updateCartItem(itemId: string, quantity: number) {
    const { data } = await this.client.patch<CartItem>(`/cart/${itemId}/`, {
      quantity,
    });
    return data;
  }

  async removeFromCart(itemId: string) {
    await this.client.delete(`/cart/${itemId}/`);
  }

  async clearCart() {
    await this.client.post('/cart/clear/');
  }

  // ===== CHECKOUT & PAYMENT =====
  async createCheckoutSession(items?: { product: number; quantity: number }[]) {
    const { data } = await this.client.post<CheckoutSession>(
      '/payment/checkout/',
      items ? { items } : {}
    );
    return data;
  }

  async getPaymentStatus(sessionId: string) {
    const { data } = await this.client.get(`/payment/status/${sessionId}/`);
    return data;
  }

  // ===== ORDERS =====
  async getOrders() {
    const { data } = await this.client.get<Order[]>('/orders/');
    return data;
  }

  async getOrder(id: number) {
    const { data } = await this.client.get<Order>(`/orders/${id}/`);
    return data;
  }

  // ===== AUTHENTICATION =====
  async login(credentials: LoginRequest) {
    const { data } = await this.client.post<{ token: string; user: User }>(
      '/accounts/login/',
      credentials
    );
    this.setToken(data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  }

  async register(details: RegisterRequest) {
    const { data } = await this.client.post<{ token: string; user: User }>(
      '/accounts/register/',
      details
    );
    this.setToken(data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  }

  async logout() {
    this.clearAuth();
  }

  getCurrentUser(): User | null {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  isAuthenticated(): boolean {
    return !!this.token && !!this.getCurrentUser();
  }
}

export const apiClient = new APIClient();
