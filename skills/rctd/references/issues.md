# GitHub issue evidence and troubleshooting

Reviewed selected high-discussion, topic-specific and recently updated issues on 2026-10-31. This is a targeted review, not an exhaustive review of every issue. Read linked threads again when debugging a newer release. An open issue, a user workaround or a closed status is not proof of a general fix.

## Interpretation and inputs

| Issue | Evidence and actionable conclusion |
|---|---|
| [108](https://github.com/dmcable/spacexr/issues/108#issuecomment-1263553481) | Maintainer: units are proportions of counts/UMIs; conversion to cells needs UMI-per-cell factors. Do not assume all types have equal captured RNA. |
| [159](https://github.com/dmcable/spacexr/issues/159#issuecomment-1577218989) | Maintainer: distinguish mRNA fractions from cell numbers; inspect fitted marker genes spatially when results disagree with expected biology. Review gene lists before blindly changing optimization. |
| [45](https://github.com/dmcable/spacexr/issues/45#issuecomment-944821237) | Maintainer: legacy `weights` is full fit, `weights_doublet` is pair fit; ignore pair weights for singlets; normalize full weights. First type need not have largest weight. Use `spot_class` and convergence. The comment has a wording typo for singlet score; current code defines its computation. |
| [193](https://github.com/dmcable/spacexr/issues/193#issuecomment-2018606601) | Community points to normalization in the vignette. Verified independently in `normalize_weights`: row division by total. Zero/nonfinite totals still require checking. |
| [49](https://github.com/dmcable/spacexr/issues/49#issuecomment-976798611) | Maintainer permits noninteger **linear-scale** reference expression via `Reference(..., require_int=FALSE)`. This exception is not for log-space, residuals, embeddings or arbitrary negative integration outputs. Default to raw counts; document provenance, denominator and altered QC units for an exception. |
| [49, abundance](https://github.com/dmcable/spacexr/issues/49#issuecomment-983665997) | Maintainer: reference cell-type frequencies are not used as target composition. It is unnecessary to match reference and tissue proportions. Adequate cells per type still matter for stable profiles. |
| [109](https://github.com/dmcable/spacexr/issues/109#issuecomment-1294884082) | Maintainer allows combined references and direct average profiles if linear-scale semantics are correct. Integration for annotation need not replace raw counts used for estimation. Avoid selecting a reference solely because it is large. |
| [77](https://github.com/dmcable/spacexr/issues/77#issuecomment-1145950102) | Maintainer resolved a large-reference failure by avoiding a huge data.frame conversion. Keep sparse matrix inputs; dense internal stages still need memory. |

## Resolution, modes and sample handling

| Issue | Evidence and actionable conclusion |
|---|---|
| [230](https://github.com/dmcable/spacexr/issues/230#issuecomment-3091287180) | Maintainer: neither full nor multi dominates universally. Full spreads small weights across more types; multi suppresses many of them. Biology determines whether minority weights are real. Use sensitivity analysis. |
| [229](https://github.com/dmcable/spacexr/issues/229#issuecomment-3091289110) | Maintainer prioritizes explicit gene-name checks. Community notes low-depth HD can trigger the overlap error after bulk-count filtering. Code confirms both mechanisms. The denominator is `min(reference_gene_count, spatial_gene_count)` before intersection; postfilter overlap below 10% triggers the error. Diagnose identifiers and sparsity separately. |
| [160](https://github.com/dmcable/spacexr/issues/160) | Reports of merged slides retaining only one image; a community workaround aggregates coordinate tables. It is not a maintainer endorsement of pooling all samples. Check all slide-specific coordinates and barcode alignment; use sample-level runs when appropriate. |
| [239](https://github.com/dmcable/spacexr/issues/239) | User reports first/second weight ordering confusion. No maintainer resolution was present in retrieved comments; use issue 45 and source code, not label rank assumptions. |
| [255](https://github.com/dmcable/spacexr/issues/255) | No retrieved answer about class scores. Documentation/source define class flags; they do not create posterior class probabilities. Map `first_type` through `class_df` when `first_class=TRUE`. |

## Runtime and source caveats

| Issue/source | Evidence and response |
|---|---|
| [227](https://github.com/dmcable/spacexr/issues/227) | Community reports missing worker functions and a one-core workaround. Maintainer acknowledges backend concerns. Start serial, inspect worker library paths and identical package installs, then retry limited parallelism. Third-party forks and alternate backends are not automatically validated fixes. |
| [253](https://github.com/dmcable/spacexr/issues/253), [250](https://github.com/dmcable/spacexr/issues/250) | Reports of multicore hangs/errors; retrieved comments include community alternatives, not a verified upstream resolution. Capture logs, memory, CPU allocation, backend and serial comparison. Do not install unsolicited forks or assume increasing cores will help. |
| [247](https://github.com/dmcable/spacexr/issues/247) plus `create.RCTD` source | No retrieved comments; source directly shows reference downsampling to five cells/type when `keep_reference=FALSE`, after profile estimation. The stored reference is not the full training reference. |
| `create.RCTD(...,cell_type_profiles=...)` | Although docs say reference is ignored, inspected legacy code still downsamples `reference` when `keep_reference=FALSE` and the S4 class needs a Reference object. Do not promise a reference-free drop-in call without testing that version. |
| `export.RCTD`, `subset_rctd` | Source inspection found fragile helper behavior: export refers to `myRCTD` instead of its argument; subset updates only selected slots. Prefer explicit saved RDS and aligned result-table exports; do not assume a partially subset S4 object is coherent. These are code observations, not runtime-confirmed bug reports. |

## Debug in this order

1. Record installed implementation, version, session, exact failing call and full traceback.
2. Inspect matrix orientation, values, zero-library cells, label factor levels, barcodes and gene namespaces.
3. Count retained spots, genes after bulk-count filters, informative markers per type, and sigma-eligible spots.
4. Run a representative one-core pilot with the same input data semantics.
5. Inspect biological reference mismatch and selected genes before altering thresholds.
6. Change one justified parameter at a time, retaining original outputs and configuration. Do not lower filters merely to remove an error.
7. If needed, prepare a minimal reproducible issue with synthetic/deidentified data; do not post it without explicit authorization.
