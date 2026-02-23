import { useEffect, useState } from "react";

import { HospitalCard } from "../components/HospitalCard";
import { WhyRankedModal } from "../components/WhyRankedModal";
import { apiClient } from "../lib/apiClient";
import type { Hospital } from "../types/hospital";
import type { HospitalRankingResponse, RankingExplain } from "../types/ranking";

export function HospitalsPage() {
  const [hospitals, setHospitals] = useState<Hospital[]>([]);
  const [city, setCity] = useState("Mumbai");
  const [minIcu, setMinIcu] = useState("5");
  const [emergencyId, setEmergencyId] = useState("");
  const [budget, setBudget] = useState("2500");
  const [ranking, setRanking] = useState<HospitalRankingResponse | null>(null);
  const [activeExplain, setActiveExplain] = useState<RankingExplain | null>(null);

  const load = async () => {
    const { data } = await apiClient.get<Hospital[]>("/hospitals", {
      params: { city: city || undefined, min_icu: minIcu ? Number(minIcu) : undefined },
    });
    setHospitals(data);
  };

  const runRanking = async () => {
    if (!emergencyId) return;
    const { data } = await apiClient.post<HospitalRankingResponse>("/rank/hospitals", {
      emergency_id: emergencyId,
      budget: Number(budget),
      severity: "HIGH",
      location_city: city,
      max_results: 6,
    });
    setRanking(data);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <section className="space-y-6">
      <div className="rounded-3xl bg-surface p-5 shadow-premium">
        <h2 className="text-3xl font-extrabold">Hospital Intelligence Engine</h2>
        <div className="mt-4 grid gap-3 md:grid-cols-4">
          <input value={city} onChange={(e) => setCity(e.target.value)} className="rounded-lg border px-3 py-2" placeholder="City" />
          <input value={minIcu} onChange={(e) => setMinIcu(e.target.value)} className="rounded-lg border px-3 py-2" placeholder="Min ICU" />
          <input value={emergencyId} onChange={(e) => setEmergencyId(e.target.value)} className="rounded-lg border px-3 py-2" placeholder="Emergency ID" />
          <input value={budget} onChange={(e) => setBudget(e.target.value)} className="rounded-lg border px-3 py-2" placeholder="Budget" />
        </div>
        <p className="mt-2 text-xs text-muted">Use the Emergency ID from the AI Triage page for precision ranking.</p>
        <div className="mt-4 flex gap-3">
          <button onClick={load} className="rounded-lg border px-4 py-2 text-sm font-semibold">
            Refresh Hospitals
          </button>
          <button onClick={runRanking} className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white">
            Rank For Emergency
          </button>
        </div>
      </div>

      {ranking ? (
        <div className="grid gap-4 lg:grid-cols-2">
          {ranking.hospitals.map((hospital) => {
            const explanation = ranking.explanations.find((e) => e.target_id === hospital.id) || null;
            return (
              <HospitalCard
                key={hospital.id}
                hospital={hospital}
                onWhy={() => explanation && setActiveExplain(explanation)}
              />
            );
          })}
        </div>
      ) : (
        <div className="grid gap-4 lg:grid-cols-2">
          {hospitals.map((hospital) => (
            <HospitalCard key={hospital.id} hospital={hospital} />
          ))}
        </div>
      )}

      <WhyRankedModal
        open={!!activeExplain}
        explanation={activeExplain}
        title="Why AI Recommended"
        onClose={() => setActiveExplain(null)}
      />
    </section>
  );
}
