import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  function login(event) {
    event.preventDefault();
    const users = JSON.parse(localStorage.getItem("users") || "[]");
    const user = users.find((item) => item.email === email.trim().toLowerCase() && item.password === password);
    if (!user) {
      setError("Email or password is incorrect.");
      return;
    }
    localStorage.setItem("user", JSON.stringify({ name: user.name, email: user.email }));
    navigate("/home");
  }

  return (
    <main className="auth-container">
      <form className="simple-form" onSubmit={login}>
        <h1>Login</h1>
        {error && <p className="error-message">{error}</p>}
        <label>Email<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required /></label>
        <label>Password<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required /></label>
        <button type="submit">Login</button>
        <p>New user? <Link to="/register">Create an account</Link></p>
        <p><Link to="/forgot-password">Forgot password?</Link></p>
      </form>
    </main>
  );
}

export default Login;
