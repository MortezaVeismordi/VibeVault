import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Sliders, X } from 'lucide-react';
import { apiClient } from '../lib/api-simple';
import { ProductCard } from '../components/ProductCard';
import { ProductGridSkeleton } from '../components/LoadingSkeleton';

export function Shop() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [isMobileFiltersOpen, setIsMobileFiltersOpen] = useState(false);

  const page = parseInt(searchParams.get('page') || '1');
  const search = searchParams.get('search') || '';
  const category = searchParams.get('category') || '';
  const minPrice = searchParams.get('min_price');
  const maxPrice = searchParams.get('max_price');
  const ordering = searchParams.get('ordering') || '-created_at';

  const { data: productsData, isLoading } = useQuery({
    queryKey: ['products', { page, search, category, minPrice, maxPrice, ordering }],
    queryFn: () =>
      apiClient.getProducts({
        page,
        page_size: 12,
        search: search || undefined,
        category: category ? parseInt(category) : undefined,
        min_price: minPrice ? parseFloat(minPrice) : undefined,
        max_price: maxPrice ? parseFloat(maxPrice) : undefined,
        ordering,
      }),
  });

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: () => apiClient.getCategories(),
  });

  const updateFilters = (key: string, value: string) => {
    const newParams = new URLSearchParams(searchParams);
    if (value) {
      newParams.set(key, value);
    } else {
      newParams.delete(key);
    }
    newParams.set('page', '1'); // Reset to first page
    setSearchParams(newParams);
  };

  const clearFilters = () => {
    setSearchParams(new URLSearchParams());
  };

  const totalPages = productsData ? Math.ceil(productsData.count / 12) : 1;

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Shop</h1>
          <p className="text-gray-600 dark:text-gray-400">
            {productsData?.count || 0} products found
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar - Desktop */}
          <motion.div
            className="hidden lg:block"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <FilterPanel
              categories={categories || []}
              search={search}
              category={category}
              minPrice={minPrice}
              maxPrice={maxPrice}
              ordering={ordering}
              onFilterChange={updateFilters}
              onClearFilters={clearFilters}
            />
          </motion.div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {/* Mobile Filter Toggle */}
            <div className="lg:hidden mb-6">
              <button
                onClick={() => setIsMobileFiltersOpen(!isMobileFiltersOpen)}
                className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-all duration-300"
              >
                <Sliders className="w-4 h-4" />
                Filters
              </button>
            </div>

            {/* Mobile Filters */}
            {isMobileFiltersOpen && (
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-6 p-4 border border-gray-200 dark:border-gray-800 rounded-lg bg-gray-50 dark:bg-gray-900"
              >
                <FilterPanel
                  categories={categories || []}
                  search={search}
                  category={category}
                  minPrice={minPrice}
                  maxPrice={maxPrice}
                  ordering={ordering}
                  onFilterChange={updateFilters}
                  onClearFilters={clearFilters}
                />
              </motion.div>
            )}

            {/* Products Grid */}
            {isLoading ? (
              <ProductGridSkeleton count={12} />
            ) : productsData?.results && productsData.results.length > 0 ? (
              <>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                  {productsData.results.map((product, idx) => (
                    <ProductCard
                      key={product.id}
                      product={product}
                      index={idx}
                    />
                  ))}
                </div>

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="flex justify-center gap-2 flex-wrap">
                    {Array.from({ length: totalPages }).map((_, i) => (
                      <button
                        key={i + 1}
                        onClick={() => updateFilters('page', String(i + 1))}
                        className={`px-4 py-2 rounded-lg transition-all duration-300 ${
                          page === i + 1
                            ? 'bg-blue-500 text-white'
                            : 'border border-gray-300 dark:border-gray-700 hover:border-blue-500'
                        }`}
                      >
                        {i + 1}
                      </button>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500 dark:text-gray-400 text-lg">
                  No products found. Try adjusting your filters.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

interface FilterPanelProps {
  categories: any[];
  search: string;
  category: string;
  minPrice: string | null;
  maxPrice: string | null;
  ordering: string;
  onFilterChange: (key: string, value: string) => void;
  onClearFilters: () => void;
}

function FilterPanel({
  categories,
  search,
  category,
  minPrice,
  maxPrice,
  ordering,
  onFilterChange,
  onClearFilters,
}: FilterPanelProps) {
  const hasActiveFilters = search || category || minPrice || maxPrice;

  return (
    <div className="space-y-6">
      {/* Search */}
      <div>
        <label className="block text-sm font-semibold mb-3">Search</label>
        <input
          type="text"
          value={search}
          onChange={(e) => onFilterChange('search', e.target.value)}
          placeholder="Product name..."
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 focus:outline-none focus:border-blue-500"
        />
      </div>

      {/* Categories */}
      <div>
        <label className="block text-sm font-semibold mb-3">Category</label>
        <select
          value={category}
          onChange={(e) => onFilterChange('category', e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 focus:outline-none focus:border-blue-500"
        >
          <option value="">All Categories</option>
          {categories.map((cat) => (
            <option key={cat.id} value={cat.id}>
              {cat.name}
            </option>
          ))}
        </select>
      </div>

      {/* Price Range */}
      <div>
        <label className="block text-sm font-semibold mb-3">Price Range</label>
        <div className="space-y-2">
          <input
            type="number"
            value={minPrice || ''}
            onChange={(e) => onFilterChange('min_price', e.target.value)}
            placeholder="Min price"
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 focus:outline-none focus:border-blue-500 text-sm"
          />
          <input
            type="number"
            value={maxPrice || ''}
            onChange={(e) => onFilterChange('max_price', e.target.value)}
            placeholder="Max price"
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 focus:outline-none focus:border-blue-500 text-sm"
          />
        </div>
      </div>

      {/* Sorting */}
      <div>
        <label className="block text-sm font-semibold mb-3">Sort By</label>
        <select
          value={ordering}
          onChange={(e) => onFilterChange('ordering', e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 focus:outline-none focus:border-blue-500"
        >
          <option value="-created_at">Newest</option>
          <option value="price">Price: Low to High</option>
          <option value="-price">Price: High to Low</option>
          <option value="name">Name: A to Z</option>
        </select>
      </div>

      {/* Clear Filters */}
      {hasActiveFilters && (
        <button
          onClick={onClearFilters}
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-all duration-300 flex items-center justify-center gap-2"
        >
          <X className="w-4 h-4" />
          Clear Filters
        </button>
      )}
    </div>
  );
}


