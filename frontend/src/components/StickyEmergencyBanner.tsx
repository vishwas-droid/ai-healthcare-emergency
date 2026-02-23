export function StickyEmergencyBanner() {
  return (
    <div className="fixed right-4 top-24 z-50 rounded-2xl bg-primary px-5 py-4 text-white shadow-premium">
      <p className="text-lg font-bold">Available 24/7 - Call Now</p>
      <div className="mt-2 flex gap-2">
        <a href="tel:+919800088108" className="rounded-lg bg-white/20 px-3 py-2 text-sm font-semibold">
          Call
        </a>
        <a
          href="https://wa.me/919800088108"
          target="_blank"
          className="rounded-lg bg-white px-3 py-2 text-sm font-semibold text-primary"
          rel="noreferrer"
        >
          WhatsApp
        </a>
      </div>
    </div>
  );
}
