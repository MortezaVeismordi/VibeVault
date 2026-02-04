import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { AlertCircle, RotateCcw, MessageCircle } from 'lucide-react';

export function OrderCancel() {
  return (
    <div className="min-h-screen flex items-center justify-center py-12">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="max-w-lg w-full mx-auto px-4"
      >
        {/* Warning Icon */}
        <motion.div
          className="flex justify-center mb-8"
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 0.6, repeat: Infinity, repeatDelay: 2 }}
        >
          <div className="relative">
            <div className="absolute inset-0 bg-orange-500/20 rounded-full blur-2xl" />
            <AlertCircle className="w-24 h-24 text-orange-500 relative" />
          </div>
        </motion.div>

        {/* Content */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-3">Payment Cancelled</h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-4">
            Your payment was not completed
          </p>
          <div className="inline-block px-4 py-2 bg-yellow-100 dark:bg-yellow-900/30 border border-yellow-300 dark:border-yellow-700 rounded-lg text-sm text-yellow-800 dark:text-yellow-200">
            No charges were made to your account
          </div>
        </div>

        {/* What You Can Do */}
        <div className="mb-8">
          <h2 className="font-semibold mb-4 text-center">What you can do:</h2>
          <div className="space-y-3">
            {[
              'Your items are still in your cart',
              'Try a different payment method',
              'Contact our support team for help',
              'Continue shopping for other products',
            ].map((item, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 + idx * 0.1 }}
                className="flex gap-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
              >
                <div className="w-5 h-5 rounded-full bg-orange-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-xs font-bold text-orange-600 dark:text-orange-400">
                    {idx + 1}
                  </span>
                </div>
                <p className="text-sm text-gray-700 dark:text-gray-300">{item}</p>
              </motion.div>
            ))}
          </div>
        </div>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="flex flex-col sm:flex-row gap-3"
        >
          <Link
            to="/cart"
            className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-500 to-violet-600 text-white rounded-xl font-semibold hover:shadow-glow transition-all duration-300 text-center flex items-center justify-center gap-2"
          >
            <RotateCcw className="w-4 h-4" />
            Back to Cart
          </Link>
          <a
            href="mailto:support@proshop.com"
            className="flex-1 px-6 py-3 border-2 border-gray-300 dark:border-gray-700 rounded-xl font-semibold hover:bg-gray-100 dark:hover:bg-gray-800 transition-all duration-300 text-center flex items-center justify-center gap-2"
          >
            <MessageCircle className="w-4 h-4" />
            Contact Support
          </a>
        </motion.div>

        {/* Continue Shopping Link */}
        <div className="text-center mt-6">
          <Link to="/shop" className="text-blue-600 dark:text-blue-400 hover:underline">
            Or continue shopping →
          </Link>
        </div>
      </motion.div>
    </div>
  );
}


