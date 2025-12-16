import { useState } from "react";
import "../styles/dashboard.css";
import { apiFetch } from "../api/api";

type ImportStatus = "idle" | "loading" | "success" | "error";

interface ImportButtonProps {
  title: string;
  endpoint: string;
}

export default function AdminDashboard() {
  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Adminbereich</h1>

      <ImportSection />
    </div>
  );
}

function ImportSection() {
  return (
    <div className="dashboard-card">
      <h2 className="dashboard-subtitle">Daten-Import</h2>

      <ImportButton title="Gehalt (Salary)" endpoint="/admin/import/salary" />
      <ImportButton title="Geodaten" endpoint="/admin/import/geodata" />
      <ImportButton title="Migranten" endpoint="/admin/import/migranten" />
      <ImportButton title="Arbeit" endpoint="/admin/import/arbeit" />
      <ImportButton title="Kurse" endpoint="/admin/import/kurse" />
      <ImportButton title="State Statistik" endpoint="/admin/import/state-stat" />
    </div>
  );
}

function ImportButton({ title, endpoint }: ImportButtonProps) {
  const [status, setStatus] = useState<ImportStatus>("idle");
  const [progress, setProgress] = useState(0);

  async function startImport() {
    setStatus("loading");
    setProgress(10);

    try {
      await apiFetch(endpoint, {
        method: "POST",
      });

      for (let i = 20; i <= 100; i += 20) {
        await new Promise((r) => setTimeout(r, 200));
        setProgress(i);
      }

      setStatus("success");
    } catch (e) {
      console.error(e);
      setStatus("error");
    }
  }

  return (
    <div className="import-block">
      <button
        className="import-button"
        onClick={startImport}
        disabled={status === "loading"}
      >
        {status === "loading" ? "Import wird ausgeführt..." : title}
      </button>

      {status !== "idle" && (
        <div className="progress-container">
          <div
            className={`progress-bar ${status}`}
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {status === "success" && (
        <p className="status-success">✔ Erfolgreich importiert</p>
      )}
      {status === "error" && (
        <p className="status-error">❌ Fehler beim Import</p>
      )}
    </div>
  );
}
