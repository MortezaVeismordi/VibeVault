import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useCartStore } from '../store/cartStore';
import { Trash2, ShoppingBag, ArrowRight } from 'lucide-react';
import toast from 'react-hot-toast';
import { useState } from 'react';
import { apiClient } from '../lib/api-simple';

export function Cart() {
  const navigate = useNavigate();
  const { items, total, removeItem, updateItem } = useCartStore();
  const [isCheckingOut, setIsCheckingOut] = useState(false);

  const handleRemove = (itemId: number) => {
    removeItem(itemId);
    toast.success('Item removed from cart');
  };

  const handleQuantityChange = (itemId: number, newQuantity: number) => {
    if (newQuantity <= 0) {
      handleRemove(itemId);
    } else {
      updateItem(itemId, newQuantity);
    }
  };

  const handleCheckout = async () => {
    setIsCheckingOut(true);
    try {
      const session = await apiClient.createCheckoutSession();
      if (session.checkout_url) {
        window.location.href = session.checkout_url;
      }
    } catch (error) {
      toast.error('Failed to proceed to checkout');
      setIsCheckingOut(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <ShoppingBag className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h1 className="text-3xl font-bold mb-2">Your Cart is Empty</h1>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Start shopping to add items to your cart
          </p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/shop')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-300"
          >
            Continue Shopping
          </motion.button>
        </motion.div>
      </div>
    );
  }

  const subtotal = parseFloat(total.toString());
  const tax = subtotal * 0.1; // 10% tax
  const shipping = subtotal > 50 ? 0 : 5; // Free shipping over $50
  const finalTotal = subtotal + tax + shipping;

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 lg:grid-cols-3 gap-8"
        >
          {/* Cart Items */}
          <div className="lg:col-span-2">
            <h1 className="text-3xl font-bold mb-8">Shopping Cart</h1>

            <motion.div layout className="space-y-4">
              {items.map((item, idx) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  className="flex gap-4 p-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm hover:shadow-md transition-all duration-300"
                >
                  {/* Product Image */}
                  <div className="w-24 h-24 rounded-lg overflow-hidden flex-shrink-0 bg-gray-100 dark:bg-gray-700">
                    <img
                      src={item.product?.images?.[0]?.image || '/placeholder.jpg'}
                      alt={item.product?.name}
                      className="w-full h-full object-cover"
                    />
                  </div>

                  {/* Product Details */}
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg mb-1">
                      {item.product?.name}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                      ${item.price} each
                    </p>

                    {/* Quantity Controls */}
                    <div className="flex items-center gap-2 w-fit">
                      <button
                        onClick={() =>
                          handleQuantityChange(item.id, item.quantity - 1)
                        }
                        className="px-2 py-1 rounded border border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 transition-all duration-300"
                      >
                        −
                      </button>
                      <span className="px-4 py-1 font-semibold">
                        {item.quantity}
                      </span>
                      <button
                        onClick={() =>
                          handleQuantityChange(item.id, item.quantity + 1)
                        }
                        className="px-2 py-1 rounded border border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 transition-all duration-300"
                      >
                        +
                      </button>
                    </div>
                  </div>

                  {/* Price & Remove */}
                  <div className="text-right">
                    <p className="text-lg font-bold text-blue-600 dark:text-blue-400 mb-4">
                      ${(parseFloat(item.price.toString()) * item.quantity).toFixed(2)}
                    </p>
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => handleRemove(item.id)}
                      className="p-2 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-all duration-300"
                    >
                      <Trash2 className="w-5 h-5" />
                    </motion.button>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          </div>

          {/* Order Summary */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="h-fit sticky top-20 bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg"
          >
            <h2 className="text-2xl font-bold mb-6">Order Summary</h2>

            <div className="space-y-3 mb-6 pb-6 border-b border-gray-200 dark:border-gray-700">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Subtotal</span>
                <span className="font-semibold">${subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Tax (10%)</span>
                <span className="font-semibold">${tax.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Shipping</span>
                <span className="font-semibold">
                  {shipping === 0 ? (
                    <span className="text-green-600 dark:text-green-400">Free</span>
                  ) : (
                    `$${shipping.toFixed(2)}`
                  )}
                </span>
              </div>
            </div>

            <div className="flex justify-between mb-6 text-lg font-bold">
              <span>Total</span>
              <span className="text-blue-600 dark:text-blue-400">
                ${finalTotal.toFixed(2)}
              </span>
            </div>

            {shipping === 0 && (
              <p className="text-sm text-green-600 dark:text-green-400 mb-4 text-center">
                ✓ Free shipping unlocked!
              </p>
            )}

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleCheckout}
              disabled={isCheckingOut}
              className="w-full py-4 bg-gradient-to-r from-blue-500 to-violet-600 text-white rounded-xl font-semibold hover:shadow-glow transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 mb-3"
            >
              {isCheckingOut ? 'Processing...' : 'Proceed to Checkout'}
              <ArrowRight className="w-4 h-4" />
            </motion.button>

            <button
              onClick={() => navigate('/shop')}
              className="w-full py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-xl font-semibold hover:bg-gray-50 dark:hover:bg-gray-700 transition-all duration-300"
            >
              Continue Shopping
            </button>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}


