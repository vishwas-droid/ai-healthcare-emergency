import { useEffect, useState } from "react";

import { DoctorCard } from "../components/DoctorCard";
import { TrackingPanel } from "../components/TrackingPanel";
import { apiClient } from "../lib/apiClient";
import type { Doctor } from "../types/doctor";
import type { TrackingStartResponse, TrackingStatusResponse } from "../types/recommendation";

export function DoctorsPage() {
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [city, setCity] = useState("Mumbai");
  const [category, setCategory] = useState("Cardiologist");
  const [maxFee, setMaxFee] = useState("1500");
  const [tracking, setTracking] = useState<TrackingStatusResponse | null>(null);

  const pollTracking = (trackingId: number) => {
    const timer = setInterval(async () => {
      const { data } = await apiClient.get<TrackingStatusResponse>(`/tracking/${trackingId}`);
      setTracking(data);
      if (data.status === "ARRIVED") clearInterval(timer);
    }, 2000);
  };

  const startDoctorTracking = async (doctor: Doctor) => {
    const { data } = await apiClient.post<TrackingStartResponse>("/tracking/start", {
      provider_type: "doctor",
      provider_id: doctor.id,
      city: doctor.city,
    });
    pollTracking(data.tracking_id);
  };

  const load = async () => {
    const { data } = await apiClient.get<Doctor[]>("/doctors", {
      params: {
        city: city || undefined,
        category: category || undefined,
        max_fee: maxFee || undefined,
      },
    });
    setDoctors(data);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <section>
      <h2 className="text-3xl font-extrabold">AI Ranked Doctors</h2>
      <div className="mt-4 grid gap-3 rounded-2xl bg-white p-4 shadow-premium sm:grid-cols-4">
        <input placeholder="City" value={city} onChange={(e) => setCity(e.target.value)} className="rounded-lg border px-3 py-2" />
        <input placeholder="Specialization" value={category} onChange={(e) => setCategory(e.target.value)} className="rounded-lg border px-3 py-2" />
        <input placeholder="Max Fee" value={maxFee} onChange={(e) => setMaxFee(e.target.value)} className="rounded-lg border px-3 py-2" />
        <button onClick={load} className="rounded-lg bg-primary px-4 py-2 font-semibold text-white">
          Apply Filters
        </button>
      </div>
      <div className="mt-4">
        <TrackingPanel status={tracking} />
      </div>
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        {doctors.map((doctor) => (
          <DoctorCard key={doctor.id} doctor={doctor} onTrack={startDoctorTracking} />
        ))}
      </div>
    </section>
  );
}
