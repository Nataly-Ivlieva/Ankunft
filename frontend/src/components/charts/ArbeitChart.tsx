import { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface Props {
  data: any[];
}

export default function ArbeitChart({ data }: Props) {
  const [countryFilter, setCountryFilter] = useState<string>("");

  const filteredData = countryFilter
    ? data.filter((d) => d.country === countryFilter)
    : data;

  const countries = Array.from(
    new Set(data.map((d) => d.country))
  );

  return (
    <>
      <div style={{ marginBottom: 16 }}>
        <select
          value={countryFilter}
          onChange={(e) => setCountryFilter(e.target.value)}
          style={{
            padding: "10px 12px",
            minHeight: 44,
            fontSize: 14,
            borderRadius: 6,
          }}
        >
          <option value="">Alle Länder</option>
          {countries.map((country) => (
            <option key={country} value={country}>
              {country}
            </option>
          ))}
        </select>
      </div>

      <ResponsiveContainer width="100%" height={420}>
        <BarChart
          data={filteredData}
          margin={{ top: 20, right: 40, left: 40, bottom: 80 }}
        >
          <Tooltip cursor={false} />
          <Legend />

          <XAxis
            dataKey="country"
            textAnchor="middle"
            interval={0}
          />

          <YAxis width={90} />

          <Bar
            dataKey="beschäftigte"
            name="Beschäftigte"
            fill="#16a34a"
          />
          <Bar
            dataKey="teilzeit"
            name="Teilzeit"
            fill="#2563eb"
          />
          <Bar
            dataKey="unterbeschäftigte"
            name="Unterbeschäftigte"
            fill="#dc2626"
          />
        </BarChart>
      </ResponsiveContainer>
    </>
  );
}
