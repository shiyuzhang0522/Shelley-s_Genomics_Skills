# Evidence and validation record

Public-edition note: the conversion and image checks below document the original source-reading review. Those full-text/image packets are not bundled in this repository; [paper sources](paper-sources.md) provides retrieval links. Authored interpretation and scientific execution limits are retained.

Reviewed 2026-10-31. This operational skill is usable with the boundaries below; it is not a claim of full supplementary-method reproduction or a runtime-tested R pipeline.

## Primary article

Cable et al., **Robust decomposition of cell type mixtures in spatial transcriptomics**, Nature Biotechnology 40, 517–526 (2022), online 2021. [DOI](https://doi.org/10.1038/s41587-021-00830-w); [accessible manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC8606190/).

Read all 15 pages of the user-supplied main PDF, including the six main figures, complete Methods, captions, references and two appended reporting-summary pages. Two page reviewers independently inspected pages 1–5 and 6–10; the coordinator inspected pages 11–15. A fresh verifier checked the assembled packet against visible originals. Input SHA-256: `0ebc7097accef89f46f3bda1d62484ec66caa03d207df4532f9ac2e73bea87fa`. Page plans, review reports, exact diagnostic adjudications and verification records were retained in the external Paper2Agent review directory.

The [reading packet](paper-sources.md) now contains the article text with source figure/equation images, replacing the earlier authored-notes-only packet. Two-column reading order and cross-page prose were repaired. Difficult equations retain source-image authority; reporting-summary pages are image-only because OCR was unreliable. Main figures and their full captions were checked. Paper2Agent strict verification passed with `reviewed_with_limitations`: all 15 pages reviewed, all 21 image assets matched source transformations, 17 specific parser/image-overlap diagnostics adjudicated against visible originals, and no unresolved or stale diagnostics. The converter's entry point is packaged as a reading guide rather than a nested installed skill. See [scientific interpretation](main-pdf-review.md) for benchmark qualifications and the original Figure 3 panel-reference inconsistency.

## Supplementary Information

Read all 71 pages of the subsequently supplied Supplementary Information, SHA-256 `694e566a4832f67a7c4df9ee94ad6cd2da2a821d5cbd8f89bdd2c3686102e173`. Five reviewers covered exclusive page ranges 1–11, 12–30, 31–48, 49–64 and 65–71. A fresh independent verifier compared the assembled mathematical source pages, all 27 figure crops and captions, experimental prose and Table 1 against visible originals. One minor Figure 2 title/body paragraph join was repaired. All seven rows of Table 1 were additionally transcribed into checked string-cell CSV form.

The [supplement source packet](paper-sources.md) preserves complete source pages 1–11 as images with searchable genuine headings, followed by searchable experimental methods/captions and complete figure crops. This image authority is deliberate: native extraction corrupts equation symbols and indices. The [practical interpretation](supplement-review.md) and [mathematical audit](supplement-mathematics.md) distinguish authored derivations and corrections from original source content. Printed formula/legend inconsistencies are preserved, not silently repaired. The separate Supplementary Table 2 cited by the main article was not included in this PDF and remains unreviewed.

Paper2Agent final build and separate strict verification passed (`reviewed_with_limitations`, exit 0): all 71 pages reviewed; 38 source-image transformations and the table export checked; all 39 delivered assets matched deterministic conversion; 28 exact-fingerprint parser/image-overlap diagnostics adjudicated against visible originals; no unresolved or stale diagnostics. The final packet differs from the independently reviewed staging only in its verified status and the Figure 2 paragraph break. Installed generated references/assets were byte-compared with the final packet; its entry is adapted to a reading guide to avoid a nested installed skill.

The main packet’s original conversion notes about an unavailable supplement describe that earlier conversion; its reading guide now directs readers to this companion packet. Source conversion checks do not certify the biological accuracy of RCTD, numerical reproduction of distributed likelihood tables or a working R runtime.

## Code and documentation

Original source pinned at [9f5dc33c8060f946c6072a138b70e189636e1435](https://github.com/dmcable/spacexr/tree/9f5dc33c8060f946c6072a138b70e189636e1435), DESCRIPTION 2.2.1. Read README, documentation/README and spatial-transcriptomics, Visium full/multi and replicate tutorials. Inspected Reference, SpatialRNA, processRef, spacexr, runRCTD, RCTD_helper, platform_effect_normalization, prob_model, IRWLS, utils and postProcessing source for the documented paths. This is targeted RCTD source review, not a line-by-line audit of every C-SIDE function.

The upstream README recommends the Bioconductor adaptation for RCTD. Inspected the [adapted fork at 4bce0a43cd084cb86a94d64e2704b1ca9d711604](https://github.com/ggrajeda/spacexr/tree/4bce0a43cd084cb86a94d64e2704b1ca9d711604): DESCRIPTION 1.1.1, tutorial, create_RCTD, run_RCTD, Reference, RCTD_helper, process_beads and post_processing. This is a repository snapshot, not a claim about the currently installed Bioconductor release. [Official tutorial](https://bioconductor.org/packages/release/bioc/vignettes/spacexr/inst/doc/rctd-tutorial.html).

Key reconciliations: RNA versus cell fractions; mean-of-ratios reference profiles; raw unconstrained full weights; paper versus public-API thresholds; legacy versus adapted orientation; uncertain singlet-like adapted reporting; conditional renormalization in adapted multi mode; no spatial smoothing; calibration dependence on the target dataset. Exact code links and parameter tables are in [versions](versions.md) and [methods](methods.md).

## Issue coverage

Searched high-discussion, recent and topic-specific issues and inspected threads 45, 49, 77, 108, 109, 159, 160, 193, 227, 229, 230, 239, 247, 250, 253 and 255. The [issue guide](issues.md) separates maintainer statements, community workarounds and source-derived observations. This is selected coverage, not every repository issue. Recheck threads and installed code for new failures.

## Validation performed

- Independent forward use on an 8-micron melanoma HD scenario caught the API/orientation mismatch, missing normal melanocyte reference, RNA-to-cell interpretation, unsupported two-type assumption and one-donor pseudoreplication. No blocking conceptual guidance gap remained.
- An independent reviewer exercised the Python legacy-results auditor with 26 synthetic CLI cases: full normalization; singlet/pair/uncertain/reject semantics; convergence/class flags; barcode reconciliation; duplicate/missing identifiers; nonfinite/negative/zero values; and overwrite refusal. Two defects involving missing/whitespace first identities were fixed. All 26 cases passed the rerun with no tested regressions.
- The Python checks validate exported-table semantics, not the accuracy of an RCTD fit. The auditor deliberately does not accept Bioconductor confidence-filtered assays or legacy multi outputs.
- A fresh forward-use check after supplement integration correctly handled a conventional Visium melanoma example: non-unit raw weights, missing normal melanocytes, RNA-versus-cell interpretation, mode choice, shared-reference bias, convergence limitations and historical/current sigma differences. It kept printed formula defects separate from unsupported runtime-failure claims.
- R and spacexr were not installed in the authoring environment. R templates were matched to inspected source signatures/structures but not executed. No real dataset, fit convergence, sensitivity result or runtime benchmark is claimed.

Before production use, inspect the user's installed package and run a representative one-core pilot. Save input/retained barcode counts, effective configuration, selected genes, reference label counts, sigma-eligible spots, warnings, output structure and biological validation. Check parallel execution separately before scaling. A source-reviewed template is not evidence that a particular environment or dataset works.
