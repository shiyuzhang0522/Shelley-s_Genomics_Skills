# R and Python export recipes

## R / ggplot2

Prefer Cairo PDF after checking runtime device creation. Shelley chose to repair the missing macOS dependencies by installing official XQuartz, then restarting the login session and RStudio. Verify /opt/X11/lib/libSM.6.dylib and /opt/X11/lib/libXrender.1.dylib exist and run a real PDF export. Do not download isolated dylibs or create arbitrary symlinks. Native Quartz PDF is an explicit optional fallback; Quartz is distinct from XQuartz and does not need those X11 libraries. `capabilities("cairo")` alone does not prove DLL loading succeeds. Avoid showtext for final vector text because glyphs can become outlines. Resolve fonts explicitly; generic sans does not guarantee Arial.

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
export_ng_pdf <- function(p, path, width_mm, height_mm, font_family,
                          device = c("cairo", "quartz")) {
  device <- match.arg(device)
  stopifnot(width_mm > 0, width_mm <= 180, height_mm > 0)
  path <- path.expand(path)
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  tmp <- tempfile("ng-figure-", tmpdir = dirname(path), fileext = ".pdf")
  export_device <- NULL
  on.exit({
    if (!is.null(export_device) && export_device %in% grDevices::dev.list()) {
      grDevices::dev.off(export_device)
    }
    unlink(tmp)
  }, add = TRUE)
  withCallingHandlers({
    if (device == "quartz") {
      if (Sys.info()[["sysname"]] != "Darwin") stop("Quartz requires macOS.")
      if (!isTRUE(capabilities("aqua", Xchk = FALSE))) stop("Native Quartz unavailable.")
      grDevices::quartz(type = "pdf", file = tmp,
                       width = width_mm / 25.4, height = height_mm / 25.4,
                       family = font_family, pointsize = 7, bg = "white")
    } else {
      if (!isTRUE(capabilities("cairo", Xchk = FALSE))) stop("Cairo PDF unavailable.")
      grDevices::cairo_pdf(filename = tmp,
                          width = width_mm / 25.4, height = height_mm / 25.4,
                          family = font_family, bg = "white", fallback_resolution = 600)
    }
    export_device <- grDevices::dev.cur()
    print(p)
    grDevices::dev.off(export_device)
    export_device <- NULL
  }, warning = function(w) stop(conditionMessage(w), call. = FALSE))
  if (!file.exists(tmp) || file.info(tmp)$size < 5) stop("PDF was not created.")
  if (!identical(readBin(tmp, "raw", n = 5), charToRaw("%PDF-"))) stop("Invalid PDF header.")
  if (!file.copy(tmp, path, overwrite = TRUE)) stop("Could not save PDF to destination.")
  message("PDF written: ", normalizePath(path), " (", width_mm, " x ", height_mm, " mm)")
}

# Create p from supplied data, then:
# export_ng_pdf(p + ng_theme, "output/figure.pdf", 90, 75, font_family)
```

For base R, draw inside the managed device. When native Quartz and working Cairo are both unavailable, base PDF with `useDingbats = FALSE` plus verified font embedding is an alternative. That flag alone does not embed fonts. Inspect mathematical expressions for additional fonts.

R verification status: the original Cairo recipe failed in Shelley's macOS R 4.4 environment on 2026-10-16 because libSM.6.dylib and libXrender.1.dylib were unavailable under /opt/X11/lib. After installing XQuartz, Shelley confirmed both libraries were present and reported successful Cairo PDF export from the original RStudio test on 2026-10-16 (R 4.4.1, Apple Silicon). This is user-reported runtime success, not independent inspection of the exported PDF. The revised selectable-device helper above has been reviewed but has not itself been runtime-tested. Illustrator text editability and PDF font embedding remain unverified for the Mac output. A PDF header/file-size check establishes creation only, not font embedding, complete page validity or Illustrator editability.

Sources checked 2026-10-16:
- https://stat.ethz.ch/R-manual/R-devel/library/grDevices/html/quartz.html — native PDF device, dimensions in inches, output finalized on device closure.
- https://www.stat.ethz.ch/R-manual/R-devel/library/base/html/capabilities.html — aqua capability and Xchk control.
- https://www.stat.ethz.ch/R-manual/R-devel/doc/manual/R-admin.html — some macOS Cairo builds depend on XQuartz. Install/repair official XQuartz for Shelley’s chosen Cairo route; do not require it for native Quartz export. Official installer: https://www.xquartz.org/.

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
