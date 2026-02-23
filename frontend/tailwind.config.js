/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "var(--primary)",
        accent: "var(--accent)",
        surface: "var(--surface)",
        ink: "var(--text)",
        muted: "var(--muted)",
      },
      boxShadow: {
        premium: "0 18px 50px rgba(15, 23, 42, 0.12)",
        glow: "0 0 40px rgba(225, 29, 72, 0.25)",
      },
    },
  },
  plugins: [],
};
