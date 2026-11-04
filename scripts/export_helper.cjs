// export_helper.cjs – Chromium-Hilfen für scripts/export.py (benötigt `playwright`)
//   node scripts/export_helper.cjs pdf  <in.html> <out.pdf>
//   node scripts/export_helper.cjs svg2png <in.svg> <out.png> [scale]
const { chromium } = require("playwright")
const fs = require("fs")
const path = require("path")

;(async () => {
  const [cmd, input, output, scale] = process.argv.slice(2)
  const browser = await chromium.launch()
  try {
    if (cmd === "pdf") {
      const page = await browser.newPage()
      await page.goto("file://" + path.resolve(input), { waitUntil: "load" })
      await page.pdf({
        path: output,
        format: "A4",
        printBackground: true,
        margin: { top: "18mm", bottom: "18mm", left: "18mm", right: "18mm" },
        displayHeaderFooter: true,
        headerTemplate: "<span></span>",
        footerTemplate:
          '<div style="font-size:8px;width:100%;text-align:center;color:#777"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
      })
    } else if (cmd === "svg2png") {
      const svg = fs.readFileSync(input, "utf8")
      const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/)
      const w = m ? Math.ceil(+m[1]) : 720
      const h = m ? Math.ceil(+m[2]) : 400
      const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: +(scale || 2) })
      await page.setContent(`<html><body style="margin:0;background:#fff">${svg}</body></html>`)
      await page.screenshot({ path: output, clip: { x: 0, y: 0, width: w, height: h } })
    } else {
      throw new Error("unknown command " + cmd)
    }
  } finally {
    await browser.close()
  }
})().catch((e) => {
  console.error(e.message)
  process.exit(1)
})
