# RCTD workflow templates

Source-reviewed against the pinned implementations in [versions.md](versions.md). These examples were not executed in R during skill creation. Adapt paths/objects, run a representative pilot in the user's installed R environment, and report actual validation before scaling. Do not claim the templates constitute a tested installation.

## Input contract and extraction

Expected objects: `ref_counts` (genes x reference cells), `sp_counts` (genes x spots), `labels` (named factor), `coords` (spot-row-named x/y data.frame). Use actual raw count assays. For Seurat, inspect `Assays`, `Layers` and installed accessors; avoid assuming the old `@assays$RNA@counts` slot works in v5. If layers are split, explicitly select/join raw layers and verify columns. Do not use default normalized `data` or SCT `scale.data`. AnnData commonly stores cells x genes: inspect the raw-count layer and transpose once, preserving names.

The following preflight is deliberately strict. It does not silently intersect barcodes or relabel cells:

```r
library(Matrix)
check_ids <- function(x, what) {
  if (is.null(x) || anyNA(x) || any(!nzchar(x)) || anyDuplicated(x))
    stop(paste('Invalid/duplicate identifiers:', what))
}
check_counts <- function(x, what) {
  if (!(is.matrix(x) || inherits(x, 'dgCMatrix')))
    stop(paste(what, 'must be a numeric matrix or dgCMatrix'))
  check_ids(rownames(x), paste(what, 'genes'))
  check_ids(colnames(x), paste(what, 'barcodes'))
  v <- if (inherits(x, 'dgCMatrix')) x@x else as.vector(x)
  if (!is.numeric(v) || any(!is.finite(v)) || any(v < 0) ||
      any(abs(v - round(v)) > 1e-6)) stop(paste('Invalid raw counts:', what))
  if (any(Matrix::colSums(x) <= 0)) stop(paste('Zero-library columns:', what))
}
check_counts(ref_counts, 'reference')
check_counts(sp_counts, 'spatial')
check_ids(names(labels), 'label barcodes')
check_ids(rownames(coords), 'coordinate barcodes')
stopifnot(setequal(names(labels), colnames(ref_counts)),
          setequal(rownames(coords), colnames(sp_counts)))
labels <- labels[colnames(ref_counts)]
stopifnot(!anyNA(labels), all(nzchar(as.character(labels))))
labels <- droplevels(factor(labels))
names(labels) <- colnames(ref_counts)
stopifnot(nlevels(labels) >= 2, !any(grepl('/', levels(labels), fixed=TRUE)))
coords <- as.data.frame(coords[colnames(sp_counts), c('x','y'), drop=FALSE])
stopifnot(all(vapply(coords, is.numeric, logical(1))),
          all(is.finite(as.matrix(coords))))

# Capture full-library denominators before any deliberate gene restriction.
ref_nUMI <- Matrix::colSums(ref_counts)
sp_nUMI <- Matrix::colSums(sp_counts)
common <- intersect(rownames(ref_counts), rownames(sp_counts))
print(c(reference_genes=nrow(ref_counts), spatial_genes=nrow(sp_counts),
        common_genes=length(common)))
if (length(common) == 0) stop('Resolve gene identifiers before fitting')
print(table(labels))
# Normally leave gene filtering to RCTD. If restricting to common features is
# justified, keep ref_nUMI/sp_nUMI above and document the restriction.
```

For a deliberate linear-scale reference exception, replace the integer requirement only for the reference and review the normalization/total semantics first. Do not turn it off for unexplained noninteger spatial values.

## Original dmcable implementation

```r
library(spacexr)
stopifnot(all(c('create.RCTD','run.RCTD','Reference','SpatialRNA') %in%
              getNamespaceExports('spacexr')))
set.seed(20261031)
reference <- Reference(ref_counts, labels, ref_nUMI)
puck <- SpatialRNA(coords, sp_counts, sp_nUMI)
# One core is an intentional pilot choice, not a scientific default.
fit <- create.RCTD(puck, reference, max_cores=1)
print(table(reference@cell_types))
print(c(input=ncol(sp_counts), retained=ncol(fit@spatialRNA@counts)))
print(lengths(fit@internal_vars[c('gene_list_bulk','gene_list_reg')]))
print(sum(fit@spatialRNA@nUMI > fit@config$UMI_min_sigma))
saveRDS(fit, 'rctd_prepared.rds')
# Conventional Visium example; choose a mode using the actual measurement unit.
fit <- run.RCTD(fit, doublet_mode='full')
saveRDS(fit, 'rctd_fitted.rds')
saveRDS(list(config=fit@config, package=packageDescription('spacexr'),
             seed=20261031, session=sessionInfo()), 'rctd_provenance.rds')
writeLines(fit@internal_vars$gene_list_bulk, 'bulk_genes.txt')
writeLines(fit@internal_vars$gene_list_reg, 'regression_genes.txt')
writeLines(colnames(sp_counts), 'expected_barcodes.txt')
writeLines(setdiff(colnames(sp_counts), colnames(fit@spatialRNA@counts)),
           'excluded_barcodes.txt')
```

Use a new output directory or explicit run identifier; do not overwrite an existing fit silently. The templates show basenames for clarity.

Full result export:

```r
w <- fit@results$weights
stopifnot(identical(rownames(w), colnames(fit@spatialRNA@counts)),
          all(is.finite(w)), all(w >= 0), all(rowSums(w) > 0))
write.csv(as.matrix(w), 'weights_raw.csv') # spots x types, generally small K
wf <- normalize_weights(w)
stopifnot(all(abs(rowSums(wf)-1) < 1e-6))
write.csv(as.matrix(wf), 'rna_fractions.csv')
```

The dense export is of the spots-by-types result only, not the original gene-by-spot matrix; estimate memory/file size first for huge data.

Doublet result export after choosing `doublet_mode='doublet'`:

```r
stopifnot(identical(rownames(fit@results$results_df),
                    rownames(fit@results$weights_doublet)))
write.csv(fit@results$results_df, 'classifications.csv')
write.csv(as.matrix(fit@results$weights_doublet), 'pair_weights.csv')
write.csv(as.matrix(fit@results$weights), 'preliminary_full_weights.csv')
```

Use the bundled Python auditor on these legacy exports. Full example:

```bash
python /path/to/rctd/scripts/audit_rctd_results.py --mode full \
  --weights weights_raw.csv --expected-barcodes expected_barcodes.txt \
  --outdir audit_full
```

Doublet example:

```bash
python /path/to/rctd/scripts/audit_rctd_results.py --mode doublet \
  --weights pair_weights.csv --classifications classifications.csv \
  --expected-barcodes expected_barcodes.txt --outdir audit_doublet
```

The auditor preserves filtered-out barcodes as exclusions, does not reassign them, and writes NA compositions for uncertain, rejected or nonconverged calls. Confidence of the first identity remains separately available. It refuses overwriting an existing output directory.

Multi mode export requires a different path:

```r
stopifnot(length(fit@results) == ncol(fit@spatialRNA@counts))
barcodes <- colnames(fit@spatialRNA@counts)
multi_long <- do.call(rbind, lapply(seq_along(fit@results), function(i) {
  z <- fit@results[[i]]
  types <- z$cell_type_list
  stopifnot(length(types) == length(z$sub_weights),
            all(types %in% names(z$sub_weights)),
            all(types %in% names(z$conf_list)))
  data.frame(barcode=barcodes[i], cell_type=types,
             rna_fraction=as.numeric(z$sub_weights[types]),
             confident=as.logical(z$conf_list[types]),
             conv_all=z$conv_all, conv_sub=z$conv_sub)
}))
write.csv(multi_long, 'multi_results_long.csv', row.names=FALSE)
```

Do not run this extractor on a full/doublet fit. Verify object structure in the installed version before use.

## Bioconductor adaptation

```r
library(spacexr)
library(SummarizedExperiment)
library(SpatialExperiment)
stopifnot(all(c('createRctd','runRctd') %in% getNamespaceExports('spacexr')))
reference_se <- SummarizedExperiment(
  assays=list(counts=ref_counts),
  colData=S4Vectors::DataFrame(cell_type=labels, nUMI=ref_nUMI,
                              row.names=colnames(ref_counts)))
spatial_spe <- SpatialExperiment(
  assays=list(counts=sp_counts),
  colData=S4Vectors::DataFrame(nUMI=sp_nUMI, row.names=colnames(sp_counts)),
  spatialCoords=as.matrix(coords))
set.seed(20261031)
rctd_data <- createRctd(spatial_spe, reference_se, cell_type_col='cell_type')
result <- runRctd(rctd_data, rctd_mode='full', max_cores=1)
saveRDS(result, 'rctd_bioc_result.rds')
assayNames(result)
dim(assay(result,'weights')) # types x spots
colnames(colData(result))
```

Inspect assay-specific confidence semantics and excluded columns. Preserve result objects; do not feed a transposed confidence-filtered assay to the legacy full auditor and assume equivalent interpretation.

## Pilot acceptance

Inspect retained/input counts; counts per reference type; shared/selected genes; sigma eligibility; fit warnings; nonfinite or negative outputs; sum-to-one only on the proper normalized result; class/confidence at the appropriate resolution; marker/histology agreement; depth-related rejection; and mode/reference sensitivity. Then increase scale and allocated cores deliberately. Scientific acceptance cannot be reduced to an exit code.
