import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { AmbulanceCard } from "../components/AmbulanceCard";
import { DoctorCard } from "../components/DoctorCard";
import { TrackingPanel } from "../components/TrackingPanel";
import { apiClient } from "../lib/apiClient";
import type { Ambulance } from "../types/ambulance";
import type { Doctor } from "../types/doctor";
import type {
  RecommendResponse,
  TrackingStartResponse,
  TrackingStatusResponse,
} from "../types/recommendation";

export function HomePage() {
  const [location, setLocation] = useState("Mumbai");
  const [problem, setProblem] = useState("chest pain");
  const [budget, setBudget] = useState("1200");
  const [servicePreference, setServicePreference] = useState("both");
  const [recommendation, setRecommendation] = useState<RecommendResponse | null>(null);
  const [tracking, setTracking] = useState<TrackingStatusResponse | null>(null);
  const [activeTrackingId, setActiveTrackingId] = useState<number | null>(null);

  const runRecommendation = async () => {
    const { data } = await apiClient.post<RecommendResponse>("/recommend", {
      location,
      problem,
      budget: Number(budget),
      service_preference: servicePreference,
      min_rating: 4,
      suggestion_count: 30,
    });
    setRecommendation(data);
  };

  const startTracking = async (providerType: "doctor" | "ambulance", providerId: number) => {
    const { data } = await apiClient.post<TrackingStartResponse>("/tracking/start", {
      provider_type: providerType,
      provider_id: providerId,
      city: location,
    });
    setActiveTrackingId(data.tracking_id);
  };

  useEffect(() => {
    if (!activeTrackingId) return;
    const timer = setInterval(async () => {
      const { data } = await apiClient.get<TrackingStatusResponse>(`/tracking/${activeTrackingId}`);
      setTracking(data);
      if (data.status === "ARRIVED") {
        clearInterval(timer);
      }
    }, 2000);

    return () => clearInterval(timer);
  }, [activeTrackingId]);

  return (
    <div className="space-y-14">
      <section className="grid items-center gap-8 rounded-3xl bg-gradient-to-r from-rose-50 via-white to-red-50 p-8 shadow-premium lg:grid-cols-2">
        <div>
          <h2 className="text-4xl font-extrabold leading-tight">AI Powered Emergency Healthcare at Your Fingertips</h2>
          <p className="mt-4 text-lg text-slate-700">Find top doctors and fastest ambulances ranked by AI intelligence.</p>
          <div className="mt-6 flex gap-3">
            <Link to="/doctors" className="rounded-xl border px-4 py-3 font-semibold">
              Find Doctors
            </Link>
            <Link to="/ambulances" className="rounded-xl bg-primary px-4 py-3 font-semibold text-white">
              Book Ambulance Now
            </Link>
          </div>
        </div>
        <img
          src="https://images.unsplash.com/photo-1516549655169-df83a0774514?w=1200"
          alt="Emergency medical"
          className="h-80 w-full rounded-2xl object-cover"
        />
      </section>

      <section className="rounded-3xl bg-white p-6 shadow-premium">
        <h3 className="text-2xl font-bold">Emergency AI Assistant</h3>
        <p className="mt-1 text-sm text-slate-600">Step 1: Location | Step 2: Problem | Step 3: Budget | Step 4: AI Ranking</p>
        <div className="mt-4 grid gap-3 md:grid-cols-4">
          <input value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Enter location" className="rounded-lg border px-3 py-2" />
          <input value={problem} onChange={(e) => setProblem(e.target.value)} placeholder="Enter medical problem" className="rounded-lg border px-3 py-2" />
          <input value={budget} onChange={(e) => setBudget(e.target.value)} placeholder="Enter budget" className="rounded-lg border px-3 py-2" />
          <select value={servicePreference} onChange={(e) => setServicePreference(e.target.value)} className="rounded-lg border px-3 py-2">
            <option value="both">Doctor + Ambulance</option>
            <option value="doctor">Doctor Only</option>
            <option value="ambulance">Ambulance Only</option>
          </select>
        </div>
        <button onClick={runRecommendation} className="mt-4 rounded-lg bg-primary px-5 py-2 font-semibold text-white">
          Get AI Recommendation
        </button>

        {recommendation && (
          <div className="mt-6 space-y-5">
            <div className="rounded-2xl bg-rose-50 p-4">
              <p className="font-semibold text-primary">Top Doctor Insight</p>
              <p className="text-sm text-slate-700">{recommendation.top_doctor_summary}</p>
            </div>
            <div className="rounded-2xl bg-blue-50 p-4">
              <p className="font-semibold text-blue-700">Top Ambulance Insight</p>
              <p className="text-sm text-slate-700">{recommendation.top_ambulance_summary}</p>
            </div>
            <div className="rounded-2xl bg-emerald-50 p-4">
              <p className="font-semibold text-emerald-700">Final AI Recommendation</p>
              <p className="text-sm text-slate-700">{recommendation.final_recommendation}</p>
              <p className="mt-2 text-xs text-slate-600">
                Compared {recommendation.compared_doctors ?? 0} doctors and {recommendation.compared_ambulances ?? 0} ambulances
              </p>
            </div>

            <TrackingPanel status={tracking} />

            {recommendation.doctors.length > 0 && (
              <div>
                <h4 className="mb-3 text-xl font-bold">AI Ranked Doctors</h4>
                <div className="grid gap-4 lg:grid-cols-2">
                  {recommendation.doctors.map((doctor: Doctor) => (
                    <DoctorCard key={doctor.id} doctor={doctor} onTrack={() => startTracking("doctor", doctor.id)} />
                  ))}
                </div>
              </div>
            )}

            {recommendation.ambulances.length > 0 && (
              <div>
                <h4 className="mb-3 text-xl font-bold">AI Ranked Ambulances</h4>
                <div className="grid gap-4 lg:grid-cols-2">
                  {recommendation.ambulances.map((ambulance: Ambulance) => (
                    <AmbulanceCard key={ambulance.id} ambulance={ambulance} onTrack={() => startTracking("ambulance", ambulance.id)} />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </section>

      <section>
        <h3 className="text-2xl font-bold">How It Works</h3>
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {["Select Service", "Enter Location", "AI Ranks Best Option", "Get Immediate Assistance"].map((s, i) => (
            <div key={s} className="rounded-2xl bg-white p-5 shadow-premium">
              <p className="text-xs font-bold text-primary">Step {i + 1}</p>
              <p className="mt-2 text-lg font-semibold">{s}</p>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h3 className="text-2xl font-bold">Why Our AI Is Better</h3>
        <p className="mt-3 text-slate-700">
          Multi-factor ranking, response-time optimization, cost optimization, experience weighting, location priority, and verified bonus.
        </p>
      </section>

      <section>
        <h3 className="text-2xl font-bold">Testimonials</h3>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          {["Saved critical time.", "Best ranked doctor instantly.", "Ambulance arrived in 9 minutes."].map((t) => (
            <div key={t} className="rounded-2xl bg-white p-5 shadow-premium">
              {t}
            </div>
          ))}
        </div>
      </section>

      <section>
        <h3 className="text-2xl font-bold">Blogs & Insights</h3>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          {["Emergency Awareness", "CPR Guides", "Medical Tips"].map((b) => (
            <article key={b} className="rounded-2xl bg-white p-5 shadow-premium">
              <p className="text-lg font-semibold">{b}</p>
              <p className="mt-1 text-sm text-slate-600">Actionable emergency guidance for families and caregivers.</p>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
