/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#E11D48",
      },
      boxShadow: {
        premium: "0 8px 30px rgba(0,0,0,0.08)",
      },
    },
  },
  plugins: [],
};
