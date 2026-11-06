import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../../components/Navbar/Navbar";
import products from "../../data/products";
import "./Home.css";

function Home() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");
  const [wishlist, setWishlist] = useState(() => JSON.parse(localStorage.getItem("wishlist") || "[]"));
  const categories = ["All", ...new Set(products.map((product) => product.category))];
  const filteredProducts = products.filter((product) => {
    const matchesSearch = product.name.toLowerCase().includes(search.toLowerCase());
    const matchesCategory = category === "All" || product.category === category;
    return matchesSearch && matchesCategory;
  });

  function addToCart(product) {
    const cart = JSON.parse(localStorage.getItem("cart") || "[]");
    const existingProduct = cart.find((item) => item.id === product.id);
    if (existingProduct) existingProduct.quantity += 1;
    else cart.push({ ...product, quantity: 1 });
    localStorage.setItem("cart", JSON.stringify(cart));
    alert(`${product.name} added to cart`);
  }

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
        <h1>Shop our products</h1>
        <p>Browse our collection, choose what you need, and place your order online.</p>
        <div className="filters">
          <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search products" aria-label="Search products" />
          <select value={category} onChange={(event) => setCategory(event.target.value)} aria-label="Filter by category">
            {categories.map((item) => <option key={item}>{item}</option>)}
          </select>
        </div>
        <div className="products">
          {filteredProducts.map((product) => (
            <article
              className="product-card"
              key={product.id}
              role="link"
              tabIndex={0}
              onClick={() => navigate(`/product/${product.id}`)}
              onKeyDown={(event) => {
                if (event.target !== event.currentTarget) return;
                if (event.key === "Enter" || event.key === " ") navigate(`/product/${product.id}`);
              }}
            >
              <div className="product-image-wrap">
                <img src={product.image} alt={product.name} />
                <button
                  className={`wishlist-heart ${wishlist.some((item) => item.id === product.id) ? "saved" : ""}`}
                  aria-label={wishlist.some((item) => item.id === product.id) ? "Remove from wishlist" : "Add to wishlist"}
                  aria-pressed={wishlist.some((item) => item.id === product.id)}
                  onClick={(event) => { event.stopPropagation(); toggleWishlist(product); }}
                >♥</button>
              </div>
              <p>{product.category}</p>
              <h2>{product.name}</h2>
              <strong>₹{product.price.toLocaleString("en-IN")}</strong>
              <div className="card-actions">
                <button onClick={(event) => { event.stopPropagation(); addToCart(product); }}>Add to cart</button>
              </div>
            </article>
          ))}
          {filteredProducts.length === 0 && <p>No products found.</p>}
        </div>
      </main>
    </>
  );
}

export default Home;
