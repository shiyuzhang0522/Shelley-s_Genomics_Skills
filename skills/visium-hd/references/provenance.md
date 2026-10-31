# Provenance and coverage

Public-edition note: the conversion and image checks below document the original source-reading review. Those full-text/image packets are not bundled in this repository; [paper sources](paper-sources.md) provides retrieval links. Authored interpretation and scientific execution limits are retained.

## Sources

- Oliveira, Romero, Chung et al. **High-definition spatial transcriptomic profiling of immune cell populations in colorectal cancer**, Nature Genetics 57, 1512–1523 (2025). DOI [10.1038/s41588-025-02193-3](https://doi.org/10.1038/s41588-025-02193-3). [PMC12165841](https://pmc.ncbi.nlm.nih.gov/articles/PMC12165841/).
- Publisher main PDF: https://www.nature.com/articles/s41588-025-02193-3.pdf. The 28-page file includes main figures, methods, extended-data figures and reporting-summary pages. Europe PMC full-text XML was independently read to cross-check Methods and source inventory.
- Author code: [10XGenomics/HumanColonCancer_VisiumHD](https://github.com/10XGenomics/HumanColonCancer_VisiumHD/tree/df5801cf5e681b33b5026626989a7635fdf26b99), reviewed at commit `df5801cf5e681b33b5026626989a7635fdf26b99` on 2026-10-28.
- Archive: [Zenodo 15042463](https://zenodo.org/records/15042463), DOI 10.5281/zenodo.15042463, published 2025-03-17. Downloaded archive MD5 `bde1f1a374511923af4b98aa58bec421` agrees with the record. All 20 analysis R/Python/YML files and LICENSE match the reviewed GitHub snapshot after ignoring terminal newlines; README differs. No claim that all binary metadata files were compared.
- Original data links: https://www.10xgenomics.com/products/visium-hd-spatial-gene-expression/dataset-human-crc and [GSE280318](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE280318).

The bundled [source manifest](source-manifest.json) records snapshot hashes. Source files are retained as evidence, including author defects; don't source them blindly. They were fetched through GitHub and include an added terminal newline from local materialization. No scientific code was silently repaired in this snapshot. The README image link points to the pinned original image rather than bundling a duplicate illustration.

## Scope and limits

The skill teaches both annotation branches and the three-section downstream workflow; it does not provide a newly validated, executable end-to-end pipeline. Full Space Ranger matrices, images and multimodal inputs were not downloaded or run. No RCTD fitting, cell segmentation, biological benchmarking or figure reproduction was executed during skill creation.

Supplementary Note 1, the standalone reporting-summary file and separate supplementary/source-data workbooks could not be retrieved through the attempted publisher/PMC/Europe PMC endpoints (server errors, timeout or non-PDF response). They are inventoried in the paper but their standalone contents are not verified or bundled. Main-PDF extended data and reporting-summary pages 26–28 are included and reviewed. Peer review and zipped segmentation data were not reviewed. Retrieve these originals if a future task depends on their exact contents; do not infer table values from titles.

Paper2Skill generated the reading package. The model-based PDF layout engine attempted unrelated telemetry and was blocked; extraction instead uses the legacy local text engine without that layout dependency, with source-page images and manual page review. Its evidence serialization converts legacy Rect objects to coordinate arrays. Source image rendering uses explicit PNG byte writes to avoid sporadic zero-byte files from Pixmap.save; the package verifier checks the resulting pixels against the original source regions. Record extraction limitations in the generated paper package rather than treating layout fallback as an unqualified native-text conversion.

The original sources contain inconsistencies, retained rather than silently corrected: Methods gives ages 58–72 whereas Table 1 lists P3 as 83; some text/captions describe nine broad types while Methods says ten. The code map distinguishes named lineages from Unknown. Original reporting-summary typography spells spacexr as “spacrxr v2.2.1”.

## Reproduction versus adaptation

Use exact author settings only when reproducing the original study and when the relevant code branch supports them. The paper's 15% versus code's 240000 sketch, explicit minimum 100 UMIs versus an omitted RCTD threshold argument, ROI selections and region definitions are recorded differences, not interchangeable descriptions. The source's hard-coded label vectors are historical results, not annotation rules for new data.

For three melanoma samples, the workflow design can transfer but the reference, markers, malignant-cell evidence, states, ROIs and thresholds need biological review. Do not describe changes as exact CRC reproduction. Add batch correction only with a stated rationale and retain raw counts for count-based models.

## Attribution

The article states CC BY-NC-ND 4.0: https://creativecommons.org/licenses/by-nc-nd/4.0/. Retain source attribution and distinguish original paper text/images from newly authored procedural guidance. Author code has its own [10x Genomics license](source-code/LICENSE.md), including use in connection with 10x products/data. Zenodo's record-level license does not replace the license included with code.

## Validation at creation

Paper2Skill strict verification passed on 2026-10-28 with status `reviewed_with_limitations`: all 28 pages reviewed; mechanical checks passed with no issues; 18 exact source-checked numeric/parser adjudications applied, none stale. The 22 final image/table assets match source conversions. Original article wording and figures are retained, with source-specific typography/table and extraction limitations documented. Host skill-format validation passed. A fresh read-only trial successfully derived the three-melanoma-section plan and distinguished merging from correction, 240000 from a dynamic 15%, source portability defects and nuclear annotation extensions. Independent source-image/Methods spot-checks found no substantive mismatch in the checked material; this does not validate execution of the scientific workflow.

For installation, figure copies use a 2400-pixel maximum side and JPEG quality 60, preserving full panels; inspect the linked original PDF for finer detail. Text, captions and table are unchanged from the independently checked high-resolution build. Compact figure-label readability was spot-checked after conversion.

The strictly verified Paper2Skill reading package is embedded as a component of one installed skill. Its nested entry file is named WORKFLOW.md in the installed component, matching the existing Paper2Agent component convention; all reading text, assets and entry-file bytes are unchanged. The outer SKILL.md is the sole installed skill entry. This packaging rename is checked separately from the original strict conversion result.
