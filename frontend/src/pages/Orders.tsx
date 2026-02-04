import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { apiClient } from '../lib/api-simple';
import { useNavigate } from 'react-router-dom';
import { Clock, CheckCircle, AlertCircle, Package } from 'lucide-react';
import { ProductGridSkeleton } from '../components/LoadingSkeleton';

const statusConfig: Record<string, { color: string; icon: any; label: string }> = {
  pending: { color: 'yellow', icon: Clock, label: 'Pending' },
  processing: { color: 'blue', icon: Package, label: 'Processing' },
  completed: { color: 'green', icon: CheckCircle, label: 'Completed' },
  cancelled: { color: 'red', icon: AlertCircle, label: 'Cancelled' },
};

export function Orders() {
  const navigate = useNavigate();

  const { data: orders, isLoading } = useQuery({
    queryKey: ['orders'],
    queryFn: () => apiClient.getOrders(),
  });

  if (isLoading) {
    return <ProductGridSkeleton count={3} />;
  }

  if (!orders || orders.length === 0) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <Package className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h1 className="text-3xl font-bold mb-2">No Orders Yet</h1>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            You haven't placed any orders yet. Start shopping today!
          </p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/shop')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-300"
          >
            Start Shopping
          </motion.button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-bold mb-8"
        >
          Your Orders
        </motion.h1>

        <motion.div layout className="space-y-4">
          {orders.map((order, idx) => {
            const config = statusConfig[order.status] || statusConfig.pending;
            const Icon = config.icon;

            return (
              <motion.div
                key={order.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-md hover:shadow-lg transition-all duration-300"
              >
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                      Order #{order.id}
                    </p>
                    <h3 className="text-xl font-bold">
                      {new Date(order.created_at).toLocaleDateString()}
                    </h3>
                  </div>

                  <div className="flex items-center gap-2">
                    <Icon
                      className={`w-5 h-5 text-${config.color}-600 dark:text-${config.color}-400`}
                    />
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-semibold bg-${config.color}-100 dark:bg-${config.color}-900/30 text-${config.color}-700 dark:text-${config.color}-300`}
                    >
                      {config.label}
                    </span>
                  </div>
                </div>

                {/* Order Items */}
                <div className="mb-4 pb-4 border-t border-gray-200 dark:border-gray-700 pt-4">
                  {order.items && order.items.length > 0 ? (
                    <div className="space-y-2">
                      {order.items.map((item) => (
                        <div key={item.id} className="flex justify-between text-sm">
                          <span className="text-gray-600 dark:text-gray-400">
                            {item.quantity}x {item.product_name}
                          </span>
                          <span className="font-semibold">
                            ${(parseFloat(item.price.toString()) * item.quantity).toFixed(
                              2
                            )}
                          </span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500 dark:text-gray-400 text-sm">
                      No items in this order
                    </p>
                  )}
                </div>

                {/* Order Total & Actions */}
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                  <div>
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-1">
                      Order Total
                    </p>
                    <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                      ${order.total}
                    </p>
                  </div>

                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => navigate(`/orders/${order.id}`)}
                    className="px-6 py-2 border border-blue-600 dark:border-blue-400 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all duration-300"
                  >
                    View Details
                  </motion.button>
                </div>
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </div>
  );
}


