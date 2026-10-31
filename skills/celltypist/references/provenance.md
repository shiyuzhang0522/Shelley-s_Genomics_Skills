# Sources and review limits

Public-edition note: the conversion and image checks below document the original source-reading review. Those full-text/image packets are not bundled in this repository; [paper sources](paper-sources.md) provides retrieval links. Authored interpretation and scientific execution limits are retained.

## Paper sources

- Domínguez Conde C, Xu C, Jarvis LB, et al. Cross-tissue immune cell analysis reveals tissue-specific features in humans. Science 376:eabl5197 (2022). https://doi.org/10.1126/science.abl5197
- User-supplied publisher PDF: 13 pages, comprising one-page research summary, 11-page main article including references and methods summary, and one publication-information page. Preserve its attribution and copyright notices.
- Supplementary Materials: 81 pages retrieved via the official EuropePMC supplementary-files endpoint for PMC7612735. Includes Materials and Methods, Supplementary Text, Figs S1–S26, Tables S1–S3. Source: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7612735/supplementaryFiles . Main open-access author manuscript: https://pmc.ncbi.nlm.nih.gov/articles/PMC7612735/ . The publisher PDF and author manuscript are distinct manifestations; do not assume identical pagination or wording.
- Source hashes and notebook identities are recorded in [source-manifest.json](source-manifest.json).

The supplement has severely corrupted native text encoding. Read source-rendered page images and reviewed descriptive summaries rather than treating corrupted extraction or unverified OCR as reliable text. Supplementary tables are image-based evidence, not validated machine-readable CSVs. Some source Table S3 cells visibly lack leading digits and some metrics appear internally inconsistent; no numerical values were invented to repair them. Obtain underlying data before quantitative reuse.

The main source contains discrepancies described in [paper-and-atlas.md](paper-and-atlas.md), including the Figure 3 hypermutation narrative/caption contrast and the SCL40A1 spelling. Supplementary L2 wording must not be interpreted as requiring positive coefficients. The original main 13 pages and all 81 supplementary pages are in review scope. The separately listed MDAR checklist is not included in the retrieved 81-page supplement and has not been reviewed.

## Code sources

- Official current CellTypist source audited at commit `fe357564a6625d3b1732a022fd39f18e55696e80`, version 1.7.1. See [software-provenance.json](software-provenance.json) for exact hashes, exercised paths and tested environment.
- Original paper software citation: version 0.1.6, https://zenodo.org/record/5736560 . This historical release is identified from the paper, not claimed to have been executed.
- Atlas notebook source audited at `49a5441d71e7315eae77d433da702f5b52eb4403`: https://github.com/Teichlab/TissueImmuneCellAtlas . Paper archive https://doi.org/10.5281/zenodo.6334988 was not assumed byte-identical to the inspected checkout.

## Execution and intended scope

Small synthetic CPU tests exercised current training, feature selection, model persistence, prediction, provided-cluster voting and outputs/CLI. These check software mechanics, not biological performance. No full atlas reproduction, downloaded public-model validation, GPU execution, automatic Leiden graph test, melanoma annotation or Visium HD analysis was performed. The skill's melanoma/spatial guidance is explicitly an adaptation requiring appropriate reference and independent validation.

Preserve normalized all-gene classifier inputs separately from batch-corrected graph/embedding data. Keep original predictions, majority-voted labels and manual labels distinct. This distinction follows both the paper and the audited current implementation rather than assuming batch correction was absent throughout the study.

## Review and conversion coverage

All 94 source pages (13 main and 81 supplementary) received visual review. The reading component preserves six main figure crops and 81 supplementary page images, with navigation for Figs S1–S26 and Tables S1–S3. Native extraction problems and source inconsistencies are explicitly retained as limitations. Independent review checked representative source pages, figures, implementation behavior and package navigation; a separate realistic-use exercise checked the operational guidance. These checks do not constitute independent reproduction of the biological study.

The Paper2Skill strict verifier passed with status `reviewed_with_limitations` and no unresolved issues. For embedding under this operational skill, its generated entry was renamed from `SKILL.md` to `WORKFLOW.md`; all other reading-component bytes were preserved and verified.
