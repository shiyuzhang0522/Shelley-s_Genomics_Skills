---
name: ng-figure
description: Create or refine Nature Genetics-compatible scientific figures and reproducible R or Python plotting scripts. Use when Shelley requests Nature Genetics or NG figure styling, publication-ready plots explicitly targeting that journal, matching typography or dimensions, restrained palettes, or editable PDF export for Adobe Illustrator and macOS. Apply to new plots, existing scripts, and final figure checks.
---

# NG_Figure.Skill

Create scientifically faithful, legible figures at final publication size. Always include PDF export in plotting code; generate the PDF when data and execution are available. Apply these rules to R and Python.

## Establish the task

Identify the scientific comparison, columns, units, language, output path, and whether the output is a panel, assembled main figure, Extended Data figure, or Supplementary Figure. Use provided context; ask only for information that materially changes the result. Do not repeatedly request approval for routine refinements or authorized exports.

For script-only requests, provide runnable export code. Do not invent data or claim the real figure was generated. Label toy examples explicitly. Preserve analyses, validated mappings and thresholds; never filter observations for visual appeal.

## Resolve requirements

Read [journal requirements](references/journal-requirements.md). At a new manuscript or final submission pass, verify current official Nature Genetics guidance and record the source and date. Reuse that snapshot within the task. If access fails, use the dated snapshot and state the limitation while continuing useful work.

Apply manuscript-specific editor instructions first, then current Nature Genetics rules, applicable general Nature advice, and house preferences. Distinguish rules from design defaults. Do not import flagship Nature's 183 mm width into an NG figure with a verified 180 mm maximum.

| Setting | Default | Basis |
|---|---|---|
| Single-column width | 90 mm | House choice; not a verified NG column specification |
| Full-width figure | 180 mm | Verified NG maximum |
| Ordinary text | 7 pt, within 5–7 pt at final size | NG requirement |
| Panel tags | 8 pt bold upright lowercase | General Nature advice adopted as house style |
| Typeface | Arial, or Helvetica if available | Standard sans serif; verify actual font |
| Axes/lines | Usually 0.5–0.75 pt | House choice |
| Background/master | White, RGB, PDF | User preference and applicable guidance |

Choose height from content and caption space; do not invent an NG height limit. Recalculate text and mark sizes after any assembly or resizing. Specify dimensions in millimetres; convert to inches with mm / 25.4.

## Design

- Use near-black text, white backgrounds, restrained borders and explicit axes/units. Remove decorative effects and unnecessary gridlines; retain meaningful reference lines.
- Use as few colors as necessary. Keep named group-to-color mappings consistent across panels. Prefer neutral context with one accent for the primary comparison.
- Use low-to-moderate saturation without sacrificing contrast. A muted palette is not automatically accessible. Check color-vision deficiency and grayscale when feasible; use shapes, labels or line styles when color alone is insufficient.
- Use sequential scales for magnitude and diverging scales around meaningful midpoints. Avoid rainbow continuous scales. For many categories, consider faceting or hierarchy before adding colors.
- Align panels and margins; match scales when comparisons require them. Manage long labels without shrinking below the required size.
- Distinguish gene symbols from proteins; use appropriate species-specific italics. Define transformations, relevant genome build, thresholds, sample counts and uncertainty from supplied information.
- Explain visible axis breaks. Never silently clip data or uncertainty, invent sample counts or tests, or replace underflowed P values with invented values.
- Prefer “Non-Outliers” for the middle group when that is the intended grouping.

## Implement and export

Read [export recipes](references/export-recipes.md). Use the requested language and preserve an existing workflow. Organize scripts into a concise header, packages/inputs, centralized settings, data checks, plotting, and export/QC. Include progress messages and relevant version information. Seed only operations that use randomness.

Make requested scripts self-contained: copy small helper functions rather than depending on private skill paths on the user's Mac or cluster. Honor supplied output directories and create missing folders. Do not overwrite input data.

Keep text editable and graphical elements vector where practical. Do not outline fonts, use showtext for final vector text, or rasterize the whole plot to hide font problems. Check font availability explicitly; prefer Arial/Helvetica and disclose fallback fonts. Do not download proprietary fonts.

Use Cairo PDF in R when available and Matplotlib PDF fonttype 42. Inspect output rather than treating settings as a guarantee. For very dense data, selectively rasterize only the dense layer at a documented resolution of at least 300 dpi at final size (600 dpi house default); preserve vector labels and axes. DPI does not improve vector resolution.

Preserve exact PDF dimensions. Avoid Matplotlib tight-bounding-box export or subsequent cropping that changes page size. Fix margins inside the canvas. Keep the PDF master even if a submission system requires an additional format.

## Inspect and deliver

Run `python scripts/inspect_pdf.py figure.pdf --width-mm WIDTH --height-mm HEIGHT` when PyMuPDF and Poppler are available. Confirm dimensions, embedded fonts, no Type 3 fonts, extractable text and intended rasterization. Treat small superscripts contextually; images in microscopy and heatmaps are not inherently defects.

Render the actual exported PDF and visually inspect all pages, including final-size readability, clipping, overlap, legend mappings, glyphs, panel tags and scientific correspondence. Fix concrete defects; repeat only affected checks. Technical inspection is not a journal acceptance certificate.

Open in Illustrator and macOS Preview when available to test appearance and editing. Otherwise explicitly state those native-app tests were not performed. Linux rendering and font embedding do not prove native compatibility; editing embedded subsets may require the matching installed font.

Deliver the requested script/PDF, dimensions, actual font and a concise validation result. Disclose material limitations such as an unexecuted script or fallback font. Do not claim full compliance while known requirements remain unresolved. Use normal persistent storage for user-facing artifacts; keep disposable QC previews temporary.
