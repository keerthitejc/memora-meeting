/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          indigo: "#6366F1",
          violet: "#8B5CF6",
          teal: "#14B8A6",
          dark: "#1E293B",
          muted: "#64748B",
          bg: "#FAFAFC",
        },
        status: {
          overdue: "#EF4444",
          progress: "#F59E0B",
          open: "#64748B",
          done: "#10B981",
        }
      },
      boxShadow: {
        soft: "0 4px 20px rgba(15, 23, 42, 0.06)",
        card: "0 10px 30px -5px rgba(99, 102, 241, 0.08)",
        glow: "0 0 25px rgba(139, 92, 246, 0.25)"
      },
      borderRadius: {
        '2xl': '16px',
        '3xl': '24px'
      }
    },
  },
  plugins: [],
}
