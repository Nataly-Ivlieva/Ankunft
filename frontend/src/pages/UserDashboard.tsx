import { useEffect, useState } from "react";
import MigrantenRegionChart from "../components/charts/MigrantenRegionChart";
import ArbeitChart from "../components/charts/ArbeitChart";
import StateStatLineChart from "../components/charts/StateStatLineChart";
import KursChart from "../components/charts/KursChart";
import JobRegionChart from "../components/charts/JobRegionChart";
import SalaryRegionChart from "../components/charts/SalaryRegionChart";
import "../styles/dashboard.css";
import { apiFetch } from "../api/api";

export default function UserDashboard() {
  const [migrantenData, setMigrantenData] = useState<any[]>([]);
  const [arbeitData, setArbeitData] = useState<any[]>([]);
  const [stateData, setStateData] = useState<any[]>([]);
  const [kursData, setKursData] = useState<any[]>([]);
  const [jobRegionData, setJobRegionData] = useState<any[]>([]);
  const [salaryData, setSalaryData] = useState<any[]>([]);

  useEffect(() => {
    apiFetch("/statistics/state/by-age")
      .then(setStateData)
      .catch(console.error);

    apiFetch("/statistics/migrants/by-region")
      .then(setMigrantenData)
      .catch(console.error);

    apiFetch("/statistics/arbeit/by-country")
      .then(setArbeitData)
      .catch(console.error);

    apiFetch("/statistics/kurs/by-protection")
      .then(setKursData)
      .catch(console.error);

    apiFetch<any[]>("/statistics/jobs/by-region")
     .then(setJobRegionData)
     .catch(console.error);

     apiFetch("/statistics/salary")
         .then(setSalaryData)
         .catch(console.error);
}, []);

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Willkommen!</h1>

      <div className="dashboard-card">
        <h2 className="dashboard-subtitle">Migranten nach Regionen</h2>
        <MigrantenRegionChart data={migrantenData} />
      </div>

      <div className="dashboard-card">
        <h2 className="dashboard-subtitle">Arbeitsmarkt</h2>
        <ArbeitChart data={arbeitData} />
      </div>

      <div className="dashboard-card">
        <h2 className="dashboard-subtitle">
          Migranten & Arbeitslose nach Alter
        </h2>
        <StateStatLineChart data={stateData} />
      </div>

      <div className="dashboard-card">
        <h2 className="dashboard-subtitle">Kurse nach Schutzstatus</h2>
        <KursChart data={kursData} />
      </div>

      <div className="dashboard-card">
        <h2 className="dashboard-subtitle">Vacancies nach Regionen</h2>
        <JobRegionChart data={jobRegionData} />
      </div>

      <div className="dashboard-card">
        <h2 className="dashboard-subtitle">Salary nach Regionen</h2>
        <SalaryRegionChart data={salaryData} />
      </div>

    </div>
  );
}



