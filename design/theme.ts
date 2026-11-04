/**
 * DESIGN-TOKENS – zentrale Stelle für Farben & Schriften des Wikis.
 * Design tokens – single place for colours & typography.
 *
 * Quartz liest diese Werte über quartz.config.ts ein und erzeugt daraus
 * CSS-Variablen (--light, --dark, --secondary …). Weiterführende Gestaltung
 * (Abstände, Komponenten, Druck) liegt in design/custom.scss.
 *
 * Palette "Esse & Zunder": warmes Papier, Kohle-Schwarz, Glutorange als Akzent,
 * Anlassblau als Zweitakzent – angelehnt an Glüh- und Anlassfarben.
 */
import { Theme } from "../quartz/util/theme"

export const theme: Theme = {
  fontOrigin: "googleFonts",
  cdnCaching: true,
  typography: {
    header: "Alegreya Sans",
    body: "Source Serif 4",
    code: "IBM Plex Mono",
  },
  colors: {
    lightMode: {
      light: "#f7f3ec", // Seitenhintergrund (Papier)
      lightgray: "#e3dccf", // Linien, Rahmen
      gray: "#a39a8c", // Meta-Text, Graph-Kanten
      darkgray: "#3b3631", // Fließtext
      dark: "#1f1b17", // Überschriften
      secondary: "#b4471b", // Links, Akzent (Glut)
      tertiary: "#2f5d7c", // Hover, besuchte Knoten (Anlassblau)
      highlight: "rgba(180, 71, 27, 0.10)",
      textHighlight: "#ffcf6e88",
    },
    darkMode: {
      light: "#17140f",
      lightgray: "#36302a",
      gray: "#7d7469",
      darkgray: "#d9d2c6",
      dark: "#f2ece2",
      secondary: "#f08a4b",
      tertiary: "#7fb0d0",
      highlight: "rgba(240, 138, 75, 0.12)",
      textHighlight: "#b37a0088",
    },
  },
}

/** Seitentitel / Site title */
export const site = {
  pageTitle: "Forging 101 · Schmiede-Wiki",
  pageTitleSuffix: " · Forging 101",
  locale: "de-DE" as const,
}
