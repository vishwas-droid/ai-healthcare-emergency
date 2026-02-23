import { Link, Outlet } from "react-router-dom";

import { StickyEmergencyBanner } from "./StickyEmergencyBanner";

export function Layout() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="sticky top-0 z-40 border-b bg-white/95 backdrop-blur">
        <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <h1 className="text-lg font-extrabold text-primary">MedAI Emergency</h1>
          <div className="flex flex-wrap gap-4 text-sm font-semibold">
            <Link to="/">Home</Link>
            <Link to="/doctors">Doctors</Link>
            <Link to="/ambulances">Ambulances</Link>
            <Link to="/compare">Compare</Link>
            <Link to="/analytics">Analytics</Link>
          </div>
          <a href="tel:+919800088108" className="rounded-full bg-primary px-4 py-2 text-sm font-bold text-white">
            24x7 Call Us
          </a>
        </nav>
      </header>
      <StickyEmergencyBanner />
      <main className="mx-auto max-w-7xl px-6 py-8">
        <Outlet />
      </main>
      <footer className="mt-8 border-t bg-white">
        <div className="mx-auto grid max-w-7xl gap-4 px-6 py-6 text-sm sm:grid-cols-5">
          <p>Quick Links</p>
          <p>Privacy Policy</p>
          <p>Terms</p>
          <p>Emergency: +91-9800088108</p>
          <p>Email: support@medaiemergency.com</p>
        </div>
      </footer>
    </div>
  );
}
