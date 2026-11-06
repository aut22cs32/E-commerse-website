import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");

  function updateForm(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  function register(event) {
    event.preventDefault();
    const users = JSON.parse(localStorage.getItem("users") || "[]");
    const email = form.email.trim().toLowerCase();
    if (users.some((user) => user.email === email)) {
      setError("An account already uses this email.");
      return;
    }
    const newUser = { ...form, name: form.name.trim(), email };
    localStorage.setItem("users", JSON.stringify([...users, newUser]));
    localStorage.setItem("user", JSON.stringify({ name: newUser.name, email }));
    navigate("/home");
  }

  return (
    <main className="auth-container">
      <form className="simple-form" onSubmit={register}>
        <h1>Create account</h1>
        {error && <p className="error-message">{error}</p>}
        <label>Name<input name="name" value={form.name} onChange={updateForm} required /></label>
        <label>Email<input name="email" type="email" value={form.email} onChange={updateForm} required /></label>
        <label>Password<input name="password" type="password" minLength="6" value={form.password} onChange={updateForm} required /></label>
        <button type="submit">Register</button>
        <p>Already registered? <Link to="/">Login</Link></p>
      </form>
    </main>
  );
}

export default Register;
