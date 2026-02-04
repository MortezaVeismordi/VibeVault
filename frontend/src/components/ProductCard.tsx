import { ShoppingCart, Star, Heart } from 'lucide-react';
import { motion } from 'framer-motion';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useCartStore } from '../store/cartStore';
import toast from 'react-hot-toast';

interface ProductCardProps {
  product: any;
  index?: number;
}

export function ProductCard({ product, index = 0 }: ProductCardProps) {
  const [isFavorite, setIsFavorite] = useState(false);
  const [isAddingToCart, setIsAddingToCart] = useState(false);
  const addItem = useCartStore((state) => state.addItem);
  
  const primaryImage = product.images?.[0]?.image || '/placeholder.jpg';
  const hasDiscount = product.discount_price && parseFloat(product.discount_price) < parseFloat(product.price);
  const discountPercent = hasDiscount 
    ? Math.round(((parseFloat(product.price) - parseFloat(product.discount_price)) / parseFloat(product.price)) * 100)
    : 0;

  const handleAddToCart = async () => {
    setIsAddingToCart(true);
    try {
      await addItem(product, 1);
      toast.success('Added to cart!');
    } catch (error) {
      toast.error('Failed to add to cart');
    } finally {
      setIsAddingToCart(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
      className="group"
    >
      <Link to={`/product/${product.id}`}>
        <div className="relative overflow-hidden rounded-xl bg-gray-100 dark:bg-gray-800 aspect-square mb-4">
          {/* Image */}
          <motion.img
            src={primaryImage}
            alt={product.name}
            className="w-full h-full object-cover group-hover:scale-110 transition-all duration-300 duration-500"
            whileHover={{ scale: 1.1 }}
          />

          {/* Badge */}
          {product.is_featured && (
            <div className="absolute top-3 left-3 bg-gradient-to-r from-blue-500 to-violet-600 text-white px-3 py-1 rounded-full text-xs font-semibold">
              Featured
            </div>
          )}

          {hasDiscount && (
            <div className="absolute top-3 right-3 bg-red-500 text-white px-3 py-1 rounded-full text-xs font-semibold">
              -{discountPercent}%
            </div>
          )}

          {/* Favorite Button */}
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={(e) => {
              e.preventDefault();
              setIsFavorite(!isFavorite);
            }}
            className="absolute bottom-3 right-3 p-2 bg-white/90 dark:bg-gray-900/90 rounded-full hover:bg-white dark:hover:bg-gray-800 transition-all duration-300"
          >
            <Heart
              className={`w-5 h-5 ${isFavorite ? 'fill-red-500 text-red-500' : 'text-gray-600 dark:text-gray-400'}`}
            />
          </motion.button>
        </div>
      </Link>

      {/* Info */}
      <div>
        <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wider">
          {typeof product.category === 'object' ? product.category.name : 'Category'}
        </p>
        <Link to={`/product/${product.id}`}>
          <h3 className="font-semibold text-lg line-clamp-2 group-hover:text-blue-500 transition-all duration-300">
            {product.name}
          </h3>
        </Link>

        {/* Rating */}
        {product.rating && (
          <div className="flex items-center gap-2 my-2">
            <div className="flex">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={`w-4 h-4 ${
                    i < Math.round(product.rating || 0)
                      ? 'fill-yellow-400 text-yellow-400'
                      : 'text-gray-300 dark:text-gray-600'
                  }`}
                />
              ))}
            </div>
            <span className="text-xs text-gray-500 dark:text-gray-400">
              ({product.review_count || 0})
            </span>
          </div>
        )}

        {/* Price */}
        <div className="flex items-center gap-2 mb-3">
          {hasDiscount ? (
            <>
              <span className="font-bold text-lg">${product.discount_price}</span>
              <span className="text-sm text-gray-500 dark:text-gray-400 line-through">
                ${product.price}
              </span>
            </>
          ) : (
            <span className="font-bold text-lg">${product.price}</span>
          )}
        </div>

        {/* Stock Status */}
        <div className="mb-3">
          {product.stock > 0 ? (
            <p className="text-xs text-green-600 dark:text-green-400 font-semibold">In Stock</p>
          ) : (
            <p className="text-xs text-red-600 dark:text-red-400 font-semibold">Out of Stock</p>
          )}
        </div>

        {/* Add to Cart Button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleAddToCart}
          disabled={product.stock === 0 || isAddingToCart}
          className="w-full py-2 bg-gradient-to-r from-blue-500 to-violet-600 text-white rounded-lg font-semibold hover:shadow-glow transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <ShoppingCart className="w-4 h-4" />
          {isAddingToCart ? 'Adding...' : 'Add to Cart'}
        </motion.button>
      </div>
    </motion.div>
  );
}


