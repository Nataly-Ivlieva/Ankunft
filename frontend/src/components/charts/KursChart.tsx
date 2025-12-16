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

const COLORS = ["#2563eb", "#16a34a", "#dc2626", "#9333ea"];

export default function KursChart({ data }: Props) {
  const [protection, setProtection] = useState<string>("");

  const allProtections = useMemo(() => {
    const keys = new Set<string>();
    data.forEach((row) => {
      Object.keys(row).forEach((k) => {
        if (k !== "kurs") keys.add(k);
      });
    });
    return Array.from(keys);
  }, [data]);

  if (!data.length || !allProtections.length) {
    return null;
  }

  const lineKeys = protection ? [protection] : allProtections;


  return (
    <>
      <div style={{ marginBottom: 16 }}>
        <select
          value={protection}
          onChange={(e) => setProtection(e.target.value)}
          style={{ padding: "10px", minHeight: 44 }}
        >
          <option value="">Alle Schutzarten</option>
          {allProtections.map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>
      </div>

      <ResponsiveContainer width="100%" height={420}>
        <LineChart
          data={data}
          margin={{ top: 20, right: 40, left: 40, bottom: 20 }}
        >
          <Tooltip />
          <Legend />

          <XAxis
            dataKey="kurs"
            angle={-10}
            textAnchor="end"
            interval={0}
            height={100}
            tickMargin={20}
          />

          <YAxis width={90} />

          {lineKeys.map((key, i) => (
            <Line
              key={key}
              type="monotone"
              dataKey={key}
              name={key}
              stroke={COLORS[i % COLORS.length]}
              strokeWidth={3}
              dot={{ r: 4 }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </>
  );
}
