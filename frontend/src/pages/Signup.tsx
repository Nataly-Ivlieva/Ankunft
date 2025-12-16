import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiSignup } from "../api/auth";
import "../styles/auth.css";

export default function Signup() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSignup(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    try {
    const session = await apiSignup(email, password);
    localStorage.setItem("token", session.token);
    localStorage.setItem("role", session.role);

      navigate("/dashboard");
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Registrierung fehlgeschlagen");
    }
  }

  return (
    <div className="auth-wrapper">
      <h2 className="auth-title">Registrierung</h2>

      <form onSubmit={handleSignup}>
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
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {error && <p style={{ color: "red", marginBottom: "12px" }}>{error}</p>}

        <button type="submit" className="btn">
          Konto erstellen
        </button>
      </form>

      <div className="auth-link">
        Bereits ein Konto? <a href="/login">Einloggen</a>
      </div>
    </div>
  );
}

