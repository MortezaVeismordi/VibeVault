import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Loader } from 'lucide-react';

export function Checkout() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'loading' | 'error'>('loading');
  const sessionId = searchParams.get('session_id');

  useEffect(() => {
    // Simulate checkout processing
    if (!sessionId) {
      setStatus('error');
      setTimeout(() => navigate('/cart'), 3000);
      return;
    }

    // In real scenario, this would verify the session with backend
    const timer = setTimeout(() => {
      navigate(`/payment/success?order_id=${sessionId}`);
    }, 3000);

    return () => clearTimeout(timer);
  }, [sessionId, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center"
      >
        {status === 'loading' ? (
          <>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
              className="inline-block mb-4"
            >
              <Loader className="w-16 h-16 text-blue-600 dark:text-blue-400" />
            </motion.div>
            <h1 className="text-3xl font-bold mb-2">Processing Checkout</h1>
            <p className="text-gray-600 dark:text-gray-400">
              Please wait while we process your payment...
            </p>
          </>
        ) : (
          <>
            <h1 className="text-3xl font-bold mb-2 text-red-600">Checkout Error</h1>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Something went wrong. Redirecting to cart...
            </p>
          </>
        )}
      </motion.div>
    </div>
  );
}


