import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0e1a12",
        panel: "#16261a",
        "panel-hover": "#1c3122",
        border: "#24392b",
        text: "#eef1e6",
        muted: "#93a894",
        accent: "#c9a24d",
        "accent-dim": "#8a7638",
        tag: "#1e3324",
        "tag-text": "#c9d9c7",
      },
      fontFamily: {
        display: ["var(--font-fraunces)", "serif"],
        body: ["var(--font-inter)", "sans-serif"],
      },
      borderRadius: {
        card: "12px",
        pill: "9999px",
      },
    },
  },
  plugins: [],
};
export default config;
