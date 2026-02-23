import { useEffect, useState } from "react";

import { apiClient } from "../lib/apiClient";
import type { Analytics, AnalyticsForecast } from "../types/analytics";

export function AnalyticsPage() {
  const [data, setData] = useState<Analytics | null>(null);
  const [forecast, setForecast] = useState<AnalyticsForecast | null>(null);

  useEffect(() => {
    apiClient.get<Analytics>("/analytics").then((res) => setData(res.data));
    apiClient.get<AnalyticsForecast>("/analytics/forecast").then((res) => setForecast(res.data));
  }, []);

  return (
    <section>
      <h2 className="text-3xl font-extrabold">Analytics Dashboard</h2>
      {!data && <p className="mt-4">Loading analytics...</p>}
      {data && (
        <div className="mt-6 grid gap-4 lg:grid-cols-2">
          <div className="rounded-2xl bg-surface p-5 shadow-premium">
            <h3 className="font-bold">Average Fee Per City</h3>
            {data.average_fee_per_city.map((row) => (
              <p key={row.city}>
                {row.city}: INR {row.average_fee}
              </p>
            ))}
          </div>
          <div className="rounded-2xl bg-surface p-5 shadow-premium">
            <h3 className="font-bold">Fastest Ambulance Per City</h3>
            {data.fastest_ambulance_per_city.map((row, i) => (
              <p key={`${row.city}-${i}`}>
                {row.city}: {row.provider_name} ({row.response_time_minutes} min)
              </p>
            ))}
          </div>
          <div className="rounded-2xl bg-surface p-5 shadow-premium">
            <h3 className="font-bold">Most Experienced Doctor Per City</h3>
            {data.most_experienced_doctor_per_city.map((row, i) => (
              <p key={`${row.city}-${i}`}>
                {row.city}: {row.doctor_name} ({row.experience_years} yrs)
              </p>
            ))}
          </div>
          <div className="rounded-2xl bg-surface p-5 shadow-premium">
            <h3 className="font-bold">Demand by Problem</h3>
            {data.demand_category_analysis.map((row) => (
              <p key={row.category}>
                {row.category}: {row.demand_count}
              </p>
            ))}
          </div>
          <div className="rounded-2xl bg-surface p-5 shadow-premium lg:col-span-2">
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

      {forecast && (
        <div className="mt-8 grid gap-4 lg:grid-cols-2">
          <div className="rounded-2xl bg-surface p-5 shadow-premium">
            <h3 className="font-bold">Peak Emergency Hours</h3>
            <div className="mt-3 grid gap-2">
              {forecast.peak_hours.map((row) => (
                <div key={row.hour} className="flex items-center justify-between rounded-lg border px-3 py-2 text-sm">
                  <span>{row.hour}:00</span>
                  <span className="font-semibold">{row.score}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="rounded-2xl bg-surface p-5 shadow-premium">
            <h3 className="font-bold">Cardiac Spike Probability</h3>
            <div className="mt-3 grid gap-2">
              {forecast.cardiac_spike_probability.map((row) => (
                <div key={row.hour} className="flex items-center justify-between rounded-lg border px-3 py-2 text-sm">
                  <span>{row.hour}:00</span>
                  <span className="font-semibold">{Math.round(row.probability * 100)}%</span>
                </div>
              ))}
            </div>
          </div>
          <div className="rounded-2xl bg-surface p-5 shadow-premium">
            <h3 className="font-bold">Ambulance Demand Forecast</h3>
            <div className="mt-3 grid gap-2">
              {forecast.demand_forecast.map((row) => (
                <div key={row.hour} className="flex items-center justify-between rounded-lg border px-3 py-2 text-sm">
                  <span>{row.hour}:00</span>
                  <span className="font-semibold">{row.forecast}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="rounded-2xl bg-surface p-5 shadow-premium">
            <h3 className="font-bold">High Risk Zones</h3>
            <div className="mt-3 grid gap-2">
              {forecast.high_risk_zones.map((row) => (
                <div key={row.zone} className="flex items-center justify-between rounded-lg border px-3 py-2 text-sm">
                  <span>{row.zone}</span>
                  <span className="font-semibold">{row.risk}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
