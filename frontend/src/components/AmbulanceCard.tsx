import type { Ambulance } from "../types/ambulance";

type Props = {
  ambulance: Ambulance;
  distanceKm?: number;
  onTrack?: (ambulance: Ambulance) => void;
  onBook?: (ambulance: Ambulance) => void;
  onWhy?: (ambulance: Ambulance) => void;
};

export function AmbulanceCard({ ambulance, distanceKm = 8, onTrack, onBook, onWhy }: Props) {
  const whatsappHref = ambulance.whatsapp_link || "https://wa.me/919800088108";
  const callHref = ambulance.phone_number ? `tel:${ambulance.phone_number}` : "tel:+919800088108";
  const estimatedTotalCost = ambulance.base_price + ambulance.cost_per_km * distanceKm;
  const tags = [
    ambulance.cost_per_km <= 25 ? "Budget Friendly" : "Premium",
    ambulance.response_time_minutes <= 10 ? "Fastest Response" : "Stable Response",
    ambulance.vehicle_type === "ICU" ? "ICU Equipped" : "Critical Ready",
    ambulance.has_ventilator ? "Ventilator" : "Oxygen Ready",
  ];

  return (
    <article className="rounded-2xl bg-surface p-5 shadow-premium">
      <h3 className="text-xl font-bold">{ambulance.provider_name}</h3>
      <p className="text-sm text-muted">
        {ambulance.city} | {ambulance.vehicle_type}
      </p>
      <div className="mt-2 flex flex-wrap gap-2 text-xs">
        <span className="rounded-full bg-rose-100 px-2 py-1 font-semibold text-primary">AI Score {ambulance.ai_score}</span>
        {ambulance.verified_status && (
          <span className="rounded-full bg-emerald-100 px-2 py-1 font-semibold text-emerald-700">Verified</span>
        )}
        <span className={`rounded-full px-2 py-1 ${ambulance.is_available ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-muted"}`}>
          {ambulance.is_available ? "Available" : "Busy"}
        </span>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-2 text-sm text-muted">
        <p>Response: {ambulance.response_time_minutes} min</p>
        <p>Rating: {ambulance.rating}</p>
        <p>Cost/km: INR {ambulance.cost_per_km}</p>
        <p>Base: INR {ambulance.base_price}</p>
        <p>Status: {ambulance.availability_status}</p>
        <p>Driver: {ambulance.driver_score}</p>
        <p className="col-span-2 font-semibold text-primary">Estimated Total: INR {estimatedTotalCost.toFixed(0)}</p>
      </div>
      <p className="mt-3 text-sm text-muted">Equipment: {ambulance.equipment_list}</p>
      <div className="mt-2 flex flex-wrap gap-2">
        {tags.map((tag) => (
          <span key={tag} className="rounded-full bg-slate-100 px-2 py-1 text-xs">
            {tag}
          </span>
        ))}
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {onBook && (
          <button onClick={() => onBook(ambulance)} className="rounded-lg bg-primary px-3 py-2 text-sm text-white">
            Book Now
          </button>
        )}
        {onTrack && (
          <button onClick={() => onTrack(ambulance)} className="rounded-lg border px-3 py-2 text-sm">
            Track Ambulance
          </button>
        )}
        <a href={callHref} className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-white">
          Call Now
        </a>
        <a href={whatsappHref} target="_blank" className="rounded-lg bg-green-600 px-3 py-2 text-sm text-white" rel="noreferrer">
          WhatsApp
        </a>
        {onWhy && (
          <button onClick={() => onWhy(ambulance)} className="rounded-lg border px-3 py-2 text-sm">
            Why AI Recommended
          </button>
        )}
      </div>
    </article>
  );
}
