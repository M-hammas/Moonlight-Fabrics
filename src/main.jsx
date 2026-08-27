import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import ErrorBoundary from "./components/common/ErrorBoundary";
import { AuthProvider } from "./context/AuthContext";
import { ProductProvider } from "./context/ProductContext";
import { CartProvider } from "./context/CartContext";
import { WishlistProvider } from "./context/WishlistContext";
import "./assets/styles/variables.css";
import "./assets/styles/global.css";
import "./assets/styles/animations.css";

const root = document.getElementById("root");

if (!root) {
  throw new Error('Sidra Fabrics startup failed: the root element "#root" is missing from index.html.');
}

ReactDOM.createRoot(root).render(
  <React.StrictMode>
    <ErrorBoundary>
      <AuthProvider>
        <ProductProvider>
          <CartProvider>
            <WishlistProvider>
              <App />
            </WishlistProvider>
          </CartProvider>
        </ProductProvider>
      </AuthProvider>
    </ErrorBoundary>
  </React.StrictMode>
);
