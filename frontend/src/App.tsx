import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClientProvider, QueryClient } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { Home } from './pages/Home';
import { useEffect } from 'react';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      gcTime: 1000 * 60 * 10,
    },
  },
});

function App() {
  useEffect(() => {
    console.log('App mounted');
  }, []);

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#030712', color: 'white' }}>
      <QueryClientProvider client={queryClient}>
        <Router>
          <Routes>
            <Route path="/" element={<Home />} />
          </Routes>
        </Router>
        <Toaster position="top-right" />
      </QueryClientProvider>
    </div>
  );
}

export default App;


