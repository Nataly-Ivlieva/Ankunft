import { useState } from "react";
import { apiLogin } from "../api/auth"; // <-- исправили
import { useNavigate } from "react-router-dom";
import "../styles/auth.css";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    try {
      const session = await apiLogin(email, password);
      localStorage.setItem("token", session.token);
      localStorage.setItem("role", session.role);

            if (session.role === "admin") {
              navigate("/admin");
            } else {
              navigate("/dashboard");
            }
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Login fehlgeschlagen");
    }
  }

  return (
    <div className="auth-wrapper">
      <h2 className="auth-title">Anmeldung</h2>

      <form onSubmit={handleLogin}>
        <div className="auth-field">
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="auth-field">
          <label>Passwort</label>
          <input
            type="password"
            value={password}
            required
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        {error && <p style={{ color: "red", marginBottom: "12px" }}>{error}</p>}

        <button type="submit" className="btn">
          Einloggen
        </button>
      </form>

      <div className="auth-link">
        Kein Konto? <a href="/signup">Registrieren</a>
      </div>
    </div>
  );
}
