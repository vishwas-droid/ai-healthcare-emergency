import { useState } from "react";
import { Link } from "react-router-dom";

export function FloatingAIAssistant() {
  const [open, setOpen] = useState(false);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {open && (
        <div className="mb-3 w-72 rounded-2xl bg-surface p-4 shadow-premium">
          <p className="text-sm font-semibold text-muted">AI Emergency Assistant</p>
          <p className="mt-2 text-sm">Start triage, summon ambulance, or view live tracking instantly.</p>
          <div className="mt-3 grid gap-2">
            <Link to="/triage" className="rounded-lg bg-primary px-3 py-2 text-sm font-semibold text-white">
              Start AI Triage
            </Link>
            <Link to="/tracking" className="rounded-lg border px-3 py-2 text-sm font-semibold">
              Live Tracking
            </Link>
            <a href="tel:+919800088108" className="rounded-lg bg-slate-900 px-3 py-2 text-sm font-semibold text-white">
              Call Emergency
            </a>
          </div>
        </div>
      )}
      <button
        onClick={() => setOpen((prev) => !prev)}
        className="flex h-14 w-14 items-center justify-center rounded-full bg-primary text-white shadow-glow"
        aria-label="Toggle AI Assistant"
      >
        AI
      </button>
    </div>
  );
}
