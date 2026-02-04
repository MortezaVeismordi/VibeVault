# E-Commerce Frontend

A modern, showcase-quality React 19 frontend for the E-Commerce platform built with Vite, TypeScript, Tailwind CSS, and Framer Motion.

## 🚀 Tech Stack

- **React 19** - Latest React with concurrent features
- **Vite 7** - Ultra-fast build tool
- **TypeScript** - Full type safety
- **Tailwind CSS v4** - Utility-first styling with plugins
- **Framer Motion** - Smooth animations and transitions
- **@tanstack/react-query** - Data fetching and caching (React 19 compatible)
- **Zustand** - Lightweight state management with persistence
- **React Router DOM v6** - Client-side routing
- **Axios** - HTTP client with interceptors
- **Lucide React** - Icon library
- **React Hot Toast** - Toast notifications

## 📦 Features

### Pages
- **Home** - Hero section, featured products, categories carousel
- **Shop** - Product listing with filters, search, pagination
- **Product Detail** - Image gallery, variants, add to cart
- **Cart** - Shopping cart with item management and checkout
- **Checkout** - Payment processing redirect to Stripe
- **Orders** - Order history and details
- **Payment Success/Cancel** - Order confirmation pages
- **404** - Not found page

### Components
- **Navbar** - Sticky header with dark mode toggle, search, cart icon
- **Footer** - Multi-section footer with newsletter, social links
- **ProductCard** - Reusable product display with animations
- **LoadingSkeleton** - Shimmer loading states

### Features
- ✅ Full dark/light mode support
- ✅ Responsive mobile-first design
- ✅ Smooth Framer Motion animations
- ✅ State persistence with Zustand
- ✅ Real-time cart updates
- ✅ API integration with auth handling
- ✅ Loading skeletons with shimmer effects
- ✅ Toast notifications
- ✅ TypeScript type safety

## 🛠️ Setup Instructions

### Prerequisites
- Node.js 18+ and npm

### Installation

1. **Install dependencies**
```bash
npm install
```

2. **Create environment file** (already provided as .env.local)
```bash
cp .env.example .env.local
```

3. **Update API URL** if backend runs on different port
```env
VITE_API_URL=http://localhost:8000/api
```

### Development

Start the development server:
```bash
npm run dev
```

Access at: http://localhost:5173

### Production Build

Build for production:
```bash
npm run build
```

Preview build locally:
```bash
npm run preview
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable components
│   │   ├── Navbar.tsx
│   │   ├── Footer.tsx
│   │   ├── Layout.tsx
│   │   ├── ProductCard.tsx
│   │   └── LoadingSkeleton.tsx
│   ├── pages/              # Page components
│   │   ├── Home.tsx
│   │   ├── Shop.tsx
│   │   ├── ProductDetail.tsx
│   │   ├── Cart.tsx
│   │   ├── Checkout.tsx
│   │   ├── Orders.tsx
│   │   ├── OrderSuccess.tsx
│   │   ├── OrderCancel.tsx
│   │   └── NotFound.tsx
│   ├── hooks/              # Custom React hooks
│   │   └── useApi.ts
│   ├── lib/                # Utilities and API client
│   │   └── api.ts
│   ├── store/              # Zustand state management
│   │   └── cartStore.ts
│   ├── types/              # TypeScript interfaces
│   │   └── index.ts
│   ├── App.tsx             # Main app with routing
│   ├── main.tsx            # React entry point
│   └── index.css           # Global styles with Tailwind
├── tailwind.config.js      # Tailwind customizations
├── postcss.config.js       # PostCSS configuration
├── package.json
└── README-DETAILED.md
```

## 🎨 Styling

### Tailwind CSS Configuration
- Custom color variables (primary blue, secondary violet)
- Extended animations (fadeIn, slideUp, slideDown, etc.)
- Dark mode support with class strategy
- Glass morphism utilities
- Glow shadow effects

### Dark Mode
Automatically detected from system preferences, can be toggled via navbar button.

## 🔌 API Integration

### API Client
Located in `src/lib/api.ts` with the following features:
- Axios instance with base URL configuration from env
- Request interceptors for auth token injection
- Response interceptors for error handling
- Automatic logout on 401 responses
- Token storage in localStorage

### Available Methods
```typescript
// Products
getProducts(filters?: object) // Get products with filters
getProduct(id: number) // Get single product details

// Categories
getCategories() // Get all categories

// Cart
getCart() // Get current cart
addToCart(productId, quantity) // Add item to cart
updateCartItem(itemId, quantity) // Update cart item quantity
removeFromCart(itemId) // Remove item from cart
clearCart() // Clear entire cart

// Orders
getOrders() // Get user's orders
getOrder(id) // Get order details

// Authentication
login(email, password) // User login
register(data) // User registration
logout() // User logout
getCurrentUser() // Get logged-in user
isAuthenticated() // Check auth status

// Payment
createCheckoutSession() // Create Stripe checkout session
getPaymentStatus(sessionId) // Get payment status
```

## 🪝 Custom Hooks

Located in `src/hooks/useApi.ts`:

```typescript
// Query hooks
useProducts(filters)  // Fetch products with caching
useProduct(id)        // Fetch single product
useCategories()       // Fetch categories
useGetOrders()        // Fetch user orders
useGetOrder(id)       // Fetch order details

// Mutation hooks
useCreateCheckout()   // Create checkout session
useLogin()            // Login mutation
useRegister()         // Register mutation
```

## 🎯 State Management

### Zustand Cart Store
Located in `src/store/cartStore.ts`:

```typescript
// State
items         // Cart items array
total         // Total price
itemCount     // Number of items
isLoading     // Loading state
error         // Error message

// Actions
fetchCart()           // Fetch cart from API
addItem(product, qty) // Add item to cart
updateItem(id, qty)   // Update item quantity
removeItem(id)        // Remove item
clearCart()           // Clear all items
setItems(items)       // Set items directly
```

## 🔐 Authentication

- User authentication via API
- Token stored in localStorage
- Automatic token injection in requests
- Auto-logout on unauthorized responses
- Protected routes (future enhancement)

## 🚦 Loading States

Shimmer loading skeletons for:
- Product cards
- Product grids
- Product detail page
- Order lists

## 📝 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| VITE_API_URL | http://localhost:8000/api | Backend API base URL |
| VITE_APP_NAME | ProShop | Application name |

## 🐛 Troubleshooting

### Port Already in Use
If port 5173 is already in use:
```bash
npm run dev -- --port 5174
```

### API Connection Issues
1. Ensure backend is running on configured URL
2. Check VITE_API_URL in .env.local
3. Verify CORS is enabled in backend

### Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

## 📱 Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

## 🔄 Development Workflow

1. **Feature Branch**
   ```bash
   git checkout -b feature/feature-name
   ```

2. **Development**
   - Start dev server: `npm run dev`
   - Make changes with HMR reloading
   - Test across browsers and responsive sizes

3. **Build & Test**
   ```bash
   npm run build
   npm run preview
   ```

4. **Commit & Push**
   ```bash
   git add .
   git commit -m "feat: description"
   git push origin feature/feature-name
   ```

## 🎬 Getting Started

1. Ensure Django backend is running on http://localhost:8000
2. Start frontend: `npm run dev`
3. Open http://localhost:5173 in browser
4. Explore the application!

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check component props and types in source code

## 📄 License

This project is part of the E-Commerce platform.

---

**Happy Coding! 🚀**
