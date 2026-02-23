import { useEffect, useState } from "react";

import { AmbulanceCard } from "../components/AmbulanceCard";
import { BookingTracker } from "../components/BookingTracker";
import { TrackingPanel } from "../components/TrackingPanel";
import { apiClient } from "../lib/apiClient";
import type { Ambulance } from "../types/ambulance";
import type { BookingCheckoutResponse, BookingPayload, BookingTrackingResponse } from "../types/booking";
import type { MetaOptions } from "../types/meta";
import type { TrackingStartResponse, TrackingStatusResponse } from "../types/recommendation";

const defaultMeta: MetaOptions = {
  cities: [],
  countries: [],
  doctor_categories: [],
  ambulance_types: ["BLS", "ALS", "ICU", "Ventilator", "Neonatal"],
  problem_suggestions: [],
  budget_suggestions: [1000, 2000, 3000, 5000, 8000],
};

export function AmbulancesPage() {
  const [ambulances, setAmbulances] = useState<Ambulance[]>([]);
  const [city, setCity] = useState("Mumbai");
  const [vehicleType, setVehicleType] = useState("ICU");
  const [distanceKm, setDistanceKm] = useState("8");
  const [tracking, setTracking] = useState<TrackingStatusResponse | null>(null);
  const [activeBookingId, setActiveBookingId] = useState<number | null>(null);
  const [bookingTrack, setBookingTrack] = useState<BookingTrackingResponse | null>(null);
  const [meta, setMeta] = useState<MetaOptions>(defaultMeta);

  const createBooking = async (payload: BookingPayload) => {
    const methodInput = (window.prompt("Payment method: COD / UPI / RAZORPAY", "COD") || "COD").toUpperCase();
    const method: "COD" | "UPI" | "RAZORPAY" =
      methodInput === "UPI" || methodInput === "RAZORPAY" ? methodInput : "COD";
    const upiId = method === "UPI" ? window.prompt("Enter UPI ID", "name@upi") || "" : "";
    const { data } = await apiClient.post<BookingCheckoutResponse>("/bookings", { ...payload, payment_method: method, upi_id: upiId, distance_km: Number(distanceKm) || 8 });
    setActiveBookingId(data.booking.id);
    if (data.payment_method === "RAZORPAY" && data.razorpay_checkout_url) {
      window.open(data.razorpay_checkout_url, "_blank", "noopener,noreferrer");
    }
    window.alert(`Ambulance booked. Booking ID: ${data.booking.id}`);
  };

  const pollTracking = (trackingId: number) => {
    const timer = setInterval(async () => {
      const { data } = await apiClient.get<TrackingStatusResponse>(`/tracking/${trackingId}`);
      setTracking(data);
      if (data.status === "ARRIVED") clearInterval(timer);
    }, 2000);
  };

  const startAmbulanceTracking = async (ambulance: Ambulance) => {
    const { data } = await apiClient.post<TrackingStartResponse>("/tracking/start", {
      provider_type: "ambulance",
      provider_id: ambulance.id,
      city: ambulance.city,
    });
    pollTracking(data.tracking_id);
  };

  const load = async () => {
    const { data } = await apiClient.get<Ambulance[]>("/ambulances", {
      params: {
        city: city || undefined,
        vehicle_type: vehicleType || undefined,
        limit: 80,
      },
    });
    setAmbulances(data);
  };

  useEffect(() => {
    load();
    apiClient.get<MetaOptions>("/meta/options").then((res) => setMeta(res.data)).catch(() => setMeta(defaultMeta));
  }, []);

  useEffect(() => {
    if (!activeBookingId) return;
    const timer = setInterval(async () => {
      const { data } = await apiClient.get<BookingTrackingResponse>(`/bookings/${activeBookingId}/track`);
      setBookingTrack(data);
      if (data.booking_status === "COMPLETED") clearInterval(timer);
    }, 2500);
    return () => clearInterval(timer);
  }, [activeBookingId]);

  return (
    <section>
      <h2 className="text-3xl font-extrabold">AI Ranked Ambulances</h2>
      <div className="mt-4 grid gap-3 rounded-2xl bg-white p-4 shadow-premium sm:grid-cols-4">
        <input list="amb-city-options" placeholder="City" value={city} onChange={(e) => setCity(e.target.value)} className="rounded-lg border px-3 py-2" />
        <datalist id="amb-city-options">{meta.cities.map((c) => <option key={c} value={c} />)}</datalist>

        <input list="amb-type-options" placeholder="Vehicle Type" value={vehicleType} onChange={(e) => setVehicleType(e.target.value)} className="rounded-lg border px-3 py-2" />
        <datalist id="amb-type-options">{meta.ambulance_types.map((t) => <option key={t} value={t} />)}</datalist>

        <input placeholder="Distance KM" value={distanceKm} onChange={(e) => setDistanceKm(e.target.value)} className="rounded-lg border px-3 py-2" />
        <button onClick={load} className="rounded-lg bg-primary px-4 py-2 font-semibold text-white">Apply Filters</button>
      </div>
      <div className="mt-4 space-y-3">
        <TrackingPanel status={tracking} />
        <BookingTracker data={bookingTrack} />
      </div>
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        {ambulances.map((ambulance) => (
          <AmbulanceCard
            key={ambulance.id}
            ambulance={ambulance}
            distanceKm={Number(distanceKm) || 8}
            onTrack={startAmbulanceTracking}
            onBook={() => createBooking({ provider_type: "ambulance", provider_id: ambulance.id, city: ambulance.city })}
          />
        ))}
      </div>
    </section>
  );
}
