import { useEffect, useState } from "react";

import { apiClient } from "../lib/apiClient";
import type { MetaOptions } from "../types/meta";

type CompareResponse = {
  winner_id: number;
  winner_name: string;
  score: number;
  reason: string;
};

export function ComparePage() {
  const [entityType, setEntityType] = useState("doctor");
  const [ids, setIds] = useState("1,2");
  const [city, setCity] = useState("Mumbai");
  const [category, setCategory] = useState("Cardiologist");
  const [budget, setBudget] = useState("1500");
  const [result, setResult] = useState<CompareResponse | null>(null);
  const [meta, setMeta] = useState<MetaOptions>({
    cities: [],
    countries: [],
    doctor_categories: [],
    ambulance_types: [],
    problem_suggestions: [],
    budget_suggestions: [800, 1200, 2000, 3000, 5000],
  });

  useEffect(() => {
    apiClient.get<MetaOptions>("/meta/options").then((res) => setMeta(res.data)).catch(() => undefined);
  }, []);

  const runCompare = async () => {
    const { data } = await apiClient.post<CompareResponse>("/compare", {
      entity_type: entityType,
      ids: ids
        .split(",")
        .map((x) => Number(x.trim()))
        .filter((x) => !Number.isNaN(x)),
      city,
      category,
      budget: Number(budget),
    });
    setResult(data);
  };

  return (
    <section>
      <h2 className="text-3xl font-extrabold">Comparison Engine</h2>
      <div className="mt-4 grid gap-3 rounded-2xl bg-surface p-4 shadow-premium sm:grid-cols-5">
        <select value={entityType} onChange={(e) => setEntityType(e.target.value)} className="rounded-lg border px-3 py-2">
          <option value="doctor">Doctors</option>
          <option value="ambulance">Ambulances</option>
        </select>
        <input value={ids} onChange={(e) => setIds(e.target.value)} placeholder="IDs: 1,2,3" className="rounded-lg border px-3 py-2" />
        <input list="compare-city-options" value={city} onChange={(e) => setCity(e.target.value)} placeholder="City" className="rounded-lg border px-3 py-2" />
        <datalist id="compare-city-options">{meta.cities.map((c) => <option key={c} value={c} />)}</datalist>
        <input list="compare-category-options" value={category} onChange={(e) => setCategory(e.target.value)} placeholder="Problem/Category" className="rounded-lg border px-3 py-2" />
        <datalist id="compare-category-options">{meta.doctor_categories.map((c) => <option key={c} value={c} />)}</datalist>
        <input list="compare-budget-options" value={budget} onChange={(e) => setBudget(e.target.value)} placeholder="Budget" className="rounded-lg border px-3 py-2" />
        <datalist id="compare-budget-options">{meta.budget_suggestions.map((b) => <option key={b} value={String(b)} />)}</datalist>
      </div>
      <button onClick={runCompare} className="mt-3 rounded-lg bg-primary px-4 py-2 font-semibold text-white">
        Compare Now
      </button>
      {result && (
        <div className="mt-6 rounded-2xl bg-surface p-5 shadow-premium">
          <p className="text-lg font-bold">Best Choice: {result.winner_name}</p>
          <p className="text-sm">AI Score: {result.score}</p>
          <p className="mt-2 text-slate-700">{result.reason}</p>
        </div>
      )}
    </section>
  );
}
