/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#16232B",        // deep slate navy - primary text
        canvas: "#F7F9FA",     // soft cool background
        panel: "#FFFFFF",
        cardline: "#E3E9EC",   // subtle card borders
        muted: "#5B6B73",      // secondary text
        teal: {
          DEFAULT: "#0E7C7B",
          dark: "#0A5E5D",
          light: "#E3F2F1",
        },
        alert: {
          DEFAULT: "#C1443D",
          light: "#FBEAE9",
        },
        amber: {
          DEFAULT: "#B7791F",
          light: "#FBF3E3",
        },
      },
      fontFamily: {
        display: ["'Fraunces'", "serif"],
        body: ["'Inter'", "sans-serif"],
        mono: ["'IBM Plex Mono'", "monospace"],
      },
      boxShadow: {
        card: "0 1px 2px rgba(22,35,43,0.04), 0 4px 16px rgba(22,35,43,0.06)",
      },
    },
  },
  plugins: [],
}
