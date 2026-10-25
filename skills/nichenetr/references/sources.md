# Sources and environment

## Reviewed sources

Reviewed 2026-10-25: [saeyslab/nichenetr](https://github.com/saeyslab/nichenetr/tree/66f90d5eeafef280b2b2f339b3fd70ffec1781dd), commit `66f90d5eeafef280b2b2f339b3fd70ffec1781dd`, DESCRIPTION version `2.2.1.1`, GPL-3. This skill contains original guidance and an adapted recipe, not vendored upstream implementation.

- [README](https://github.com/saeyslab/nichenetr/blob/66f90d5eeafef280b2b2f339b3fd70ffec1781dd/README.md): scope, installation, v2 model, deprecated Differential NicheNet.
- [Seurat tutorial](https://github.com/saeyslab/nichenetr/blob/66f90d5eeafef280b2b2f339b3fd70ffec1781dd/vignettes/seurat_steps.md): candidates, background, corrected AUPR, model URLs.
- [FAQ](https://github.com/saeyslab/nichenetr/blob/66f90d5eeafef280b2b2f339b3fd70ffec1781dd/vignettes/faq.md): unsigned regulation, score interpretation, bulk inputs. Some entries describe v1; prefer current tutorial ranking defaults.
- [Prediction implementation](https://github.com/saeyslab/nichenetr/blob/66f90d5eeafef280b2b2f339b3fd70ffec1781dd/R/application_prediction.R): actual function signatures, corrected AUPR output, and top-n behavior. The Rd output list omits corrected AUPR but code and current vignette include it.
- [Original paper](https://doi.org/10.1038/s41592-019-0667-5): Browaeys, Saelens & Saeys, Nature Methods 17, 159–162 (2020), online 2019. Abstract and bibliography reviewed; full PDF and supplements not reviewed.

Further routes (not fully reviewed): [2024 protocol](https://doi.org/10.1038/s41596-024-01121-9), [MultiNicheNet](https://github.com/saeyslab/multinichenetr), [model construction](https://github.com/saeyslab/nichenetr/blob/master/vignettes/model_construction.md), [signaling paths](https://github.com/saeyslab/nichenetr/blob/master/vignettes/ligand_target_signaling_path.md). Read actual documentation before using these advanced workflows. Do not recommend deprecated Differential NicheNet by default.

## Install

Use a project R library or renv. Avoid unnecessary upgrades of shared environments. Install missing Bioconductor dependencies via BiocManager. The upstream dependency stack includes Seurat and ComplexHeatmap.

```r
if (!requireNamespace("remotes", quietly = TRUE)) install.packages("remotes")
remotes::install_github(
  "saeyslab/nichenetr@66f90d5eeafef280b2b2f339b3fd70ffec1781dd",
  upgrade = "never", build_vignettes = FALSE
)
stopifnot(requireNamespace("nichenetr", quietly = TRUE))
packageVersion("nichenetr")
sessionInfo()
```

README reports testing with R 4.3.2; DESCRIPTION's older lower R bound does not guarantee modern dependencies work on old R. No R runtime/package execution occurred at skill creation.

## Species-matched v2 priors

Use [Zenodo 7074291](https://zenodo.org/records/7074291), linked by the authors' tutorial. Download once, verify record checksums if available, and record local SHA-256. Downloads were not run during skill creation.

| Species | Ligand–receptor RDS | Ligand–target RDS | Optional weighted networks RDS |
| --- | --- | --- | --- |
| human | lr_network_human_21122021.rds | ligand_target_matrix_nsga2r_final.rds | weighted_networks_nsga2r_final.rds |
| mouse | lr_network_mouse_21122021.rds | ligand_target_matrix_nsga2r_final_mouse.rds | weighted_networks_nsga2r_final_mouse.rds |

Tutorial URLs use `https://zenodo.org/record/7074291/files/<filename>`. Weighted networks support advanced path/weighted-network visualization; they are unnecessary for basic activity scoring. Never mix v1/v2 priors or species. Package version, prior release, and publication date are distinct; current v2 analysis is not exact original-paper reproduction.
