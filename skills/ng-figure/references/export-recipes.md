# R and Python export recipes

## R / ggplot2

Prefer Cairo PDF; verify `capabilities("cairo")`. Avoid showtext for final vector text because glyphs can become outlines. Resolve fonts explicitly; generic sans does not guarantee Arial.

```r
library(ggplot2)
library(systemfonts)
font_candidates <- c("Arial", "Helvetica", "Liberation Sans", "DejaVu Sans")
installed <- unique(systemfonts::system_fonts()$family)
available <- font_candidates[font_candidates %in% installed]
if (!length(available)) stop("Select an installed sans-serif font.")
font_family <- available[[1]]
if (!font_family %in% c("Arial", "Helvetica")) warning("Fallback font: ", font_family)
ng_theme <- theme_classic(base_size = 7, base_family = font_family) +
  theme(text = element_text(colour = "#222222"),
        axis.text = element_text(size = 7, colour = "#222222"),
        axis.title = element_text(size = 7),
        legend.text = element_text(size = 7),
        legend.title = element_text(size = 7),
        strip.text = element_text(size = 7),
        plot.title = element_text(size = 7),
        plot.subtitle = element_text(size = 7),
        plot.caption = element_text(size = 6),
        plot.tag = element_text(size = 8, face = "bold"),
        axis.line = element_line(linewidth = 0.18),
        axis.ticks = element_line(linewidth = 0.18))
# geom_text() sizes are usually mm, unlike theme text sizes in points:
# use size = 7 / ggplot2::.pt or a supported size.unit = "pt".
export_ng_pdf <- function(p, path, width_mm, height_mm, font_family) {
  stopifnot(width_mm > 0, width_mm <= 180, height_mm > 0)
  if (!capabilities("cairo")) stop("Configure a verified alternative PDF device.")
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  grDevices::cairo_pdf(filename = path, width = width_mm / 25.4,
                      height = height_mm / 25.4, family = font_family,
                      bg = "white", fallback_resolution = 600)
  on.exit(grDevices::dev.off(), add = TRUE)
  print(p)
  message("PDF written: ", path, " (", width_mm, " x ", height_mm, " mm)")
}
# Create p from supplied data, then:
# export_ng_pdf(p + ng_theme, "output/figure.pdf", 90, 75, font_family)
```

For base R, draw inside the managed device. If Cairo is absent, base PDF with `useDingbats = FALSE` plus verified font embedding is an alternative. That flag alone does not embed fonts. Inspect mathematical expressions for additional fonts.

R verification at skill creation: reviewed but not executed because R was unavailable. Run in the target R environment before claiming validation.

## Python / Matplotlib

Copy the small functions in `scripts/ng_style.py` into a self-contained script, or import them when the helper is distributed with it. Configure before creating artists. Use explicit dimensions and avoid `bbox_inches="tight"`. Add 8 pt bold panel tags separately. Resolve glyph coverage; mathtext may add fonts requiring inspection. Do not enable external LaTeX without checking output fonts.

## PDF checks

```bash
python inspect_pdf.py output/figure.pdf --width-mm 90 --height-mm 75
pdffonts output/figure.pdf
pdftotext output/figure.pdf -
pdftoppm -scale-to 1600 -png -singlefile output/figure.pdf /tmp/figure-preview
```

Inspect embedded status, actual font names, Type 3, glyphs and text extraction. Never fix extraction by outlining. Render every page. Checks do not replace native Illustrator editing and macOS Preview testing.
