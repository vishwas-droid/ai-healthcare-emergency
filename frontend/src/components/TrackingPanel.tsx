import type { TrackingStatusResponse } from "../types/recommendation";

type Props = {
  status: TrackingStatusResponse | null;
};

function fmt(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}m ${s}s`;
}

export function TrackingPanel({ status }: Props) {
  if (!status) return null;

  return (
    <div className="rounded-2xl bg-slate-900 p-4 text-white shadow-premium">
      <p className="text-sm font-semibold">Live Tracking</p>
      <p className="mt-1 text-lg font-bold">Status: {status.status}</p>
      <p className="text-sm">ETA: {fmt(status.eta_seconds)}</p>
      <p className="text-sm">Progress: {status.progress_percent}%</p>
      <div className="mt-2 h-2 rounded-full bg-white/20">
        <div className="h-2 rounded-full bg-primary" style={{ width: `${status.progress_percent}%` }} />
      </div>
      <p className="mt-2 text-xs text-slate-300">
        Simulated location: {status.simulated_location.lat}, {status.simulated_location.lng}
      </p>
    </div>
  );
}
