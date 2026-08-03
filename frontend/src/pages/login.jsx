import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../authContext";

function Login() {
  const auth = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    try {
      await auth.login(email, password);
      navigate("/dashboard");
    } catch (err) {
      setError("Login failed. Check your email and password.");
    }
  };

  return (
    <div style={{ maxWidth: 420, margin: "40px auto", padding: 24 }}>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <label style={{ display: "block", marginBottom: 12 }}>
          Email
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: "100%", marginTop: 6, padding: 8 }}
          />
        </label>

        <label style={{ display: "block", marginBottom: 12 }}>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: "100%", marginTop: 6, padding: 8 }}
          />
        </label>

        {error && (
          <div style={{ color: "crimson", marginBottom: 12 }}>{error}</div>
        )}

        <button type="submit" style={{ padding: "10px 16px" }}>
          Sign in
        </button>
      </form>

      <p style={{ marginTop: 18 }}>
        New here? <Link to="/register">Create an account</Link>
      </p>
    </div>
  );
}

export default Login;