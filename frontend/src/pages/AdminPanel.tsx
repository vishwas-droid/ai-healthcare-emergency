import { useState } from "react";

import { apiClient } from "../lib/apiClient";
import type { AuthResponse } from "../types/auth";

type Overview = {
  doctors: number;
  ambulances: number;
  hospitals: number;
  emergencies: number;
};

export function AdminPanel() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [overview, setOverview] = useState<Overview | null>(null);

  const login = async () => {
    const { data } = await apiClient.post<AuthResponse>("/auth/login", { email, password });
    window.localStorage.setItem("auth_token", data.access_token);
    await loadOverview();
  };

  const loadOverview = async () => {
    const { data } = await apiClient.get<Overview>("/admin/overview");
    setOverview(data);
  };

  return (
    <section className="space-y-6">
      <div className="rounded-3xl bg-surface p-6 shadow-premium">
        <h2 className="text-3xl font-extrabold">Admin Control Room</h2>
        <p className="text-sm text-muted">Role-based access required.</p>
        <div className="mt-4 grid gap-3 md:grid-cols-3">
          <input value={email} onChange={(e) => setEmail(e.target.value)} className="rounded-lg border px-3 py-2" placeholder="Admin Email" />
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="rounded-lg border px-3 py-2" placeholder="Password" />
          <button onClick={login} className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white">
            Login
          </button>
        </div>
        <button onClick={loadOverview} className="mt-3 rounded-lg border px-4 py-2 text-sm">
          Refresh Overview
        </button>
      </div>

      {overview && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            { label: "Doctors", value: overview.doctors },
            { label: "Ambulances", value: overview.ambulances },
            { label: "Hospitals", value: overview.hospitals },
            { label: "Emergencies", value: overview.emergencies },
          ].map((item) => (
            <div key={item.label} className="rounded-2xl bg-surface p-5 shadow-premium">
              <p className="text-xs text-muted">{item.label}</p>
              <p className="text-3xl font-bold">{item.value}</p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
