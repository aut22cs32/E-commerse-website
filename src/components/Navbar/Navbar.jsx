import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user") || "null");

  function logout() {
    localStorage.removeItem("user");
    navigate("/");
  }

  return (
    <nav className="navbar">
      <Link className="navbar-brand" to="/home">Our Store</Link>
      <div className="nav-links">
        <Link to="/home">Home</Link>
        <Link to="/category">Categories</Link>
        <Link to="/profile">{user?.name || "Profile"}</Link>
        <Link to="/cart">Cart</Link>
        <button onClick={logout}>Logout</button>
      </div>
    </nav>
  );
}

export default Navbar;
