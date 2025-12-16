type Props = {
  raw: any;
};

export default function StatisticBlock({ raw }: Props) {
  if (!raw) return null;

  return (
    <div className="stat-block">
      {raw.employment_percent !== undefined && (
        <div className="stat-item">
          <strong>{raw.employment_percent}%</strong>
          <span>beruflich aktiv</span>
        </div>
      )}

      {raw.salary !== undefined && (
        <div className="stat-item">
          <strong>{raw.salary} €</strong>
          <span>Ø Bruttogehalt</span>
        </div>
      )}

      {raw.vacancies !== undefined && (
        <div className="stat-item">
          <strong>{raw.vacancies}</strong>
          <span>offene Stellen</span>
        </div>
      )}

      {raw.total_migrants !== undefined && (
        <div className="stat-sub">
          Gesamt: {raw.total_migrants.toLocaleString()} Personen
        </div>
      )}
    </div>
  );
}