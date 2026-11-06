import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "../../components/Navbar/Navbar";

function createOrder(form, user, cart, total) {
  return {
    id: Date.now(),
    email: user?.email,
    name: form.name,
    address: form.address,
    phone: form.phone,
    products: cart,
    total,
    date: new Date().toLocaleDateString("en-IN"),
  };
}

function Checkout() {
  const navigate = useNavigate();
  const cart = JSON.parse(localStorage.getItem("cart") || "[]");
  const user = JSON.parse(localStorage.getItem("user") || "null");
  const [form, setForm] = useState({ name: user?.name || "", address: "", phone: "" });
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  function updateForm(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  function placeOrder(event) {
    event.preventDefault();
    if (cart.length === 0) return;
    if (!/^\d{10}$/.test(form.phone)) {
      alert("Enter a valid 10 digit phone number");
      return;
    }
    const orders = JSON.parse(localStorage.getItem("orders") || "[]");
    const order = createOrder(form, user, cart, total);
    localStorage.setItem("orders", JSON.stringify([order, ...orders]));
    localStorage.setItem("lastOrder", JSON.stringify(order));
    localStorage.removeItem("cart");
    navigate("/order-success");
  }

  return (
    <>
      <Navbar />
      <main className="page form-page">
        <h1>Checkout</h1>
        {cart.length === 0 ? <p>Your cart is empty. <Link to="/home">Browse products</Link></p> : (
          <>
            <p>Order total: ₹{total.toLocaleString("en-IN")}</p>
            <form onSubmit={placeOrder}>
              <label>Full name<input name="name" value={form.name} onChange={updateForm} required /></label>
              <label>Address<textarea name="address" value={form.address} onChange={updateForm} required /></label>
              <label>Phone number<input name="phone" type="tel" inputMode="numeric" maxLength="10" value={form.phone} onChange={updateForm} required /></label>
              <button type="submit">Place order</button>
            </form>
          </>
        )}
      </main>
    </>
  );
}

export default Checkout;
