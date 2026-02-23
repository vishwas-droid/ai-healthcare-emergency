import { useEffect, useMemo, useState } from "react";

import { apiClient } from "../lib/apiClient";
import type { TrackingStatusResponse } from "../types/recommendation";

function fmt(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}m ${s}s`;
}

export function LiveTrackingPage() {
  const [trackingId, setTrackingId] = useState("");
  const [status, setStatus] = useState<TrackingStatusResponse | null>(null);
  const [wsConnected, setWsConnected] = useState(false);

  const wsUrl = useMemo(() => {
    if (!trackingId) return null;
    const base = (import.meta.env.VITE_WS_URL || "ws://127.0.0.1:8000").replace(/\/$/, "");
    return `${base}/tracking/ws/${trackingId}`;
  }, [trackingId]);

  const connect = async () => {
    if (!trackingId) return;
    const { data } = await apiClient.get<TrackingStatusResponse>(`/tracking/${trackingId}`);
    setStatus(data);
  };

  useEffect(() => {
    if (!wsUrl) return;
    const socket = new WebSocket(wsUrl);
    socket.onopen = () => setWsConnected(true);
    socket.onclose = () => setWsConnected(false);
    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload.error) return;
        setStatus(payload);
      } catch {
        return;
      }
    };
    return () => socket.close();
  }, [wsUrl]);

  return (
    <section className="space-y-6">
      <div className="rounded-3xl bg-surface p-6 shadow-premium">
        <h2 className="text-3xl font-extrabold">Live Tracking Command Center</h2>
        <p className="text-sm text-muted">Connect to a tracking ID and watch real-time ETA updates.</p>
        <p className="mt-1 text-xs text-muted">Tracking IDs come from booking or dispatch responses.</p>
        <div className="mt-4 flex flex-wrap gap-3">
          <input
            value={trackingId}
            onChange={(e) => setTrackingId(e.target.value)}
            placeholder="Enter Tracking ID"
            className="rounded-lg border px-3 py-2"
          />
          <button onClick={connect} className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white">
            Fetch Status
          </button>
          <span className={`rounded-full px-3 py-1 text-xs ${wsConnected ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-muted"}`}>
            {wsConnected ? "WebSocket Connected" : "Waiting for WebSocket"}
          </span>
        </div>
      </div>

      {status && (
        <div className="rounded-3xl bg-slate-900 p-6 text-white shadow-premium">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-white/70">Tracking #{status.tracking_id}</p>
              <h3 className="text-2xl font-bold">{status.status}</h3>
            </div>
            <div className="text-right">
              <p className="text-sm text-white/70">ETA</p>
              <p className="text-2xl font-bold">{fmt(status.eta_seconds)}</p>
            </div>
          </div>
          <div className="mt-4 h-2 rounded-full bg-white/20">
            <div className="h-2 rounded-full bg-primary" style={{ width: `${status.progress_percent}%` }} />
          </div>
          <p className="mt-3 text-xs text-white/60">
            Simulated Location: {status.simulated_location.lat}, {status.simulated_location.lng}
          </p>
        </div>
      )}
    </section>
  );
}
