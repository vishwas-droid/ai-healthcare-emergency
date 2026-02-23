import { useEffect, useState } from "react";

import { apiClient } from "../lib/apiClient";
import type { Analytics } from "../types/analytics";

export function AnalyticsPage() {
  const [data, setData] = useState<Analytics | null>(null);

  useEffect(() => {
    apiClient.get<Analytics>("/analytics").then((res) => setData(res.data));
  }, []);

  return (
    <section>
      <h2 className="text-3xl font-extrabold">Analytics Dashboard</h2>
      {!data && <p className="mt-4">Loading analytics...</p>}
      {data && (
        <div className="mt-6 grid gap-4 lg:grid-cols-2">
          <div className="rounded-2xl bg-white p-5 shadow-premium">
            <h3 className="font-bold">Average Fee Per City</h3>
            {data.average_fee_per_city.map((row) => (
              <p key={row.city}>
                {row.city}: INR {row.average_fee}
              </p>
            ))}
          </div>
          <div className="rounded-2xl bg-white p-5 shadow-premium">
            <h3 className="font-bold">Fastest Ambulance Per City</h3>
            {data.fastest_ambulance_per_city.map((row, i) => (
              <p key={`${row.city}-${i}`}>
                {row.city}: {row.provider_name} ({row.response_time_minutes} min)
              </p>
            ))}
          </div>
          <div className="rounded-2xl bg-white p-5 shadow-premium">
            <h3 className="font-bold">Most Experienced Doctor Per City</h3>
            {data.most_experienced_doctor_per_city.map((row, i) => (
              <p key={`${row.city}-${i}`}>
                {row.city}: {row.doctor_name} ({row.experience_years} yrs)
              </p>
            ))}
          </div>
          <div className="rounded-2xl bg-white p-5 shadow-premium">
            <h3 className="font-bold">Demand by Problem</h3>
            {data.demand_category_analysis.map((row) => (
              <p key={row.category}>
                {row.category}: {row.demand_count}
              </p>
            ))}
          </div>
          <div className="rounded-2xl bg-white p-5 shadow-premium lg:col-span-2">
            <h3 className="font-bold">Demand by City</h3>
            <div className="mt-2 grid gap-2 md:grid-cols-4">
              {data.demand_by_city.map((row) => (
                <div key={row.city} className="rounded-xl bg-rose-50 p-3">
                  <p className="font-semibold">{row.city}</p>
                  <p className="text-sm">Searches: {row.demand_count}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
