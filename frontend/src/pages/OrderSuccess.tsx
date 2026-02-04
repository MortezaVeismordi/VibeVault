import { Link, useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { CheckCircle, Package, Truck, MailOpen } from 'lucide-react';

export function OrderSuccess() {
  const [searchParams] = useSearchParams();
  const orderId = searchParams.get('order_id');

  return (
    <div className="min-h-screen flex items-center justify-center py-12">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="max-w-lg w-full mx-auto px-4"
      >
        {/* Success Icon */}
        <motion.div
          className="flex justify-center mb-8"
          animate={{ scale: [1, 1.1, 1] }}
          transition={{ duration: 0.6, repeat: Infinity, repeatDelay: 2 }}
        >
          <div className="relative">
            <div className="absolute inset-0 bg-green-500/20 rounded-full blur-2xl" />
            <CheckCircle className="w-24 h-24 text-green-500 relative" />
          </div>
        </motion.div>

        {/* Content */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-3">Payment Successful!</h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-2">
            Thank you for your purchase
          </p>
          {orderId && (
            <p className="text-sm text-gray-500 dark:text-gray-500">
              Order ID: <span className="font-mono font-semibold">{orderId}</span>
            </p>
          )}
        </div>

        {/* Info Cards */}
        <div className="space-y-4 mb-8">
          {[
            {
              icon: MailOpen,
              title: 'Confirmation Email',
              desc: 'Check your inbox for order details',
            },
            {
              icon: Package,
              title: 'Order Processing',
              desc: 'Your order will be prepared shortly',
            },
            {
              icon: Truck,
              title: 'Fast Shipping',
              desc: 'Track your package once it ships',
            },
          ].map((item, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 + idx * 0.1 }}
              className="flex gap-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-xl"
            >
              <item.icon className="w-6 h-6 text-green-500 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-sm">{item.title}</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {item.desc}
                </p>
              </div>
            </motion.div>
          ))}
        </div>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="flex flex-col sm:flex-row gap-3"
        >
          <Link
            to="/orders"
            className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-500 to-violet-600 text-white rounded-xl font-semibold hover:shadow-glow transition-all duration-300 text-center"
          >
            View Orders
          </Link>
          <Link
            to="/shop"
            className="flex-1 px-6 py-3 border-2 border-gray-300 dark:border-gray-700 rounded-xl font-semibold hover:bg-gray-100 dark:hover:bg-gray-800 transition-all duration-300 text-center"
          >
            Continue Shopping
          </Link>
        </motion.div>
      </motion.div>
    </div>
  );
}


