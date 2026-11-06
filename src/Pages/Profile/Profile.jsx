import { Link, useNavigate } from "react-router-dom";
import Navbar from "../../components/Navbar/Navbar";
import { useState } from "react";

function createReturnRequest(order, item, user, reason) {
  return {
    orderId: order.id,
    productId: item.id,
    productName: item.name,
    email: user?.email,
    status: "Return requested",
    reason,
    date: new Date().toLocaleDateString("en-IN"),
  };
}

function Profile() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user") || "null");
  const orders = JSON.parse(localStorage.getItem("orders") || "[]")
    .filter((order) => order.email === user?.email);
  const [wishlist, setWishlist] = useState(() => JSON.parse(localStorage.getItem("wishlist") || "[]"));
  const [returns, setReturns] = useState(() => JSON.parse(localStorage.getItem("returns") || "[]"));
  const [returningItem, setReturningItem] = useState(null);
  const [returnReason, setReturnReason] = useState("");
  const [otherReason, setOtherReason] = useState("");

  function removeWishlist(id) {
    const updatedWishlist = wishlist.filter((item) => item.id !== id);
    localStorage.setItem("wishlist", JSON.stringify(updatedWishlist));
    setWishlist(updatedWishlist);
  }

  function logout() {
    localStorage.removeItem("user");
    navigate("/");
  }

  function requestReturn(order, item) {
    const alreadyRequested = returns.some((request) =>
      request.orderId === order.id && request.productId === item.id && request.email === user?.email);
    if (alreadyRequested) return;

    if (!returnReason) {
      alert("Please choose a reason for the return.");
      return;
    }
    if (returnReason === "Other" && !otherReason.trim()) {
      alert("Please enter the return reason.");
      return;
    }

    const reason = returnReason === "Other" ? otherReason.trim() : returnReason;
    const updatedReturns = [...returns, createReturnRequest(order, item, user, reason)];
    localStorage.setItem("returns", JSON.stringify(updatedReturns));
    setReturns(updatedReturns);
    setReturningItem(null);
    setReturnReason("");
    setOtherReason("");
  }

  return (
    <>
      <Navbar />
      <main className="page">
        <h1>My profile</h1>
        <section className="profile-section">
          <h2>Account</h2>
          <p>Name: {user?.name}</p>
          <p>Email: {user?.email}</p>
          <button onClick={logout}>Logout</button>
        </section>
        <section className="profile-section">
          <h2>My orders</h2>
          {orders.length === 0 ? <p>You have not placed an order yet.</p> : orders.map((order) => (
            <article className="order-card" key={order.id}>
              <p>Order #{order.id}</p>
              <p>Date: {order.date}</p>
              <p>Total: ₹{order.total.toLocaleString("en-IN")}</p>
              <div className="ordered-products">
                {order.products.map((item) => {
                  const returnRequest = returns.find((request) =>
                    request.orderId === order.id && request.productId === item.id && request.email === user?.email);
                  return (
                    <div className="ordered-product" key={item.id}>
                      <span>{item.name} × {item.quantity}</span>
                      {returnRequest ? (
                        <span className="return-status">
                          {returnRequest.status} ({returnRequest.date})
                          {returnRequest.reason && <small>Reason: {returnRequest.reason}</small>}
                        </span>
                      ) : (
                        returningItem === `${order.id}-${item.id}` ? (
                          <form className="return-form" onSubmit={(event) => { event.preventDefault(); requestReturn(order, item); }}>
                            <label>Why are you returning this item?
                              <select value={returnReason} onChange={(event) => setReturnReason(event.target.value)} required>
                                <option value="">Choose a reason</option>
                                <option value="Product damaged">Product damaged</option>
                                <option value="Parcel damaged">Parcel damaged</option>
                                <option value="Poor delivery experience">Poor delivery experience</option>
                                <option value="Different product delivered">Different product delivered</option>
                                <option value="Other">Other</option>
                              </select>
                            </label>
                            {returnReason === "Other" && (
                              <label>Tell us the reason
                                <input value={otherReason} onChange={(event) => setOtherReason(event.target.value)} required />
                              </label>
                            )}
                            <div className="return-form-actions">
                              <button type="submit">Send return request</button>
                              <button type="button" className="secondary-button" onClick={() => { setReturningItem(null); setReturnReason(""); setOtherReason(""); }}>Cancel</button>
                            </div>
                          </form>
                        ) : (
                          <button className="secondary-button" onClick={() => setReturningItem(`${order.id}-${item.id}`)}>Return</button>
                        )
                      )}
                    </div>
                  );
                })}
              </div>
            </article>
          ))}
        </section>
        <section className="profile-section">
          <h2>Wishlist</h2>
          {wishlist.length === 0 ? <p>Your wishlist is empty.</p> : wishlist.map((item) => (
            <article className="wishlist-item" key={item.id}>
              <Link to={`/product/${item.id}`}>{item.name}</Link>
              <span>₹{item.price.toLocaleString("en-IN")}</span>
              <button className="secondary-button" onClick={() => removeWishlist(item.id)}>Remove</button>
            </article>
          ))}
        </section>
      </main>
    </>
  );
}

export default Profile;
