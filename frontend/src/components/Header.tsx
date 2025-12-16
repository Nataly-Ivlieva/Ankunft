import { Link, useNavigate } from "react-router-dom";
import "../styles/global.css";
import Logo from "../assets/Logo.png";

export default function Header() {
  const navigate = useNavigate();

  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/");
  }

  function handleLogoClick(e: React.MouseEvent) {
    if (token) {
      e.preventDefault();
    }
  }

  return (
    <header className="header">
      <a href="/" className="header-logo" onClick={handleLogoClick}>
        <img
          src={Logo}
          alt="Ankunft Logo"
          style={{ height: "44px", verticalAlign: "middle" }}
        />
      </a>

      <nav className="header-nav">
        {!token ? (
          <>
            <Link to="/login" className="header-link">Anmelden</Link>
            <Link to="/signup" className="header-link header-link--strong">
              Registrieren
            </Link>
          </>
        ) : (
          <>
            <span className="header-link">Angemeldet als: {role}</span>
            <button onClick={handleLogout} className="btn">
              Logout
            </button>
          </>
        )}
      </nav>
    </header>
  );
}
