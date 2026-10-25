# Provenance and verification

Created 2026-10-22. This is an original operational skill using existing upstream implementations and format adaptation; no new deconvolution or GWAS method is implemented.

## Primary sources

- Ru et al. *Estimation of cell lineages in tumors from spatial transcriptomics data*. Nature Communications 14, 568 (2023). https://doi.org/10.1038/s41467-023-36062-6 ; full text https://pmc.ncbi.nlm.nih.gov/articles/PMC9895078/ . Paper-level concepts are summarized, not claimed as a page-verified paper package.
- SpaCET repository: https://github.com/data2intelligence/SpaCET at `eed9666a0d76507d46e70e5a168da2504086db0e`, DESCRIPTION version 1.4.0. Inspected README, DESCRIPTION, NAMESPACE, R/utilities.R, R/deconvolution.R, R/extensions.R and the SpaCET_object, visium_BC, hiresST_CRC and oldST_PDAC vignettes.
- Official tutorials: https://data2intelligence.github.io/SpaCET/articles/SpaCET_object.html ; https://data2intelligence.github.io/SpaCET/articles/visium_BC.html ; https://data2intelligence.github.io/SpaCET/articles/hiresST_CRC.html ; https://data2intelligence.github.io/SpaCET/articles/oldST_PDAC.html . Inspect source-pinned versions if live documentation has changed.
- gsMap repository: https://github.com/JianYang-Lab/gsMap at `ffb561db3e5a92ddabf7dc7b8f203c25e4d9f627`. Inspected docs/source/data_format.md, quick_mode.md, step_by_step.md, src/gsMap/find_latent_representation.py, latent_to_gene.py, config.py and cauchy_combination_test.py.
- User-linked extraction helper: https://github.com/shiyuzhang0522/Agent-Skill-Paper2Agent/blob/main/skills/paper2agent/paper2skill/scripts/pdf_to_skill.py . Its supported parent workflow uses paper_bundle.py for reviewed paper packages. No complete paper-PDF conversion or MCP server was requested/produced as part of this operational bridge.

## Source-backed interface details

SpaCET utilities rename 10x bins to array-row x array-column identifiers and retain barcodes in metadata. Input counts are genes × spots; propMat is lineages × spots. Constructor duplicate-gene filtering retains the greatest-expression row. Deconvolution stores `Ref$lineageTree` and the full propMat. Upstream dominant labels ignore Unidentifiable and pick the first tied maximum. These behaviors motivate identity joins, preserved fractions, explicit major-level selection and visible ambiguity handling in the bridge.

gsMap source, not only prose tutorials, establishes the current annotation-related 30-observation exclusion and within-annotation neighborhood behavior. These are version-specific and must be rechecked after upgrades.

## Validation scope

All 17 regression tests passed on 2026-10-22 after the final converter changes.

Synthetic tests cover an actual CLI invocation, h5ad round trip, shuffled fraction/label rows, hierarchy selection, ties, all-missing reviewed labels, predicted gsMap exclusions, raw sparse counts, and rejection of duplicate/missing IDs, duplicate genes, invalid fractions, non-count values, zero-count spots, incomplete HD metadata, invalid major-level totals and output overwrite. See scripts/test_bridge.py. Test environment: Python 3.12, anndata 0.11.4, pandas 2.3.3, numpy 2.5.4, scipy 1.18.1 and h5py 3.16.0. The host skill-format validator passed.

A fresh agent exercised an independent 62-spot fixture: all counts and IDs survived; an annotated policy correctly predicted 32 exclusions (a 29-spot class plus three unlabeled observations), while retaining all 62 input spots in the h5ad. Independent review identified native signature-selection provenance, matrix-versus-data.frame handling in the R export recipe, and PCA dimension prerequisites. These were clarified/fixed before installation. No real analysis was represented as completed by this test.

R recipes are source-checked; this environment does not provide R/SpaCET. Full tumor deconvolution, biological validation, gsMap model training, GWAS analysis and Visium HD runtime compatibility have not been executed by installing this skill.
