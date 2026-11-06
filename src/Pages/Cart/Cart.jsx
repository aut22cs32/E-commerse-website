import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "../../components/Navbar/Navbar";

function Cart() {
  const navigate = useNavigate();
  const [cart, setCart] = useState(() => JSON.parse(localStorage.getItem("cart") || "[]"));
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  function saveCart(updatedCart) {
    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  }

  function changeQuantity(id, change) {
    const updatedCart = cart.map((item) => item.id === id
      ? { ...item, quantity: Math.max(1, item.quantity + change) }
      : item);
    saveCart(updatedCart);
  }

  function removeItem(id) {
    saveCart(cart.filter((item) => item.id !== id));
  }

  return (
    <>
      <Navbar />
      <main className="page">
        <h1>Shopping cart</h1>
        {cart.length === 0 ? (
          <p>Your cart is empty. <Link to="/home">Browse products</Link></p>
        ) : (
          <>
            {cart.map((item) => (
              <div className="cart-item" key={item.id}>
                <img src={item.image} alt={item.name} />
                <div><h2>{item.name}</h2><p>₹{item.price.toLocaleString("en-IN")}</p></div>
                <div className="quantity-buttons">
                  <button onClick={() => changeQuantity(item.id, -1)} aria-label="Decrease quantity">−</button>
                  <span>{item.quantity}</span>
                  <button onClick={() => changeQuantity(item.id, 1)} aria-label="Increase quantity">+</button>
                </div>
                <button className="secondary-button" onClick={() => removeItem(item.id)}>Remove</button>
              </div>
            ))}
            <h2>Total: ₹{total.toLocaleString("en-IN")}</h2>
            <button onClick={() => navigate("/checkout")}>Go to checkout</button>
          </>
        )}
      </main>
    </>
  );
}

export default Cart;
