import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import Navbar from "../../components/Navbar/Navbar";
import products from "../../data/products";
import "../Home/Home.css";
import "./ProductDetails.css";

function createRating(product, user, stars, review) {
  return {
    productId: product.id,
    email: user?.email || "guest",
    name: user?.name || "Customer",
    stars,
    review: review.trim(),
    date: new Date().toLocaleDateString("en-IN"),
  };
}

function ProductDetails() {
  const { id } = useParams();
  const product = products.find((item) => item.id === Number(id));
  const [wishlist, setWishlist] = useState(() => JSON.parse(localStorage.getItem("wishlist") || "[]"));
  const [ratings, setRatings] = useState(() => JSON.parse(localStorage.getItem("ratings") || "[]"));
  const [selectedRating, setSelectedRating] = useState(0);
  const [reviewText, setReviewText] = useState("");
  const user = JSON.parse(localStorage.getItem("user") || "null");
  const isSaved = product ? wishlist.some((item) => item.id === product.id) : false;
  const productRatings = product ? ratings.filter((rating) => rating.productId === product.id) : [];
  const averageRating = productRatings.length
    ? (productRatings.reduce((total, rating) => total + rating.stars, 0) / productRatings.length).toFixed(1)
    : null;

  function toggleWishlist() {
    const updatedWishlist = isSaved
      ? wishlist.filter((item) => item.id !== product.id)
      : [...wishlist, product];
    localStorage.setItem("wishlist", JSON.stringify(updatedWishlist));
    setWishlist(updatedWishlist);
  }

  function addToCart() {
    const cart = JSON.parse(localStorage.getItem("cart") || "[]");
    const existingProduct = cart.find((item) => item.id === product.id);
    if (existingProduct) existingProduct.quantity += 1;
    else cart.push({ ...product, quantity: 1 });
    localStorage.setItem("cart", JSON.stringify(cart));
    alert(`${product.name} added to cart`);
  }

  function submitRating(event) {
    event.preventDefault();
    if (selectedRating === 0) {
      alert("Please choose a star rating");
      return;
    }

    const newRating = createRating(product, user, selectedRating, reviewText);
    const updatedRatings = [
      ...ratings.filter((rating) => !(rating.productId === product.id && rating.email === newRating.email)),
      newRating,
    ];
    localStorage.setItem("ratings", JSON.stringify(updatedRatings));
    setRatings(updatedRatings);
    setReviewText("");
    alert("Thanks for rating this product");
  }

  if (!product) return <><Navbar /><main className="page"><h1>Product not found</h1><Link to="/home">Back to products</Link></main></>;

  return (
    <>
      <Navbar />
      <main className="page details-page">
        <img src={product.image} alt={product.name} />
        <section>
          <p>{product.category}</p>
          <h1>{product.name}</h1>
          <h2>₹{product.price.toLocaleString("en-IN")}</h2>
          <p>{averageRating ? `★ ${averageRating} / 5 (${productRatings.length} rating${productRatings.length === 1 ? "" : "s"})` : "Not rated yet"}</p>
          <p>{product.description}</p>
          <button
            className={`details-wishlist ${isSaved ? "saved" : ""}`}
            aria-label={isSaved ? "Remove from wishlist" : "Add to wishlist"}
            aria-pressed={isSaved}
            onClick={toggleWishlist}
          >♥</button>
          <button onClick={addToCart}>Add to cart</button>
          <p><Link to="/home">Back to products</Link></p>
          <section className="rating-section">
            <h2>Rate this product</h2>
            <form onSubmit={submitRating}>
              <div className="star-picker" aria-label="Choose a rating from one to five stars">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    className={star <= selectedRating ? "star selected" : "star"}
                    type="button"
                    key={star}
                    aria-label={`${star} star${star === 1 ? "" : "s"}`}
                    onClick={() => setSelectedRating(star)}
                  >★</button>
                ))}
              </div>
              <label>Your review (optional)
                <textarea value={reviewText} onChange={(event) => setReviewText(event.target.value)} maxLength="300" />
              </label>
              <button type="submit">Submit rating</button>
            </form>
            <div className="rating-list">
              {productRatings.map((rating) => (
                <article className="rating-item" key={`${rating.email}-${rating.productId}`}>
                  <strong>{rating.name} · {"★".repeat(rating.stars)}{"☆".repeat(5 - rating.stars)}</strong>
                  <small>{rating.date}</small>
                  {rating.review && <p>{rating.review}</p>}
                </article>
              ))}
            </div>
          </section>
        </section>
      </main>
    </>
  );
}

export default ProductDetails;
