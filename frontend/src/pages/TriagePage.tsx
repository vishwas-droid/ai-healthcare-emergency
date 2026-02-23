import { useState } from "react";

import { AmbulanceCard } from "../components/AmbulanceCard";
import { DoctorCard } from "../components/DoctorCard";
import { HospitalCard } from "../components/HospitalCard";
import { SeverityBadge } from "../components/SeverityBadge";
import { WhyRankedModal } from "../components/WhyRankedModal";
import { apiClient } from "../lib/apiClient";
import type { AmbulanceRankingResponse, DoctorRankingResponse, HospitalRankingResponse, RankingExplain } from "../types/ranking";
import type { TriageResponse } from "../types/triage";

export function TriagePage() {
  const [complaint, setComplaint] = useState("Severe chest pain and sweating for 20 minutes");
  const [location, setLocation] = useState("Mumbai");
  const [budget, setBudget] = useState("2000");
  const [triage, setTriage] = useState<TriageResponse | null>(null);
  const [doctorRanking, setDoctorRanking] = useState<DoctorRankingResponse | null>(null);
  const [ambulanceRanking, setAmbulanceRanking] = useState<AmbulanceRankingResponse | null>(null);
  const [hospitalRanking, setHospitalRanking] = useState<HospitalRankingResponse | null>(null);
  const [activeExplain, setActiveExplain] = useState<RankingExplain | null>(null);
  const [modalTitle, setModalTitle] = useState("Why AI Recommended");

  const runTriage = async () => {
    const { data } = await apiClient.post<TriageResponse>("/triage", {
      complaint_text: complaint,
      location_city: location,
    });
    setTriage(data);
    setDoctorRanking(null);
    setAmbulanceRanking(null);
    setHospitalRanking(null);
  };

  const runRankDoctors = async () => {
    if (!triage) return;
    const { data } = await apiClient.post<DoctorRankingResponse>("/rank/doctors", {
      emergency_id: triage.emergency_id,
      budget: Number(budget),
      severity: triage.severity,
      location_city: location,
      max_results: 6,
    });
    setDoctorRanking(data);
  };

  const runRankAmbulances = async () => {
    if (!triage) return;
    const { data } = await apiClient.post<AmbulanceRankingResponse>("/rank/ambulances", {
      emergency_id: triage.emergency_id,
      budget: Number(budget),
      severity: triage.severity,
      location_city: location,
      max_results: 6,
    });
    setAmbulanceRanking(data);
  };

  const runRankHospitals = async () => {
    if (!triage) return;
    const { data } = await apiClient.post<HospitalRankingResponse>("/rank/hospitals", {
      emergency_id: triage.emergency_id,
      budget: Number(budget),
      severity: triage.severity,
      location_city: location,
      max_results: 6,
    });
    setHospitalRanking(data);
  };

  const openWhy = (explain: RankingExplain, title: string) => {
    setActiveExplain(explain);
    setModalTitle(title);
  };

  return (
    <section className="space-y-8">
      <div className="rounded-3xl bg-surface p-6 shadow-premium">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 className="text-3xl font-extrabold">AI Emergency Triage</h2>
            <p className="text-sm text-muted">Describe symptoms and get instant severity + recommendations.</p>
          </div>
          {triage && (
            <div className="flex items-center gap-3">
              <SeverityBadge severity={triage.severity} score={triage.severity_score} />
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs">Confidence {Math.round(triage.confidence * 100)}%</span>
            </div>
          )}
        </div>
        {triage && <p className="mt-2 text-xs text-muted">Emergency ID: {triage.emergency_id}</p>}
        <div className="mt-4 grid gap-3 lg:grid-cols-4">
          <textarea
            value={complaint}
            onChange={(e) => setComplaint(e.target.value)}
            className="h-24 rounded-2xl border px-3 py-2 lg:col-span-2"
          />
          <input value={location} onChange={(e) => setLocation(e.target.value)} className="rounded-2xl border px-3 py-2" />
          <input value={budget} onChange={(e) => setBudget(e.target.value)} className="rounded-2xl border px-3 py-2" />
        </div>
        <div className="mt-4 flex flex-wrap gap-3">
          <button onClick={runTriage} className="rounded-xl bg-primary px-5 py-2 text-sm font-semibold text-white">
            Run AI Triage
          </button>
          <button onClick={runRankDoctors} className="rounded-xl border px-5 py-2 text-sm font-semibold">
            Rank Doctors
          </button>
          <button onClick={runRankAmbulances} className="rounded-xl border px-5 py-2 text-sm font-semibold">
            Rank Ambulances
          </button>
          <button onClick={runRankHospitals} className="rounded-xl border px-5 py-2 text-sm font-semibold">
            Rank Hospitals
          </button>
        </div>
      </div>

      {triage && (
        <div className="grid gap-4 lg:grid-cols-3">
          <div className="rounded-2xl bg-rose-50 p-5">
            <p className="text-sm font-semibold text-primary">Emergency Type</p>
            <p className="text-2xl font-bold">{triage.emergency_type}</p>
            <p className="mt-2 text-sm text-muted">Recommended Specialty: {triage.recommended.doctor_specialty}</p>
          </div>
          <div className="rounded-2xl bg-blue-50 p-5">
            <p className="text-sm font-semibold text-blue-700">Ambulance Priority</p>
            <p className="text-2xl font-bold text-blue-700">{triage.recommended.ambulance_priority}</p>
            <p className="mt-2 text-sm text-muted">Hospital Type: {triage.recommended.hospital_type}</p>
          </div>
          <div className="rounded-2xl bg-emerald-50 p-5">
            <p className="text-sm font-semibold text-emerald-700">Risk Flags</p>
            <p className="mt-2 text-sm text-muted">{triage.risk_flags.length ? triage.risk_flags.join(", ") : "None detected"}</p>
            <p className="mt-2 text-xs text-muted">Escalation: {triage.escalation.reason}</p>
          </div>
        </div>
      )}

      {triage && (
        <div className="rounded-2xl bg-surface p-5 shadow-premium">
          <h4 className="text-lg font-semibold">Extracted Medical Entities</h4>
          <div className="mt-3 grid gap-3 md:grid-cols-3 text-sm text-muted">
            <div>
              <p className="text-xs uppercase text-muted">Symptoms</p>
              <p>{triage.entities.symptoms.join(", ") || "N/A"}</p>
            </div>
            <div>
              <p className="text-xs uppercase text-muted">Vitals</p>
              <p>BP: {triage.entities.vitals.bp || "N/A"}</p>
              <p>HR: {triage.entities.vitals.hr || "N/A"}</p>
              <p>SpO2: {triage.entities.vitals.spo2 || "N/A"}</p>
            </div>
            <div>
              <p className="text-xs uppercase text-muted">Risk Factors</p>
              <p>{triage.entities.risk_factors.join(", ") || "None"}</p>
            </div>
          </div>
        </div>
      )}

      {doctorRanking && (
        <div>
          <h3 className="text-2xl font-bold">AI Ranked Doctors</h3>
          <div className="mt-4 grid gap-4 lg:grid-cols-2">
            {doctorRanking.doctors.map((doctor) => {
              const explanation = doctorRanking.explanations.find((e) => e.target_id === doctor.id) || null;
              return (
                <DoctorCard
                  key={doctor.id}
                  doctor={doctor}
                  onWhy={() => explanation && openWhy(explanation, "Why AI Recommended")}
                />
              );
            })}
          </div>
        </div>
      )}

      {ambulanceRanking && (
        <div>
          <h3 className="text-2xl font-bold">AI Ranked Ambulances</h3>
          <div className="mt-4 grid gap-4 lg:grid-cols-2">
            {ambulanceRanking.ambulances.map((ambulance) => {
              const explanation = ambulanceRanking.explanations.find((e) => e.target_id === ambulance.id) || null;
              return (
                <AmbulanceCard
                  key={ambulance.id}
                  ambulance={ambulance}
                  onWhy={() => explanation && openWhy(explanation, "Why AI Recommended")}
                />
              );
            })}
          </div>
        </div>
      )}

      {hospitalRanking && (
        <div>
          <h3 className="text-2xl font-bold">AI Ranked Hospitals</h3>
          <div className="mt-4 grid gap-4 lg:grid-cols-2">
            {hospitalRanking.hospitals.map((hospital) => {
              const explanation = hospitalRanking.explanations.find((e) => e.target_id === hospital.id) || null;
              return (
                <HospitalCard
                  key={hospital.id}
                  hospital={hospital}
                  onWhy={() => explanation && openWhy(explanation, "Why AI Recommended")}
                />
              );
            })}
          </div>
        </div>
      )}

      <WhyRankedModal open={!!activeExplain} explanation={activeExplain} title={modalTitle} onClose={() => setActiveExplain(null)} />
    </section>
  );
}
