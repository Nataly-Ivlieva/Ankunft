import { useMemo, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface Props {
  data: any[];
}

export default function StateStatLineChart({ data }: Props) {
  const [protection, setProtection] = useState<string>("");

  const protections = useMemo(
    () => Array.from(new Set(data.map((d) => d.protection))),
    [data]
  );

  const filteredData = protection
    ? data.filter((d) => d.protection === protection)
    : data;

  return (
    <>
      <div style={{ marginBottom: 16 }}>
        <select
          value={protection}
          onChange={(e) => setProtection(e.target.value)}
          style={{ padding: "10px", minHeight: 44 }}
        >
          <option value="">Alle Schutzarten</option>
          {protections.map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>
      </div>

      <ResponsiveContainer width="100%" height={420}>
        <LineChart
          data={filteredData}
          margin={{ top: 20, right: 40, left: 40, bottom: 40 }}
        >
          <Tooltip />
          <Legend />

          <XAxis dataKey="age" />
          <YAxis width={80} />

          <Line
            type="monotone"
            dataKey="arbeitslose"
            name="Arbeitslose"
            stroke="#dc2626"
            strokeWidth={3}
          />

          <Line
            type="monotone"
            dataKey="migranten"
            name="Migranten"
            stroke="#2563eb"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </>
  );
}
