# Implementations and version contract

Inspected 2026-10-31. Recheck installed exports/formals rather than assuming these snapshots remain current.

| Item | Original dmcable implementation | Bioconductor adaptation |
|---|---|---|
| Repository | [dmcable/spacexr](https://github.com/dmcable/spacexr) | [ggrajeda/spacexr](https://github.com/ggrajeda/spacexr) |
| Inspected revision | `9f5dc33c8060f946c6072a138b70e189636e1435` | `4bce0a43cd084cb86a94d64e2704b1ca9d711604` |
| DESCRIPTION at that revision | 2.2.1; R >=3.5.0 | 1.1.1; R >=4.5.0 |
| Inputs | `Reference`, `SpatialRNA` | `SummarizedExperiment`, optionally `SpatialExperiment` |
| Preparation | `create.RCTD` | `createRctd` |
| Fit | `run.RCTD(..., doublet_mode=...)` | `runRctd(..., rctd_mode=...)` |
| Results | S4 RCTD object | SpatialExperiment |
| Weight orientation | spots x types | types x spots |
| Full weights | raw `@results$weights`, row-normalize | raw `assay(result,'weights')`; column-normalize positive totals |
| Doublet selected results | `results_df`, `weights_doublet` | `colData`, `weights`, `weights_unconfident`, `weights_full` assays |
| Multi results | per-spot list | assays plus per-spot `colData` |
| C-SIDE | available; separate methodology | not implemented in inspected adaptation |

The fork DESCRIPTION is a pinned repository snapshot, not a claim about the latest Bioconductor release. Both install under the package name `spacexr`; use separate library/project environments if both are needed. Do not replace one silently.

```r
library(spacexr)
d <- packageDescription('spacexr')
print(d[c('Package','Version','RemoteRepo','RemoteRef','RemoteSha','Built')])
exports <- getNamespaceExports('spacexr')
print(intersect(exports, c('Reference','SpatialRNA','create.RCTD','run.RCTD',
                          'createRctd','runRctd')))
sessionInfo()
```

For original GitHub installation, pin the inspected revision for reproduction:

```r
remotes::install_github(
  'dmcable/spacexr', ref='9f5dc33c8060f946c6072a138b70e189636e1435',
  build_vignettes=FALSE, upgrade='never'
)
```

Resolve dependencies and record versions; `upgrade='never'` does not make an incompatible environment valid. For the adapted package, use `BiocManager::install('spacexr')` in a compatible, isolated Bioconductor environment and record the actual release/version. It need not match the development fork snapshot.

## Legacy effective defaults

Source: [R/spacexr.R](https://github.com/dmcable/spacexr/blob/9f5dc33c8060f946c6072a138b70e189636e1435/R/spacexr.R), [Reference.R](https://github.com/dmcable/spacexr/blob/9f5dc33c8060f946c6072a138b70e189636e1435/R/Reference.R).

| Argument | Value | Interpretation |
|---|---:|---|
| Reference `min_UMI` | 100 | Reference cell depth filter |
| Reference `n_max_cells` | 10000 | Random cap per reference type |
| `CELL_MIN_INSTANCE` | 25 | Minimum reference cells per type after QC |
| `gene_cutoff`, `fc_cutoff` | 0.000125, 0.5 | Bulk marker fraction and natural-log fold change |
| `gene_cutoff_reg`, `fc_cutoff_reg` | 0.0002, 0.75 | Per-spot regression marker thresholds |
| `UMI_min`, `UMI_max` | 100, 20000000 | Spatial total depth range |
| `counts_MIN` | 10 | Counts in the currently selected gene set per spot |
| `UMI_min_sigma` | 300 | Sigma estimation requires spots strictly above this |
| `MAX_MULTI_TYPES` | 4 | Multi-mode cap |
| `CONFIDENCE_THRESHOLD` | 5 | Alternative-fit score gap, not a probability |
| `DOUBLET_THRESHOLD` | 20 | Complexity penalty |
| `max_cores` | 4 | Must be adapted to allocated CPUs |
| `test_mode` | FALSE | TRUE changes several thresholds and iteration counts |
| `keep_reference` | FALSE | Retains only five reference cells per type after profiling |

Lower-level helpers still show 10/25 confidence/doublet defaults; `fitPixels` passes values from public `create.RCTD`. Do not copy lower-level or paper values as current public defaults.

## Bioconductor differences worth checking

The adaptation moves core count/mode-cap/confidence arguments to `runRctd`; reference cell thresholds are `ref_UMI_min`, `ref_n_cells_min`, `ref_n_cells_max`. It exposes `gene_obs_min` and `pixel_count_min` in `createRctd`. Read installed help before porting options. `UMI_min_sigma` controls sigma fitting, even where a docstring describes it broadly as platform normalization.

Assay naming has changed semantics: legacy `weights` is the full fit; adapted `weights` follows the selected mode. In the inspected `R/post_processing.R`, doublet-uncertain columns of the confident `weights` assay put weight one on the first type. This is a confidence-reporting convention, NOT evidence that the spot contains 100% RNA from that type. Multi-mode confident weights discard unconfident types and renormalize those retained; they are conditional on the retained set. `weights_unconfident` preserves the fitted candidate mixture, while `weights_full` preserves the unrestricted fit. Rejected/all-unconfident columns can be zero. Check `colData` and inspect sums; a transposed legacy CSV still does not acquire these confidence semantics.

In the inspected adaptation, full-mode `fitPixels` passes `constrain=FALSE` and `create_spe_full` copies the resulting weights without normalization. Preserve the raw assay and column-normalize finite nonnegative positive-total columns for RNA fractions. This source behavior takes precedence over simplified documentation claiming every full column already sums to one. Recheck after updates. Source: [RCTD_helper.R](https://github.com/ggrajeda/spacexr/blob/4bce0a43cd084cb86a94d64e2704b1ca9d711604/R/RCTD_helper.R), [process_beads.R](https://github.com/ggrajeda/spacexr/blob/4bce0a43cd084cb86a94d64e2704b1ca9d711604/R/process_beads.R), [post_processing.R](https://github.com/ggrajeda/spacexr/blob/4bce0a43cd084cb86a94d64e2704b1ca9d711604/R/post_processing.R).
