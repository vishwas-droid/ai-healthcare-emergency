import { useEffect, useState } from "react";

import { DoctorCard } from "../components/DoctorCard";
import { TrackingPanel } from "../components/TrackingPanel";
import { apiClient } from "../lib/apiClient";
import type { BookingPayload } from "../types/booking";
import type { Doctor } from "../types/doctor";
import type { MetaOptions } from "../types/meta";
import type { TrackingStartResponse, TrackingStatusResponse } from "../types/recommendation";

const defaultMeta: MetaOptions = {
  cities: [],
  countries: [],
  doctor_categories: ["Cardiologist", "Neurologist", "Pediatrician", "General Physician", "Orthopedic", "Dermatologist"],
  ambulance_types: [],
  problem_suggestions: [],
  budget_suggestions: [800, 1200, 2000, 3000, 5000],
};

export function DoctorsPage() {
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [city, setCity] = useState("Mumbai");
  const [category, setCategory] = useState("Cardiologist");
  const [maxFee, setMaxFee] = useState("1500");
  const [tracking, setTracking] = useState<TrackingStatusResponse | null>(null);
  const [meta, setMeta] = useState<MetaOptions>(defaultMeta);

  const createBooking = async (payload: BookingPayload) => {
    const method = (window.prompt("Payment method: COD / UPI / RAZORPAY", "COD") || "COD").toUpperCase();
    const upiId = method === "UPI" ? window.prompt("Enter UPI ID", "name@upi") || "" : "";
    const { data } = await apiClient.post("/bookings", { ...payload, payment_method: method, upi_id: upiId });
    window.alert(`Appointment booked. Booking ID: ${data.booking.id}`);
  };

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
        limit: 80,
      },
    });
    setDoctors(data);
  };

  useEffect(() => {
    load();
    apiClient.get<MetaOptions>("/meta/options").then((res) => setMeta(res.data)).catch(() => setMeta(defaultMeta));
  }, []);

  return (
    <section>
      <h2 className="text-3xl font-extrabold">AI Ranked Doctors</h2>
      <div className="mt-4 grid gap-3 rounded-2xl bg-white p-4 shadow-premium sm:grid-cols-4">
        <input list="doc-city-options" placeholder="City" value={city} onChange={(e) => setCity(e.target.value)} className="rounded-lg border px-3 py-2" />
        <datalist id="doc-city-options">{meta.cities.map((c) => <option key={c} value={c} />)}</datalist>

        <input list="doc-category-options" placeholder="Specialization" value={category} onChange={(e) => setCategory(e.target.value)} className="rounded-lg border px-3 py-2" />
        <datalist id="doc-category-options">{meta.doctor_categories.map((c) => <option key={c} value={c} />)}</datalist>

        <input list="doc-fee-options" placeholder="Max Fee" value={maxFee} onChange={(e) => setMaxFee(e.target.value)} className="rounded-lg border px-3 py-2" />
        <datalist id="doc-fee-options">{meta.budget_suggestions.map((b) => <option key={b} value={String(b)} />)}</datalist>

        <button onClick={load} className="rounded-lg bg-primary px-4 py-2 font-semibold text-white">Apply Filters</button>
      </div>
      <div className="mt-4"><TrackingPanel status={tracking} /></div>
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        {doctors.map((doctor) => (
          <DoctorCard
            key={doctor.id}
            doctor={doctor}
            onTrack={startDoctorTracking}
            onBook={() => createBooking({ provider_type: "doctor", provider_id: doctor.id, city: doctor.city })}
          />
        ))}
      </div>
    </section>
  );
}
