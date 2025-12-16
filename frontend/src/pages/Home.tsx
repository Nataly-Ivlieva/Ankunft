import { useNavigate } from "react-router-dom";
import Logo from "../assets/Logo.png"; // путь к твоему логотипу

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-wrapper">
      <div className="home-box">

        <h1 className="home-title">Willkommen in Deutschland</h1>

        <p className="home-subtitle">
          Willkommen bei <strong>Ankunft+</strong>! Du hast einen mutigen Schritt gemacht – du bist in Deutschland angekommen
          und beginnst ein neues Kapitel. Wir wissen, dass dies viele Fragen aufwirft und manchmal überwältigend sein kann.
          <strong>Ankunft+</strong> ist hier, um dich zu unterstützen. Beantworte einfache Fragen zu deinem Leben und Wohnort,
          und erhalte am Ende eine <strong>persönliche, auf aktuellen Daten basierende Einschätzung</strong>, wie du deine
          Integration in Deutschland gestalten kannst. <em>Du bist nicht allein – jeder Schritt zählt!</em>
        </p>

        <button className="btn home-btn" onClick={() => navigate("/survey")}>
          Fragebogen starten
        </button>
      </div>
    </div>
  );
}
