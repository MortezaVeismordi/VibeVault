import { Link } from 'react-router-dom';
import { Facebook, Twitter, Instagram, Mail } from 'lucide-react';

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-violet-600 rounded-lg" />
              <span className="font-bold text-lg gradient-text">ProShop</span>
            </div>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Your trusted e-commerce platform for quality products and seamless shopping experience.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold mb-4 text-gray-900 dark:text-white">Shop</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/shop" className="text-gray-600 dark:text-gray-400 hover:text-blue-500 transition-all duration-300">
                  All Products
                </Link>
              </li>
              <li>
                <a href="#categories" className="text-gray-600 dark:text-gray-400 hover:text-blue-500 transition-all duration-300">
                  Categories
                </a>
              </li>
              <li>
                <a href="#featured" className="text-gray-600 dark:text-gray-400 hover:text-blue-500 transition-all duration-300">
                  Featured
                </a>
              </li>
              <li>
                <a href="#sale" className="text-gray-600 dark:text-gray-400 hover:text-blue-500 transition-all duration-300">
                  On Sale
                </a>
              </li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="font-semibold mb-4 text-gray-900 dark:text-white">Company</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#about" className="text-gray-600 dark:text-gray-400 hover:text-blue-500 transition-all duration-300">
                  About Us
                </a>
              </li>
              <li>
                <a href="#contact" className="text-gray-600 dark:text-gray-400 hover:text-blue-500 transition-all duration-300">
                  Contact
                </a>
              </li>
              <li>
                <a href="#privacy" className="text-gray-600 dark:text-gray-400 hover:text-blue-500 transition-all duration-300">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#terms" className="text-gray-600 dark:text-gray-400 hover:text-blue-500 transition-all duration-300">
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>

          {/* Newsletter */}
          <div>
            <h3 className="font-semibold mb-4 text-gray-900 dark:text-white">Newsletter</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Subscribe to get special offers and updates.
            </p>
            <div className="flex gap-2">
              <input
                type="email"
                placeholder="Your email"
                className="flex-1 px-3 py-2 rounded-lg bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 text-sm focus:outline-none focus:border-blue-500"
              />
              <button className="px-4 py-2 bg-gradient-to-r from-blue-500 to-violet-600 text-white rounded-lg hover:shadow-glow transition-all duration-300 text-sm">
                <Mail className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-gray-200 dark:border-gray-800 py-8">
          {/* Social Links */}
          <div className="flex justify-center gap-6 mb-6">
            <a
              href="#facebook"
              className="p-3 bg-gray-200 dark:bg-gray-800 rounded-full hover:bg-blue-500 hover:text-white transition-all duration-300"
              aria-label="Facebook"
            >
              <Facebook className="w-5 h-5" />
            </a>
            <a
              href="#twitter"
              className="p-3 bg-gray-200 dark:bg-gray-800 rounded-full hover:bg-blue-500 hover:text-white transition-all duration-300"
              aria-label="Twitter"
            >
              <Twitter className="w-5 h-5" />
            </a>
            <a
              href="#instagram"
              className="p-3 bg-gray-200 dark:bg-gray-800 rounded-full hover:bg-pink-500 hover:text-white transition-all duration-300"
              aria-label="Instagram"
            >
              <Instagram className="w-5 h-5" />
            </a>
          </div>

          {/* Copyright */}
          <div className="text-center text-sm text-gray-600 dark:text-gray-400">
            <p>&copy; {currentYear} ProShop. All rights reserved. Built with React & Django.</p>
          </div>
        </div>
      </div>
    </footer>
  );
}


