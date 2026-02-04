import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { AlertTriangle, Home, Search } from 'lucide-react';

export function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center py-12">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="max-w-lg w-full mx-auto px-4 text-center"
      >
        {/* 404 Illustration */}
        <motion.div
          className="mb-8"
          animate={{ y: [0, -20, 0] }}
          transition={{ duration: 3, repeat: Infinity }}
        >
          <div className="relative inline-block">
            <div className="text-9xl font-bold gradient-text">404</div>
            <div className="absolute inset-0 opacity-20">
              <AlertTriangle className="w-32 h-32 mx-auto animate-spin" />
            </div>
          </div>
        </motion.div>

        {/* Content */}
        <h1 className="text-4xl font-bold mb-3">Page Not Found</h1>
        <p className="text-lg text-gray-600 dark:text-gray-400 mb-8">
          Oops! The page you're looking for doesn't exist. It might have been moved or deleted.
        </p>

        {/* Suggestions */}
        <div className="space-y-3 mb-8">
          {[
            { icon: Home, text: 'Go back to home' },
            { icon: Search, text: 'Search products' },
          ].map((item, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 + idx * 0.1 }}
              className="text-sm text-gray-600 dark:text-gray-400"
            >
              <item.icon className="w-4 h-4 inline-block mr-2" />
              {item.text}
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
            to="/"
            className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-500 to-violet-600 text-white rounded-xl font-semibold hover:shadow-glow transition-all duration-300 flex items-center justify-center gap-2"
          >
            <Home className="w-4 h-4" />
            Go Home
          </Link>
          <Link
            to="/shop"
            className="flex-1 px-6 py-3 border-2 border-gray-300 dark:border-gray-700 rounded-xl font-semibold hover:bg-gray-100 dark:hover:bg-gray-800 transition-all duration-300 flex items-center justify-center gap-2"
          >
            <Search className="w-4 h-4" />
            Shop
          </Link>
        </motion.div>
      </motion.div>
    </div>
  );
}


