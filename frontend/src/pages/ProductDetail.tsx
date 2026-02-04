import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { apiClient } from '../lib/api-simple';
import { ProductGridSkeleton } from '../components/LoadingSkeleton';
import { ShoppingCart, Star, TrendingUp } from 'lucide-react';
import { useCartStore } from '../store/cartStore';
import toast from 'react-hot-toast';
import { useState } from 'react';

export function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const [quantity, setQuantity] = useState(1);
  const [isAddingToCart, setIsAddingToCart] = useState(false);
  const addItem = useCartStore((state) => state.addItem);

  const { data: product, isLoading } = useQuery({
    queryKey: ['product', id],
    queryFn: () => apiClient.getProduct(parseInt(id!)),
    enabled: !!id,
  });

  const handleAddToCart = async () => {
    setIsAddingToCart(true);
    try {
      await addItem(product!, quantity);
      toast.success(`Added ${quantity} item(s) to cart!`);
      setQuantity(1);
    } catch (error) {
      toast.error('Failed to add to cart');
    } finally {
      setIsAddingToCart(false);
    }
  };

  if (isLoading) return <ProductGridSkeleton count={1} />;

  if (!product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-lg text-gray-600 dark:text-gray-400">Product not found</p>
      </div>
    );
  }

  const hasDiscount = product.discount_price && parseFloat(product.discount_price) < parseFloat(product.price);
  const displayPrice = hasDiscount ? product.discount_price : product.price;

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12"
        >
          {/* Product Images */}
          <div>
            <motion.div
              className="aspect-square bg-gray-100 dark:bg-gray-800 rounded-2xl overflow-hidden mb-4"
              whileHover={{ scale: 1.02 }}
            >
              <img
                src={product.images?.[0]?.image || '/placeholder.jpg'}
                alt={product.name}
                className="w-full h-full object-cover"
              />
            </motion.div>

            {/* Thumbnail Gallery */}
            {product.images && product.images.length > 1 && (
              <div className="grid grid-cols-4 gap-3">
                {product.images.map((img, idx) => (
                  <motion.button
                    key={idx}
                    whileHover={{ scale: 1.05 }}
                    className="aspect-square bg-gray-100 dark:bg-gray-800 rounded-lg overflow-hidden border-2 border-transparent hover:border-blue-500 transition-all duration-300"
                  >
                    <img
                      src={img.image}
                      alt={img.alt_text}
                      className="w-full h-full object-cover"
                    />
                  </motion.button>
                ))}
              </div>
            )}
          </div>

          {/* Product Info */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <p className="text-sm text-gray-500 dark:text-gray-400 uppercase tracking-widest mb-2">
              {typeof product.category === 'object' ? product.category.name : 'Category'}
            </p>

            <h1 className="text-4xl font-bold mb-4">{product.name}</h1>

            {/* Rating */}
            {product.rating && (
              <div className="flex items-center gap-3 mb-6">
                <div className="flex gap-1">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className={`w-5 h-5 ${
                        i < Math.round(product.rating || 0)
                          ? 'fill-yellow-400 text-yellow-400'
                          : 'text-gray-300 dark:text-gray-600'
                      }`}
                    />
                  ))}
                </div>
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {product.review_count} reviews
                </span>
              </div>
            )}

            {/* Price */}
            <div className="flex items-center gap-4 mb-6">
              <span className="text-4xl font-bold text-blue-600 dark:text-blue-400">
                ${displayPrice}
              </span>
              {hasDiscount && (
                <span className="text-lg text-gray-500 dark:text-gray-400 line-through">
                  ${product.price}
                </span>
              )}
            </div>

            {/* Description */}
            <p className="text-gray-600 dark:text-gray-400 mb-8 leading-relaxed">
              {product.description}
            </p>

            {/* Stock Status */}
            <div className="mb-6">
              {product.stock > 0 ? (
                <div className="flex items-center gap-2 text-green-600 dark:text-green-400">
                  <div className="w-2 h-2 bg-green-600 dark:bg-green-400 rounded-full" />
                  In Stock ({product.stock} available)
                </div>
              ) : (
                <div className="text-red-600 dark:text-red-400 font-semibold">
                  Out of Stock
                </div>
              )}
            </div>

            {/* Add to Cart */}
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="flex items-center border border-gray-300 dark:border-gray-700 rounded-lg">
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    className="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-800 transition-all duration-300"
                  >
                    −
                  </button>
                  <span className="px-6 py-2 border-l border-r border-gray-300 dark:border-gray-700">
                    {quantity}
                  </span>
                  <button
                    onClick={() => setQuantity(quantity + 1)}
                    className="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-800 transition-all duration-300"
                  >
                    +
                  </button>
                </div>
              </div>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleAddToCart}
                disabled={product.stock === 0 || isAddingToCart}
                className="w-full py-4 bg-gradient-to-r from-blue-500 to-violet-600 text-white rounded-xl font-semibold hover:shadow-glow transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <ShoppingCart className="w-5 h-5" />
                {isAddingToCart ? 'Adding...' : 'Add to Cart'}
              </motion.button>
            </div>

            {/* Features */}
            <div className="grid grid-cols-2 gap-4 mt-8 pt-8 border-t border-gray-200 dark:border-gray-800">
              {[
                { icon: TrendingUp, label: 'Best Seller' },
                { icon: ShoppingCart, label: 'Free Shipping' },
              ].map((feature, idx) => (
                <div key={idx} className="flex items-center gap-3">
                  <feature.icon className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                  <span className="text-sm font-medium">{feature.label}</span>
                </div>
              ))}
            </div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}


