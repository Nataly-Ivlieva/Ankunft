import { useEffect, useState } from "react";
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
  Niedersachsen:	"NI",
  "Rheinland-Pfalz":	"RP",
  Saarland:	"SL",
  "Sachsen-Anhalt":	"ST",
  "Schleswig-Holstein":	"SH",
  Thüringen:	"TH",
};

interface Props {
  data: any[];
}

export default function MigrantenRegionChart({ data }: Props) {
  const [regionFilter, setRegionFilter] = useState<string>("");

  const regions = Array.from(
    new Set(data.map((d) => d.region))
  );

  const filteredData = regionFilter
    ? data.filter((d) => d.region === regionFilter)
    : data;

  return (
    <>
      <div style={{ marginBottom: 12 }}>
        <select
          className="dashboard-filter"
          value={regionFilter}
          onChange={(e) => setRegionFilter(e.target.value)}
        >
          <option value="">Alle Regionen</option>

          {regions.map((region) => (
            <option key={region} value={region}>
              {region} ({REGION_SHORT[region] ?? region.slice(0, 2)})
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
            dataKey="region"
            angle={-30}
            textAnchor="end"
            interval={0}
            tickFormatter={(value) =>
              REGION_SHORT[value] ?? value.slice(0, 2)
            }
          />

          <YAxis width={90} />

          <Bar dataKey="zusammen" name="Migranten gesamt" fill="#4f46e5" />
          <Bar dataKey="arbeitslos" name="Arbeitslos" fill="#dc2626" />
        </BarChart>
      </ResponsiveContainer>
    </>
  );
}
