import type { BookingTrackingResponse } from "../types/booking";

type Props = {
  data: BookingTrackingResponse | null;
};

function fmt(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}m ${s}s`;
}

export function BookingTracker({ data }: Props) {
  if (!data) return null;

  return (
    <div className="rounded-2xl border bg-surface p-4 shadow-premium">
      <p className="text-lg font-bold">Live Booking Tracker #{data.booking_id}</p>
      <p className="text-sm text-slate-600">Status: {data.booking_status} | ETA: {fmt(data.eta_seconds)}</p>
      <div className="mt-3 h-2 rounded-full bg-slate-200">
        <div className="h-2 rounded-full bg-primary" style={{ width: `${data.progress_percent}%` }} />
      </div>
      <div className="mt-3 grid gap-2 sm:grid-cols-3">
        {data.timeline.map((step) => (
          <div key={step.step} className={`rounded-lg border px-3 py-2 text-xs ${step.done ? "border-emerald-300 bg-emerald-50" : "border-slate-200"}`}>
            {step.step}
          </div>
        ))}
      </div>
      <p className="mt-2 text-xs text-slate-500">Simulated location: {data.simulated_location.lat}, {data.simulated_location.lng}</p>
    </div>
  );
}
