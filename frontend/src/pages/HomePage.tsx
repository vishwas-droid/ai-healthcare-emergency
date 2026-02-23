import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { AmbulanceCard } from "../components/AmbulanceCard";
import { DoctorCard } from "../components/DoctorCard";
import { SeverityBadge } from "../components/SeverityBadge";
import { apiClient } from "../lib/apiClient";
import type { Ambulance } from "../types/ambulance";
import type { Doctor } from "../types/doctor";
import type { MetaOptions } from "../types/meta";
import type { RecommendResponse } from "../types/recommendation";
import type { TriageResponse } from "../types/triage";

const defaultMeta: MetaOptions = {
  cities: [],
  countries: [],
  doctor_categories: [],
  ambulance_types: [],
  problem_suggestions: ["chest pain", "high fever", "stroke signs", "accident trauma"],
  budget_suggestions: [800, 1200, 2000, 3000, 5000],
};

export function HomePage() {
  const [location, setLocation] = useState("Mumbai");
  const [problem, setProblem] = useState("chest pain");
  const [budget, setBudget] = useState("1200");
  const [servicePreference, setServicePreference] = useState("both");
  const [recommendation, setRecommendation] = useState<RecommendResponse | null>(null);
  const [triage, setTriage] = useState<TriageResponse | null>(null);
  const [meta, setMeta] = useState<MetaOptions>(defaultMeta);

  useEffect(() => {
    apiClient.get<MetaOptions>("/meta/options").then((res) => setMeta(res.data)).catch(() => setMeta(defaultMeta));
  }, []);

  const runRecommendation = async () => {
    const { data } = await apiClient.post<RecommendResponse>("/recommend", {
      location,
      problem,
      budget: Number(budget),
      service_preference: servicePreference,
      min_rating: 3.3,
      suggestion_count: 8,
    });
    setRecommendation(data);
  };

  const runTriagePreview = async () => {
    const { data } = await apiClient.post<TriageResponse>("/triage", {
      complaint_text: problem,
      location_city: location,
    });
    setTriage(data);
  };

  return (
    <div className="space-y-14">
      <section className="grid items-center gap-10 rounded-3xl bg-gradient-to-br from-rose-50 via-white to-blue-50 p-10 shadow-premium lg:grid-cols-2">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-muted">AI Emergency Operating System</p>
          <h2 className="mt-3 text-4xl font-extrabold leading-tight">Real-time triage, dispatch, and AI-ranked care in under 60 seconds.</h2>
          <p className="mt-4 text-lg text-muted">A unified command center for patients, doctors, ambulances, and hospitals. Built for critical response.</p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link to="/triage" className="rounded-xl bg-primary px-4 py-3 font-semibold text-white">
              Start AI Triage
            </Link>
            <Link to="/tracking" className="rounded-xl border px-4 py-3 font-semibold">
              Live Tracking
            </Link>
          </div>
          {triage && (
            <div className="mt-6 rounded-2xl bg-surface p-4">
              <div className="flex items-center gap-3">
                <SeverityBadge severity={triage.severity} score={triage.severity_score} />
                <span className="text-sm text-muted">Emergency: {triage.emergency_type}</span>
              </div>
              <p className="mt-2 text-sm text-muted">Recommended: {triage.recommended.doctor_specialty} | {triage.recommended.hospital_type}</p>
            </div>
          )}
        </div>
        <div className="rounded-3xl bg-surface p-6 shadow-premium">
          <h3 className="text-2xl font-bold">Quick AI Triage Preview</h3>
          <p className="mt-1 text-sm text-muted">Get instant severity scoring and next steps.</p>
          <div className="mt-4 grid gap-3">
            <input list="city-options" value={location} onChange={(e) => setLocation(e.target.value)} className="rounded-lg border px-3 py-2" />
            <datalist id="city-options">{meta.cities.map((city) => <option key={city} value={city} />)}</datalist>
            <input list="problem-options" value={problem} onChange={(e) => setProblem(e.target.value)} className="rounded-lg border px-3 py-2" />
            <datalist id="problem-options">{meta.problem_suggestions.map((p) => <option key={p} value={p} />)}</datalist>
            <button onClick={runTriagePreview} className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white">
              Run Triage
            </button>
          </div>
        </div>
      </section>

      <section className="rounded-3xl bg-surface p-6 shadow-premium">
        <h3 className="text-2xl font-bold">Emergency AI Assistant</h3>
        <p className="mt-1 text-sm text-muted">Fast AI ranking for doctors and ambulances.</p>
        <div className="mt-4 grid gap-3 md:grid-cols-4">
          <input list="city-options" value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Enter location" className="rounded-lg border px-3 py-2" />
          <input list="problem-options" value={problem} onChange={(e) => setProblem(e.target.value)} placeholder="Enter medical problem" className="rounded-lg border px-3 py-2" />
          <input list="budget-options" value={budget} onChange={(e) => setBudget(e.target.value)} placeholder="Enter budget" className="rounded-lg border px-3 py-2" />
          <select value={servicePreference} onChange={(e) => setServicePreference(e.target.value)} className="rounded-lg border px-3 py-2">
            <option value="both">Doctor + Ambulance</option>
            <option value="doctor">Doctor Only</option>
            <option value="ambulance">Ambulance Only</option>
          </select>
        </div>
        <button onClick={runRecommendation} className="mt-4 rounded-lg bg-primary px-5 py-2 font-semibold text-white">Get AI Recommendation</button>

        {recommendation && (
          <div className="mt-6 space-y-5">
            <div className="rounded-2xl bg-rose-50 p-4">
              <p className="font-semibold text-primary">Top Doctor Insight</p>
              <p className="text-sm text-muted">{recommendation.top_doctor_summary}</p>
            </div>
            <div className="rounded-2xl bg-blue-50 p-4">
              <p className="font-semibold text-blue-700">Top Ambulance Insight</p>
              <p className="text-sm text-muted">{recommendation.top_ambulance_summary}</p>
            </div>
            <div className="rounded-2xl bg-emerald-50 p-4">
              <p className="font-semibold text-emerald-700">Final AI Recommendation</p>
              <p className="text-sm text-muted">{recommendation.final_recommendation}</p>
              <p className="mt-2 text-xs text-muted">Compared {recommendation.compared_doctors ?? 0} doctors and {recommendation.compared_ambulances ?? 0} ambulances</p>
            </div>

            {recommendation.doctors.length > 0 && (
              <div>
                <h4 className="mb-3 text-xl font-bold">AI Ranked Doctors</h4>
                <div className="grid gap-4 lg:grid-cols-2">
                  {recommendation.doctors.map((doctor: Doctor) => (
                    <DoctorCard key={doctor.id} doctor={doctor} />
                  ))}
                </div>
              </div>
            )}

            {recommendation.ambulances.length > 0 && (
              <div>
                <h4 className="mb-3 text-xl font-bold">AI Ranked Ambulances</h4>
                <div className="grid gap-4 lg:grid-cols-2">
                  {recommendation.ambulances.map((ambulance: Ambulance) => (
                    <AmbulanceCard key={ambulance.id} ambulance={ambulance} />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </section>

      <section>
        <h3 className="text-2xl font-bold">Core Modules</h3>
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            { title: "AI Triage Engine", desc: "Symptom NLP, severity scoring, auto escalation." },
            { title: "Doctor Ranking", desc: "Bayesian ratings + response + proximity intelligence." },
            { title: "Ambulance Dispatch", desc: "Traffic aware ETA + ICU filtering." },
            { title: "Hospital Intelligence", desc: "ICU beds, wait time, success rate." },
          ].map((card) => (
            <div key={card.title} className="rounded-2xl bg-surface p-5 shadow-premium">
              <p className="text-xs font-bold text-primary">Module</p>
              <p className="mt-2 text-lg font-semibold">{card.title}</p>
              <p className="mt-2 text-sm text-muted">{card.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
