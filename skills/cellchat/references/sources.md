# Sources, coverage, and validation

## Version baseline and citation

Reviewed 2026-10-25. Repository: [jinworks/CellChat](https://github.com/jinworks/CellChat/tree/75253cd0c9e68410e6e721a6d3a0419a1d7e358f), commit `75253cd0c9e68410e6e721a6d3a0419a1d7e358f`, DESCRIPTION version `2.2.0.9001`, GPL-3. The code snapshot is the reproducibility anchor; NEWS stops at 2.1.2 and is not the full current-version specification. This skill contains original synthesis/adapted guidance and an original validator, not a copy of the papers or upstream implementation.

- Jin S et al. *Inference and analysis of cell-cell communication using CellChat*. Nature Communications 12, 1088 (2021). [DOI](https://doi.org/10.1038/s41467-021-21246-9), [full main article](https://pmc.ncbi.nlm.nih.gov/articles/PMC7889871/).
- Jin S, Plikus MV, Nie Q. *CellChat for systematic analysis of cell–cell communication from single-cell transcriptomics*. Nature Protocols 20, 180–219 (2025), online 16 September 2024. [DOI](https://doi.org/10.1038/s41596-024-01045-4), [NSF repository copy](https://par.nsf.gov/servlets/purl/10560563). Cite this protocol for versions >=1.5 as requested by the authors; retaining the 2021 citation also credits the core method.

The current README advertises [SpatialCellChat v3](https://github.com/jinworks/SpatialCellChat) separately. This skill is a v1/v2 skill, with v3 routing guidance, not a comprehensive v3 tutorial audit.

## Narrative documentation reviewed one by one

The nine Rmd tutorials/FAQ are the authored prose/code sources for their rendered HTML counterparts. All were read completely. Blob identifiers were checked against the retrieved content after removing the single newline added by scratch serialization. HTML graphics were not separately rendered/reviewed, and author-local example data paths were not executed.

| Source | Coverage | Git blob prefix |
| --- | --- | --- |
| [DESCRIPTION](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/DESCRIPTION) | Full text/code read | 32f8d25b4ec1 |
| [NEWS.md](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/NEWS.md) | Full text/code read | 37fbf35aac2c |
| [README.md](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/README.md) | Full text/code read | b72e4cdaf58a |
| [tutorial/CellChat-vignette.Rmd](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/tutorial/CellChat-vignette.Rmd) | Full text/code read | 4270a1715d00 |
| [tutorial/CellChat_analysis_of_multiple_spatial_transcriptomics_datasets.Rmd](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/tutorial/CellChat_analysis_of_multiple_spatial_transcriptomics_datasets.Rmd) | Full text/code read | de318d853be9 |
| [tutorial/CellChat_analysis_of_spatial_multiomics_data.Rmd](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/tutorial/CellChat_analysis_of_spatial_multiomics_data.Rmd) | Full text/code read | 903aacae44b5 |
| [tutorial/CellChat_analysis_of_spatial_transcriptomics_data.Rmd](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/tutorial/CellChat_analysis_of_spatial_transcriptomics_data.Rmd) | Full text/code read | 4cb469374006 |
| [tutorial/Comparison_analysis_of_multiple_datasets.Rmd](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/tutorial/Comparison_analysis_of_multiple_datasets.Rmd) | Full text/code read | 89d745a6457c |
| [tutorial/Comparison_analysis_of_multiple_datasets_with_different_cellular_compositions.Rmd](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/tutorial/Comparison_analysis_of_multiple_datasets_with_different_cellular_compositions.Rmd) | Full text/code read | 76fea5e7fdee |
| [tutorial/FAQ_on_applying_CellChat_to_spatial_transcriptomics_data.Rmd](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/tutorial/FAQ_on_applying_CellChat_to_spatial_transcriptomics_data.Rmd) | Full text/code read | 4786bc82e4be |
| [tutorial/Interface_with_other_single-cell_analysis_toolkits.Rmd](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/tutorial/Interface_with_other_single-cell_analysis_toolkits.Rmd) | Full text/code read | 790a0e82acd9 |
| [tutorial/Update-CellChatDB.Rmd](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/tutorial/Update-CellChatDB.Rmd) | Full text/code read | b2114d413ab7 |

Additional targeted implementation review: [modeling.R](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/R/modeling.R), [CellChat_class.R](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/R/CellChat_class.R), [utilities.R](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/R/utilities.R), [analysis.R](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/R/analysis.R), and [database.R](https://github.com/jinworks/CellChat/blob/75253cd0c9e68410e6e721a6d3a0419a1d7e358f/R/database.R). This is not a claim that every API manual page or every source line was audited.

## Paper review scope

The 2021 main article's introduction/results/discussion/methods, equations, and all seven main figure captions were read. All seven main figures were visually inspected, including RNAscope panels. Supplementary PDF access was blocked, so supplementary notes/tables/figures are not independently verified. The Figure 2 HTML caption reverses e/f relative to the image (e centrality, f LR contribution); use the actual panel labels.

The full protocol was retrieved from NSF: all substantive text, Procedures 1–3, Box 1, troubleshooting Table 1, and all four main figures were reviewed. The PDF's two reporting-summary pages were visually inspected. Its detailed workflow is scRNA-seq, not a full spatial protocol. The source is copyrighted; the skill stores original notes and source links rather than redistributing it.

Paper2Skill packages original reviewed method notes as a separate development reading bundle. Its mechanical verification concerns faithful packaging of those notes, not full-article transcription or verification of inaccessible supplements.

## Issues and external calibration

Reviewed the bodies and returned comment threads for 19 selected live-repository issues: 6, 10, 16, 18, 20, 53, 68, 77, 92, 108, 185, 224, 226, 297, 300, 305, 364, 375, 397. They cover input alignment, spatial units, API renaming, replication, size weighting, missing groups/lifting, plotting, and installation. See troubleshooting.md for per-issue links and evidence status. This is targeted issue review, not a claim to have read the whole tracker. Maintainer comments, source-confirmed behavior, and unresolved user reports are kept distinct.

Official [Space Ranger spatial outputs](https://www.10xgenomics.com/support/software/space-ranger/latest/analysis/spatial-outputs) was consulted for calibration and HD coordinate-field semantics where the FAQ generalization was unsafe.

## Validation performed

- Skill format and local-link checks.
- R 4.3.3 execution of the original input validator on dense and sparse inputs, including misordered barcodes, invalid expression, duplicate symbols, missing/invalid labels, coordinate alignment, invalid calibration, custom sample-column canonicalization, preserved factor order, and conflicting sample labels.
- Numerical smoke tests using the unmodified pinned upstream R source (loaded into an isolated test session): Hill score on a known synthetic example, label-permutation reproducibility, optional population factor, exact min.cells exclusion, p=0.05 aggregation boundary, both/either endpoint selection, and complex geometric means/zero subunits. The empty-result export branch was executed and singleton-pathway guards were independently checked.
- These tests use a small synthetic database and selected source functions, not an installed full CellChat package or a real biological dataset. Full dependency installation, real-data end-to-end inference, plotting/UMAP/NMF, and spatial-neighbor computation remain outside the executed test scope.
- Independent forward-use and final artifact review completed; the discovered empty-result and custom-sample bugs were fixed and regression-checked. R example blocks were syntax-checked. These reviews are not external certification of biological validity.

For a new analysis, run a local pilot with the actual installed version, data modality, database, design, and intended figures. Record any changed defaults and recheck source-sensitive behavior.
