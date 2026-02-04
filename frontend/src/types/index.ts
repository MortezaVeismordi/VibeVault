export interface Category {
  id: number;
  name: string;
  description?: string;
  slug: string;
}

export interface ProductImage {
  id: number;
  image: string;
  alt_text?: string;
  is_primary: boolean;
}

export interface ProductVariant {
  id: number;
  name: string;
  sku: string;
  price: string;
  stock: number;
}

export interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  price: string;
  discount_price?: string | null;
  category: Category | number;
  images: ProductImage[];
  rating?: number;
  review_count?: number;
  stock: number;
  is_featured: boolean;
  created_at: string;
  updated_at: string;
}

export interface CartItem {
  id: string;
  product: Product;
  quantity: number;
  price: string;
  subtotal: string;
}

export interface Cart {
  items: CartItem[];
  total: string;
  item_count: number;
}

export interface Order {
  id: number;
  order_number: string;
  user: number;
  items: OrderItem[];
  total_amount: string;
  status: "pending" | "processing" | "completed" | "cancelled";
  payment_status: "pending" | "completed";
  shipping_address: string;
  created_at: string;
  updated_at: string;
}

export interface OrderItem {
  id: number;
  product: Product;
  quantity: number;
  price: string;
  subtotal: string;
}

export interface CheckoutSession {
  session_id: string;
  checkout_url: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

export interface Review {
  id: number;
  product: number;
  author: string;
  rating: number;
  title: string;
  content: string;
  created_at: string;
}

