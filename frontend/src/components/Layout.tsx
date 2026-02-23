import { Link, Outlet } from "react-router-dom";

import { FloatingAIAssistant } from "./FloatingAIAssistant";
import { StickyEmergencyBanner } from "./StickyEmergencyBanner";
import { useTheme } from "../store/useTheme";

export function Layout() {
  const { theme, toggle } = useTheme();

  return (
    <div className="min-h-screen text-ink">
      <header className="sticky top-0 z-40 border-b border-white/20 bg-surface backdrop-blur">
        <nav className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-6 py-4">
          <h1 className="text-xl font-extrabold text-primary">MedAI Emergency OS</h1>
          <div className="flex flex-wrap gap-4 text-sm font-semibold">
            <Link to="/">Home</Link>
            <Link to="/triage">AI Triage</Link>
            <Link to="/doctors">Doctors</Link>
            <Link to="/ambulances">Ambulances</Link>
            <Link to="/hospitals">Hospitals</Link>
            <Link to="/compare">Compare</Link>
            <Link to="/tracking">Live Tracking</Link>
            <Link to="/analytics">Analytics</Link>
            <Link to="/admin">Admin</Link>
          </div>
          <div className="flex items-center gap-3">
            <button onClick={toggle} className="rounded-full border px-3 py-2 text-xs font-semibold">
              {theme === "dark" ? "Light" : "Dark"}
            </button>
            <a href="tel:+919800088108" className="rounded-full bg-primary px-4 py-2 text-sm font-bold text-white">
              24x7 Call Us
            </a>
          </div>
        </nav>
      </header>
      <StickyEmergencyBanner />
      <main className="mx-auto max-w-7xl px-6 py-8">
        <Outlet />
      </main>
      <footer className="mt-8 border-t border-white/10 bg-surface">
        <div className="mx-auto grid max-w-7xl gap-4 px-6 py-6 text-sm sm:grid-cols-5">
          <p>Quick Links</p>
          <p>Privacy Policy</p>
          <p>Terms</p>
          <p>Emergency: +91-9800088108</p>
          <p>Email: support@medaiemergency.com</p>
        </div>
      </footer>
      <FloatingAIAssistant />
    </div>
  );
}
