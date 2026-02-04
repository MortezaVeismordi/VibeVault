import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ChevronRight, Zap, Truck, Shield, RotateCcw } from 'lucide-react';
import { apiClient } from '../lib/api-simple';
import { ProductCard } from '../components/ProductCard';
import { ProductGridSkeleton } from '../components/LoadingSkeleton';

export function Home() {
  const { data: products, isLoading } = useQuery({
    queryKey: ['products', { is_featured: true, page_size: 8 }],
    queryFn: () =>
      apiClient.getProducts({
        is_featured: true,
        page_size: 8,
      }),
  });

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: () => apiClient.getCategories(),
  });

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.3,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 },
    },
  };

  return (
    <div className="w-full">
      {/* Hero Section */}
      <section className="relative min-h-[90vh] flex items-center overflow-hidden">
        {/* Background Gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 via-transparent to-violet-500/20 dark:from-blue-500/10 dark:via-transparent dark:to-violet-500/10" />

        {/* Animated shapes */}
        <motion.div
          className="absolute top-10 left-10 w-72 h-72 bg-blue-400/30 rounded-full blur-3xl"
          animate={{ y: [0, 50, 0] }}
          transition={{ duration: 8, repeat: Infinity }}
        />
        <motion.div
          className="absolute bottom-20 right-20 w-72 h-72 bg-violet-400/30 rounded-full blur-3xl"
          animate={{ y: [0, -50, 0] }}
          transition={{ duration: 8, repeat: Infinity, delay: 1 }}
        />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-32">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <motion.h1
                className="text-5xl md:text-6xl lg:text-7xl font-bold leading-tight mb-6"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2, duration: 0.8 }}
              >
                <span className="text-gray-900 dark:text-white">Your Premium</span>
                <br />
                <span className="gradient-text">Shopping Experience</span>
              </motion.h1>

              <motion.p
                className="text-lg text-gray-600 dark:text-gray-400 mb-8 max-w-lg"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4, duration: 0.8 }}
              >
                Discover curated products, amazing deals, and seamless checkout. Shop smart, shop fast, shop with us.
              </motion.p>

              <motion.div
                className="flex flex-wrap gap-4"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6, duration: 0.8 }}
              >
                <Link
                  to="/shop"
                  className="group px-8 py-4 bg-gradient-to-r from-blue-500 to-violet-600 text-white rounded-xl font-semibold hover:shadow-glow transition-all duration-300 flex items-center gap-2"
                >
                  Shop Now
                  <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Link>
                <button className="px-8 py-4 border-2 border-gray-900 dark:border-white rounded-xl font-semibold hover:bg-gray-900 hover:text-white dark:hover:bg-white dark:hover:text-gray-900 transition-all duration-300">
                  Watch Demo
                </button>
              </motion.div>
            </motion.div>

            {/* Right - Featured Product Card */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="relative"
            >
              <motion.div
                className="relative aspect-square rounded-2xl bg-gradient-to-br from-blue-500/20 to-violet-500/20 p-8 glass-md"
                whileHover={{ scale: 1.05 }}
                transition={{ duration: 0.5 }}
              >
                <div className="w-full h-full bg-gray-300 dark:bg-gray-700 rounded-lg animate-pulse flex items-center justify-center">
                  <span className="text-gray-600 dark:text-gray-400">Featured Product</span>
                </div>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              { icon: Zap, title: 'Fast Checkout', desc: 'Complete your purchase in seconds' },
              { icon: Truck, title: 'Free Shipping', desc: 'On orders over $50' },
              { icon: Shield, title: 'Secure Payment', desc: 'Powered by Stripe' },
              { icon: RotateCcw, title: 'Easy Returns', desc: '30-day return policy' },
            ].map((feature, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="text-center"
              >
                <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-blue-500/20 to-violet-500/20 rounded-xl flex items-center justify-center">
                  <feature.icon className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                </div>
                <h3 className="font-semibold text-lg mb-2">{feature.title}</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories Section */}
      {categories && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center mb-12">
              <div>
                <h2 className="text-3xl md:text-4xl font-bold mb-2">Shop by Category</h2>
                <p className="text-gray-600 dark:text-gray-400">Browse our curated collections</p>
              </div>
              <Link to="/shop" className="text-blue-600 dark:text-blue-400 hover:text-blue-700 font-semibold flex items-center gap-2">
                View All <ChevronRight className="w-4 h-4" />
              </Link>
            </div>

            <motion.div
              className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4"
              variants={containerVariants}
              initial="hidden"
              whileInView="visible"
            >
              {categories.slice(0, 5).map((category) => (
                <motion.div key={category.id} variants={itemVariants}>
                  <Link to={`/shop?category=${category.id}`}>
                    <div className="aspect-square rounded-xl bg-gradient-to-br from-blue-500/20 to-violet-500/20 hover:from-blue-500/30 hover:to-violet-500/30 flex items-center justify-center transition-all duration-300 cursor-pointer group">
                      <h3 className="font-semibold text-center px-4 group-hover:scale-110 transition-transform">
                        {category.name}
                      </h3>
                    </div>
                  </Link>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </section>
      )}

      {/* Featured Products */}
      <section className="py-16 border-t border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-12">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-2">Featured Products</h2>
              <p className="text-gray-600 dark:text-gray-400">Handpicked items just for you</p>
            </div>
            <Link to="/shop" className="text-blue-600 dark:text-blue-400 hover:text-blue-700 font-semibold flex items-center gap-2">
              View All <ChevronRight className="w-4 h-4" />
            </Link>
          </div>

          {isLoading ? (
            <ProductGridSkeleton count={8} />
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {products?.map((product, idx) => (
                <ProductCard key={product.id} product={product} index={idx} />
              ))}
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 border-t border-gray-200 dark:border-gray-800 bg-gradient-to-r from-blue-500/20 via-violet-500/20 to-pink-500/20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.h2
            className="text-4xl md:text-5xl font-bold mb-6"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
          >
            Ready to Shop?
          </motion.h2>
          <motion.p
            className="text-lg text-gray-600 dark:text-gray-400 mb-8"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            Explore thousands of products with unbeatable prices and amazing customer service.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Link
              to="/shop"
              className="inline-block px-8 py-4 bg-gradient-to-r from-blue-500 to-violet-600 text-white rounded-xl font-semibold hover:shadow-glow transition-all duration-300"
            >
              Start Shopping Now
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  );
}


