import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { apiClient } from '../lib/api-simple';

interface CartState {
  items: any[];
  total: string;
  itemCount: number;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchCart: () => Promise<void>;
  addItem: (product: any, quantity: number) => Promise<void>;
  updateItem: (itemId: string, quantity: number) => Promise<void>;
  removeItem: (itemId: string) => Promise<void>;
  clearCart: () => Promise<void>;
  setItems: (items: any[], total: string) => void;
}

export const useCartStore = create<CartState>()(
  persist(
    (set) => ({
      items: [],
      total: '0',
      itemCount: 0,
      isLoading: false,
      error: null,

      fetchCart: async () => {
        set({ isLoading: true, error: null });
        try {
          const cart = await apiClient.getCart();
          set({
            items: cart.items,
            total: cart.total,
            itemCount: cart.item_count,
            isLoading: false,
          });
        } catch (error) {
          set({
            error: 'Failed to fetch cart',
            isLoading: false,
          });
        }
      },

      addItem: async (product: Product, quantity: number) => {
        set({ isLoading: true, error: null });
        try {
          await apiClient.addToCart(product.id, quantity);
          // Refetch cart to update state
          const cart = await apiClient.getCart();
          set({
            items: cart.items,
            total: cart.total,
            itemCount: cart.item_count,
            isLoading: false,
          });
        } catch (error) {
          set({
            error: 'Failed to add item to cart',
            isLoading: false,
          });
        }
      },

      updateItem: async (itemId: string, quantity: number) => {
        set({ isLoading: true, error: null });
        try {
          if (quantity <= 0) {
            await apiClient.removeFromCart(itemId);
          } else {
            await apiClient.updateCartItem(itemId, quantity);
          }
          const cart = await apiClient.getCart();
          set({
            items: cart.items,
            total: cart.total,
            itemCount: cart.item_count,
            isLoading: false,
          });
        } catch (error) {
          set({
            error: 'Failed to update cart item',
            isLoading: false,
          });
        }
      },

      removeItem: async (itemId: string) => {
        set({ isLoading: true, error: null });
        try {
          await apiClient.removeFromCart(itemId);
          const cart = await apiClient.getCart();
          set({
            items: cart.items,
            total: cart.total,
            itemCount: cart.item_count,
            isLoading: false,
          });
        } catch (error) {
          set({
            error: 'Failed to remove item from cart',
            isLoading: false,
          });
        }
      },

      clearCart: async () => {
        set({ isLoading: true, error: null });
        try {
          await apiClient.clearCart();
          set({
            items: [],
            total: '0',
            itemCount: 0,
            isLoading: false,
          });
        } catch (error) {
          set({
            error: 'Failed to clear cart',
            isLoading: false,
          });
        }
      },

      setItems: (items: CartItem[], total: string) => {
        set({
          items,
          total,
          itemCount: items.length,
        });
      },
    }),
    {
      name: 'cart-storage',
      version: 1,
    }
  )
);

