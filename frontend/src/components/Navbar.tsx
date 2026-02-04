import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X, ShoppingCart, Sun, Moon, Search } from 'lucide-react';
import { useCartStore } from '../store/cartStore';
import { motion, AnimatePresence } from 'framer-motion';

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [isDark, setIsDark] = useState(() => 
    document.documentElement.classList.contains('dark')
  );
  const itemCount = useCartStore((state) => state.itemCount);

  const toggleDarkMode = () => {
    document.documentElement.classList.toggle('dark');
    setIsDark(!isDark);
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
  };

  return (
    <nav className="sticky top-0 z-50 glass-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 font-bold text-xl">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-violet-600 rounded-lg" />
            <span className="gradient-text">ProShop</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-8">
            <Link to="/shop" className="hover:text-blue-500 transition-all duration-300">
              Shop
            </Link>
            <Link to="/orders" className="hover:text-blue-500 transition-all duration-300">
              Orders
            </Link>
            <div className="relative">
              <input
                type="text"
                placeholder="Search products..."
                className="px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 text-sm w-64 focus:outline-none focus:border-blue-500"
              />
              <Search className="absolute right-3 top-2.5 w-4 h-4 text-gray-400" />
            </div>
          </div>

          {/* Right Actions */}
          <div className="flex items-center gap-4">
            {/* Dark Mode Toggle */}
            <button
              onClick={toggleDarkMode}
              className="p-2 hover:bg-gray-200 dark:hover:bg-gray-800 rounded-lg transition-all duration-300"
              aria-label="Toggle dark mode"
            >
              {isDark ? (
                <Sun className="w-5 h-5 text-yellow-400" />
              ) : (
                <Moon className="w-5 h-5 text-gray-600" />
              )}
            </button>

            {/* Cart Icon */}
            <Link to="/cart" className="relative p-2 hover:bg-gray-200 dark:hover:bg-gray-800 rounded-lg transition-all duration-300">
              <ShoppingCart className="w-5 h-5" />
              {itemCount > 0 && (
                <motion.span
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute top-0 right-0 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center"
                >
                  {itemCount}
                </motion.span>
              )}
            </Link>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden p-2 hover:bg-gray-200 dark:hover:bg-gray-800 rounded-lg transition-all duration-300"
            >
              {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden border-t border-gray-200 dark:border-gray-800 py-4"
            >
              <div className="space-y-3">
                <Link
                  to="/shop"
                  className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-all duration-300"
                  onClick={() => setIsOpen(false)}
                >
                  Shop
                </Link>
                <Link
                  to="/orders"
                  className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-all duration-300"
                  onClick={() => setIsOpen(false)}
                >
                  Orders
                </Link>
                <div className="px-4 py-2">
                  <input
                    type="text"
                    placeholder="Search..."
                    className="w-full px-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 text-sm"
                  />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </nav>
  );
}


