import { Link } from "react-router-dom";
import { useState } from "react";

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  function resetPassword(event) {
    event.preventDefault();
    const users = JSON.parse(localStorage.getItem("users") || "[]");
    const index = users.findIndex((user) => user.email === email.trim().toLowerCase());
    if (index === -1) {
      setMessage("No account was found with that email.");
      return;
    }
    users[index].password = password;
    localStorage.setItem("users", JSON.stringify(users));
    setMessage("Password changed. You can now log in.");
  }

  return (
    <main className="auth-container">
      <form className="simple-form" onSubmit={resetPassword}>
        <h1>Reset password</h1>
        {message && <p>{message}</p>}
        <label>Email<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required /></label>
        <label>New password<input type="password" minLength="6" value={password} onChange={(event) => setPassword(event.target.value)} required /></label>
        <button type="submit">Save new password</button>
        <p><Link to="/">Back to login</Link></p>
      </form>
    </main>
  );
}

export default ForgotPassword;
