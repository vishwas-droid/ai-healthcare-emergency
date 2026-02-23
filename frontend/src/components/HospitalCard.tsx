import type { Hospital } from "../types/hospital";

type Props = {
  hospital: Hospital;
  onWhy?: (hospital: Hospital) => void;
};

export function HospitalCard({ hospital, onWhy }: Props) {
  return (
    <article className="rounded-2xl bg-surface p-5 shadow-premium">
      <h3 className="text-xl font-bold">{hospital.name}</h3>
      <p className="text-sm text-muted">
        {hospital.city} | ICU Beds {hospital.icu_beds_available}
      </p>
      <div className="mt-2 flex flex-wrap gap-2 text-xs">
        <span className="rounded-full bg-rose-100 px-2 py-1 font-semibold text-primary">AI Score {hospital.ai_score}</span>
        <span className={`rounded-full px-2 py-1 ${hospital.is_available ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-muted"}`}>
          {hospital.is_available ? "Available" : "Busy"}
        </span>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-2 text-sm text-muted">
        <p>Wait: {hospital.emergency_wait_minutes} min</p>
        <p>Success: {hospital.success_rate}%</p>
        <p>Cost Index: {hospital.avg_cost_index}</p>
        <p>Distance: {hospital.distance_km_estimate} km</p>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        <a href={`tel:${hospital.phone_number}`} className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-white">
          Call Hospital
        </a>
        {onWhy && (
          <button onClick={() => onWhy(hospital)} className="rounded-lg border px-3 py-2 text-sm">
            Why AI Recommended
          </button>
        )}
      </div>
    </article>
  );
}
