import { useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "../../components/Navbar/Navbar";
import products from "../../data/products";
import "../Home/Home.css";
import "./Category.css";

function Category() {
  const [wishlist, setWishlist] = useState(() => JSON.parse(localStorage.getItem("wishlist") || "[]"));
  const categories = [...new Set(products.map((product) => product.category))];

  function toggleWishlist(product) {
    const isSaved = wishlist.some((item) => item.id === product.id);
    const updatedWishlist = isSaved
      ? wishlist.filter((item) => item.id !== product.id)
      : [...wishlist, product];
    localStorage.setItem("wishlist", JSON.stringify(updatedWishlist));
    setWishlist(updatedWishlist);
  }

  return (
    <>
      <Navbar />
      <main className="page">
        <h1>Our product categories</h1>
        <p>Browse our products by category.</p>
        {categories.map((category) => (
          <section className="category-section" key={category}>
            <h2>{category}</h2>
            <div className="products">
              {products.filter((product) => product.category === category).map((product) => (
                <article className="card category-product-card" key={product.id}>
                  <Link to={`/product/${product.id}`}>
                    <img src={product.image} alt={product.name} />
                    <h3>{product.name}</h3>
                    <p>₹{product.price.toLocaleString("en-IN")}</p>
                  </Link>
                  <button
                    className={`wishlist-heart ${wishlist.some((item) => item.id === product.id) ? "saved" : ""}`}
                    aria-label={wishlist.some((item) => item.id === product.id) ? "Remove from wishlist" : "Add to wishlist"}
                    aria-pressed={wishlist.some((item) => item.id === product.id)}
                    onClick={() => toggleWishlist(product)}
                  >♥</button>
                </article>
              ))}
            </div>
          </section>
        ))}
      </main>
    </>
  );
}

export default Category;
