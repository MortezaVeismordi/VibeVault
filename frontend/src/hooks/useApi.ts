import { useQuery, useMutation } from '@tanstack/react-query';
import { apiClient } from '../lib/api-simple';

export function useProducts(filters?: {
  search?: string;
  category?: number;
  min_price?: number;
  max_price?: number;
  sort_by?: string;
  page?: number;
  limit?: number;
}) {
  return useQuery({
    queryKey: ['products', filters],
    queryFn: () => apiClient.getProducts(filters),
  });
}

export function useProduct(id: number) {
  return useQuery({
    queryKey: ['product', id],
    queryFn: () => apiClient.getProduct(id),
    enabled: !!id,
  });
}

export function useCategories() {
  return useQuery({
    queryKey: ['categories'],
    queryFn: () => apiClient.getCategories(),
  });
}

export function useCreateCheckout() {
  return useMutation({
    mutationFn: () => apiClient.createCheckoutSession(),
  });
}

export function useGetOrders() {
  return useQuery({
    queryKey: ['orders'],
    queryFn: () => apiClient.getOrders(),
  });
}

export function useGetOrder(id: number) {
  return useQuery({
    queryKey: ['order', id],
    queryFn: () => apiClient.getOrder(id),
    enabled: !!id,
  });
}

export function useLogin() {
  return useMutation({
    mutationFn: (data: { email: string; password: string }) =>
      apiClient.login(data.email, data.password),
  });
}

export function useRegister() {
  return useMutation({
    mutationFn: (data: { email: string; password: string; first_name?: string; last_name?: string }) =>
      apiClient.register(data),
  });
}

