import { useEffect, useState } from "react";

import { AmbulanceCard } from "../components/AmbulanceCard";
import { TrackingPanel } from "../components/TrackingPanel";
import { apiClient } from "../lib/apiClient";
import type { Ambulance } from "../types/ambulance";
import type { TrackingStartResponse, TrackingStatusResponse } from "../types/recommendation";

export function AmbulancesPage() {
  const [ambulances, setAmbulances] = useState<Ambulance[]>([]);
  const [city, setCity] = useState("Mumbai");
  const [vehicleType, setVehicleType] = useState("ICU");
  const [distanceKm, setDistanceKm] = useState("8");
  const [tracking, setTracking] = useState<TrackingStatusResponse | null>(null);

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
      },
    });
    setAmbulances(data);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <section>
      <h2 className="text-3xl font-extrabold">AI Ranked Ambulances</h2>
      <div className="mt-4 grid gap-3 rounded-2xl bg-white p-4 shadow-premium sm:grid-cols-4">
        <input placeholder="City" value={city} onChange={(e) => setCity(e.target.value)} className="rounded-lg border px-3 py-2" />
        <input placeholder="Vehicle Type" value={vehicleType} onChange={(e) => setVehicleType(e.target.value)} className="rounded-lg border px-3 py-2" />
        <input placeholder="Distance KM" value={distanceKm} onChange={(e) => setDistanceKm(e.target.value)} className="rounded-lg border px-3 py-2" />
        <button onClick={load} className="rounded-lg bg-primary px-4 py-2 font-semibold text-white">
          Apply Filters
        </button>
      </div>
      <div className="mt-4">
        <TrackingPanel status={tracking} />
      </div>
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        {ambulances.map((ambulance) => (
          <AmbulanceCard
            key={ambulance.id}
            ambulance={ambulance}
            distanceKm={Number(distanceKm) || 8}
            onTrack={startAmbulanceTracking}
          />
        ))}
      </div>
    </section>
  );
}
