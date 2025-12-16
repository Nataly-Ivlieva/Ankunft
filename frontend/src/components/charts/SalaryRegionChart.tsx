import { useMemo, useState } from "react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const REGION_SHORT: Record<string, string> = {
 Bayern: "BY",
  Berlin: "BE",
  Hamburg: "HH",
  Hessen: "HE",
  Sachsen: "SN",
  NordrheinWestfalen: "NRW",
  "Baden-Württemberg": "BW",
  Brandenburg: "BB",
  Bremen: "HB",
  "Mecklenburg-Vorpommern": "MV",
  Niedersachsen: "NI",
  "Rheinland-Pfalz": "RP",
  Saarland: "SL",
  "Sachsen-Anhalt": "ST",
  "Schleswig-Holstein": "SH",
  Thüringen: "TH",
};

interface Props {
  data: {
    region: string;
    region_id: number;
    category: string;
    category_id: number;
    month: string;
    salary: number;
  }[];
}

export default function SalaryRegionChart({ data }: Props) {
  const [category, setCategory] = useState("");
  const [region, setRegion] = useState("");

  const categories = useMemo(
    () => Array.from(new Set(data.map((d) => d.category))),
    [data]
  );

  const regions = useMemo(
    () => Array.from(new Set(data.map((d) => d.region))),
    [data]
  );

  const filtered = useMemo(() => {
    return data.filter(
      (d) =>
        (!category || d.category === category) &&
        (!region || d.region === region)
    );
  }, [data, category, region]);

  const regionBarData = useMemo(() => {
    if (region) return [];

    const lastMonth = filtered
      .map((d) => d.month)
      .sort()
      .at(-1);

    const map = new Map<string, number>();

    filtered
      .filter((d) => d.month === lastMonth)
      .forEach(({ region, salary }) => {
        map.set(region, salary);
      });

    return Array.from(map.entries()).map(([region, salary]) => ({
      region,
      salary,
    }));
  }, [filtered, region]);

  const timeLineData = useMemo(() => {
    if (!region) return [];

    const map = new Map<string, number>();

    filtered.forEach(({ month, salary }) => {
      map.set(month, salary);
    });

    return Array.from(map.entries())
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([month, salary]) => ({
        month,
        salary,
      }));
  }, [filtered, region]);

  return (
    <>
      <div style={{ display: "flex", gap: 16, marginBottom: 16 }}>
        <select value={category} onChange={(e) => setCategory(e.target.value)} style={{ padding: "10px", minHeight: 44 }}>
          <option value="">Alle Berufe</option>
          {categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>

        <select value={region} onChange={(e) => setRegion(e.target.value)} style={{ padding: "10px", minHeight: 44 }}>
          <option value="">Alle Regionen</option>
          {regions.map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>
      </div>

      <ResponsiveContainer width="100%" height={420}>
        {region ? (

          <LineChart data={timeLineData}>
            <Tooltip />
            <Legend />
            <XAxis dataKey="month" />
            <YAxis />
            <Line
              type="monotone"
              dataKey="salary"
              name="Salary"
              stroke="#2563eb"
              strokeWidth={3}
            />
          </LineChart>
        ) : (
          <BarChart data={regionBarData}>
            <Tooltip />
            <Legend />
            <XAxis
              dataKey="region"
              tickFormatter={(v) => REGION_SHORT[v] ?? v}
            />
            <YAxis />
            <Bar dataKey="salary" name="Salary" fill="#16a34a" />
          </BarChart>
        )}
      </ResponsiveContainer>
    </>
  );
}


