import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
import { FullSlug, resolveRelative } from "../util/path"

/**
 * Sprachumschalter DE/EN.
 * Jede Seite deklariert im Frontmatter:
 *   lang: de | en
 *   translation: <slug der Gegenseite>   (z. B. en/techniques/drawing-out)
 * Fehlt `translation`, wird die Startseite der anderen Sprache verlinkt.
 */
const LANGS = [
  { code: "de", label: "Deutsch", home: "de/index" },
  { code: "en", label: "English", home: "en/index" },
]

const LanguageSwitch: QuartzComponent = ({ fileData, displayClass }: QuartzComponentProps) => {
  const slug = fileData.slug as FullSlug
  const fm = (fileData.frontmatter ?? {}) as Record<string, unknown>
  const current = (fm.lang as string) ?? slug.split("/")[0]
  const translation = fm.translation as string | undefined

  return (
    <nav class={classNames(displayClass, "language-switch")} aria-label="Language">
      {LANGS.map((l) => {
        if (l.code === current) {
          return <span class="active">{l.label}</span>
        }
        const target = (translation ?? l.home) as FullSlug
        return (
          <a
            href={resolveRelative(slug, target)}
            class={classNames(undefined, "internal", translation ? "" : "missing")}
            hreflang={l.code}
            lang={l.code}
          >
            {l.label}
          </a>
        )
      })}
    </nav>
  )
}

export default (() => LanguageSwitch) satisfies QuartzComponentConstructor
