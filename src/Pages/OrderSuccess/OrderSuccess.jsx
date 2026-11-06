import { Link, Navigate } from "react-router-dom";
import Navbar from "../../components/Navbar/Navbar";

function OrderSuccess() {
  const order = JSON.parse(localStorage.getItem("lastOrder") || "null");
  if (!order) return <Navigate to="/home" replace />;
  return (
    <>
      <Navbar />
      <main className="page">
        <h1>Order placed successfully!</h1>
        <p>Thank you for shopping with us, {order.name}. Your order number is {order.id}.</p>
        <h2>Total: ₹{order.total.toLocaleString("en-IN")}</h2>
        <p>Delivery address: {order.address}</p>
        <Link to="/home">Continue shopping</Link>
      </main>
    </>
  );
}

export default OrderSuccess;
