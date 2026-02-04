import { motion } from 'framer-motion';

export function ProductCardSkeleton() {
  return (
    <motion.div animate={{ opacity: [0.6, 1, 0.6] }} transition={{ duration: 2, repeat: Infinity }}>
      <div className="rounded-xl bg-gray-200 dark:bg-gray-800 aspect-square mb-4" />
      <div className="space-y-3">
        <div className="h-4 bg-gray-200 dark:bg-gray-800 rounded w-24" />
        <div className="h-6 bg-gray-200 dark:bg-gray-800 rounded" />
        <div className="h-4 bg-gray-200 dark:bg-gray-800 rounded w-32" />
        <div className="h-10 bg-gray-200 dark:bg-gray-800 rounded" />
      </div>
    </motion.div>
  );
}

export function ProductGridSkeleton({ count = 8 }: { count?: number }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      {[...Array(count)].map((_, i) => (
        <ProductCardSkeleton key={i} />
      ))}
    </div>
  );
}


