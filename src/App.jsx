import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import Login from "./Pages/Login/Login";
import Register from "./Pages/Register/Register";
import ForgotPassword from "./Pages/ForgotPassword/ForgotPassword";
import Home from "./Pages/Home/Home";
import Category from "./Pages/Category/Category";
import ProductDetails from "./Pages/ProductDetails/ProductDetails";
import Cart from "./Pages/Cart/Cart";
import Checkout from "./Pages/Checkout/Checkout";
import OrderSuccess from "./Pages/OrderSuccess/OrderSuccess";
import Profile from "./Pages/Profile/Profile";

function ProtectedRoute({ children }) {
  return localStorage.getItem("user") ? children : <Navigate to="/" replace />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/home" element={<ProtectedRoute><Home /></ProtectedRoute>} />
        <Route path="/category" element={<ProtectedRoute><Category /></ProtectedRoute>} />
        <Route path="/product/:id" element={<ProtectedRoute><ProductDetails /></ProtectedRoute>} />
        <Route path="/cart" element={<ProtectedRoute><Cart /></ProtectedRoute>} />
        <Route path="/checkout" element={<ProtectedRoute><Checkout /></ProtectedRoute>} />
        <Route path="/order-success" element={<ProtectedRoute><OrderSuccess /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/home" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
