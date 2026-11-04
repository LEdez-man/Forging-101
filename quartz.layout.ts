import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

/**
 * Seitenlayout des Schmiede-Wikis.
 * Gestaltung (Farben/Schriften/CSS) liegt in /design – hier nur die Anordnung.
 */

// Explorer: zeigt nur den Baum der aktuellen Sprache (de/ oder en/),
// Ordner in didaktischer Reihenfolge statt alphabetisch.
const explorer = Component.Explorer({
  title: "Inhalt / Contents",
  folderDefaultState: "collapsed",
  langRoots: ["de", "en"],
  sortFn: (a, b) => {
    const order = [
      // Ordner (DE/EN paarweise) – folders (DE/EN pairs)
      "grundlagen", "basics", "techniken", "techniques", "fortgeschritten", "advanced",
      "projekte", "projects", "kanaele", "channels", "videos", "quellen", "sources",
      "glossar", "glossary", "export",
      // Grundlagen / basics
      "sicherheit", "safety", "werkstatt", "workshop", "gluehfarben", "heat-colours",
      "werkstoffe", "materials", "hammerfuehrung", "hammer-control", "volumenkonstanz", "volume-constancy",
      // Techniken / techniques
      "strecken", "drawing-out", "breiten", "spreading", "stauchen", "upsetting", "spitzen", "tapering",
      "absetzen", "shouldering", "kehlen", "fullering", "spalten", "splitting", "lochen", "punching",
      "abschroten", "cutting", "biegen", "bending", "tordieren", "twisting",
    ]
    const ia = order.indexOf(a.slugSegment)
    const ib = order.indexOf(b.slugSegment)
    if (a.isFolder !== b.isFolder) return a.isFolder ? -1 : 1
    if (ia !== -1 || ib !== -1) {
      if (ia === -1) return 1
      if (ib === -1) return -1
      return ia - ib
    }
    return a.displayName.localeCompare(b.displayName, undefined, { numeric: true, sensitivity: "base" })
  },
})

export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      "GitHub-Repo": "https://github.com/LEdez-man/Forging-101",
      "Quartz": "https://quartz.jzhao.xyz",
    },
  }),
}

export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.LanguageSwitch(),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        { Component: Component.Search(), grow: true },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
      ],
    }),
    explorer,
  ],
  right: [
    Component.Graph(),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks(),
  ],
}

export const defaultListPageLayout: PageLayout = {
  beforeBody: [
    Component.Breadcrumbs(),
    Component.LanguageSwitch(),
    Component.ArticleTitle(),
    Component.ContentMeta(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [{ Component: Component.Search(), grow: true }, { Component: Component.Darkmode() }],
    }),
    explorer,
  ],
  right: [],
}
