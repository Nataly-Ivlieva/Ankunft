import { useMemo, useState } from "react";
import {
  BarChart,
  Bar,
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
    category: string;
    count: number;
  }[];
}

export default function JobRegionChart({ data }: Props) {
  const [category, setCategory] = useState<string>("");

  const categories = useMemo(
    () => Array.from(new Set(data.map((d) => d.category))),
    [data]
  );
  const chartData = useMemo(() => {
    const source = category
      ? data.filter((d) => d.category === category)
      : data;

    const regionMap = new Map<string, number>();

    source.forEach(({ region, count }) => {
      regionMap.set(region, (regionMap.get(region) ?? 0) + count);
    });

    return Array.from(regionMap.entries()).map(([region, count]) => ({
      region,
      count,
    }));
  }, [data, category]);

  return (
    <>
      <div style={{ marginBottom: 16 }}>
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          style={{ padding: "10px", minHeight: 44 }}
        >
          <option value="">Alle Berufe</option>
          {categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      <ResponsiveContainer width="100%" height={420}>
        <BarChart
          data={chartData}
          margin={{ top: 20, right: 40, left: 40, bottom: 80 }}
        >
          <Tooltip cursor={false} />
          <Legend />

          <XAxis
            dataKey="region"
            angle={-30}
            textAnchor="end"
            interval={0}
            tickFormatter={(value) =>
              REGION_SHORT[value] ?? value.slice(0, 2)
            }
          />

          <YAxis width={90} />

          <Bar
            dataKey="count"
            name="Anzahl"
            fill="#2563eb"
          />
        </BarChart>
      </ResponsiveContainer>
    </>
  );
}
