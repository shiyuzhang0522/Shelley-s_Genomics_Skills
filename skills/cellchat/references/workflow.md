# Core workflow

## Contents

1. Environment and inputs
2. Source-checked v2 recipe
3. Optional analysis and reproducibility

## Environment and inputs

Use a project-specific R library/renv. Inspect existing versions before installing. Do not downgrade shared igraph/R or reinstall XQuartz merely because an old issue suggests it. The pinned package depends on R>=3.6 but modern dependencies may require newer R. Install Bioconductor packages through BiocManager. Example:

```r
if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
BiocManager::install(c("ComplexHeatmap", "BiocNeighbors", "BiocGenerics"),
                    ask = FALSE, update = FALSE)
if (!requireNamespace("remotes", quietly = TRUE)) install.packages("remotes")
remotes::install_github(
  "jinworks/CellChat@75253cd0c9e68410e6e721a6d3a0419a1d7e358f",
  upgrade = "never", build_vignettes = FALSE
)
packageVersion("CellChat")
formals(CellChat::identifyOverExpressedInteractions)
```

NMF/circlize and the compiler stack are package dependencies; Python umap-learn is relevant to the optional embedding backend, not the LR scoring model itself. Use `do.fast=FALSE` when choosing the supported non-presto backend; don't switch backends silently between conditions.

### Prepare expression and metadata

- **Seurat:** inspect `Layers(object[["RNA"]])` for v5. Resolve split layers deliberately on a working copy if required, then extract the intended normalized RNA data matrix. Old `@data` recipes and blindly selecting the first layer can omit cells. Require row/column identifiers. Check that the chosen assay is measured expression, not integrated/scaled residuals.
- **SCE:** use a verified normalized nonnegative assay (`logcounts` by default). Record log base and normalization.
- **AnnData:** determine what X/layers/raw actually contain before conversion. Transpose cells × genes into genes × cells once; preserve sparsity. Do not assume X contains counts or normalize an already normalized layer.
- **Raw counts:** normalize once, for example library-size scaling followed by log1p; use a justified scale factor consistently. CellChat expects normalized values. `normalizeData` is provided upstream; confirm its arguments in the installed version.
- Use the full relevant measured gene universe, not only HVGs or DE genes, so required ligand/receptor subunits are retained. Audit symbols and duplicate mappings. Do not use capitalization as ortholog mapping.

Prepare `expr` (genes × cells), `meta` with row names=barcodes and columns `celltype`, `samples`, donor/condition information. Preserve donors separately from sections. The helper `scripts/check_inputs.R` checks technical integrity and alignment, not biological suitability. For spatial data supply coordinates and per-sample calibration as described in spatial.md.

If using a custom sample_col, the helper also copies it to the upstream-required `samples` field and rejects conflicting existing samples. Explicit factor level order is preserved. Inspect the returned sample-by-group table per section before analysis; pooled counts can hide inadequate groups within individual sections.

## Source-checked v2 recipe

Set `skill_dir` to the installed skill path when generating the user's script. This example chooses the current stricter both-endpoint candidate rule and a slow DE backend explicitly; use FALSE for the older either-endpoint candidate rule only with a documented choice. Core numerical behavior is smoke-tested with synthetic data; this complete installed-package recipe still requires a pilot in the user's environment.

```r
library(CellChat)
source(file.path(skill_dir, "scripts", "check_inputs.R"))
x <- check_cellchat_inputs(expr, meta, group_col = "celltype", sample_col = "samples",
                          normalization = "library-size normalized and log1p", min_cells = 10L)
# Replace the declaration above with the true normalization provenance.
out_dir <- "cellchat_results" # choose a new directory
if (dir.exists(out_dir)) stop("Choose a new output directory to preserve previous results")
dir.create(out_dir, recursive = TRUE)
future::plan("sequential") # start reproducibly; increase workers after memory assessment
message("[1/5] Constructing object and selecting database")
cc <- CellChat::createCellChat(x$expression, meta = x$metadata, group.by = "celltype")
db <- CellChatDB.human # use CellChatDB.mouse for mouse; do not mix species
db.use <- CellChat::subsetDB(db, non_protein = FALSE)
# Alternative explicit scope: subsetDB(db, search="Secreted Signaling", key="annotation")
cc@DB <- db.use
cc <- CellChat::subsetData(cc)
if (!nrow(cc@data.signaling) || max(cc@data.signaling) <= 0) stop("No usable signaling expression")
message("[2/5] Selecting candidate genes and interactions")
cc <- CellChat::identifyOverExpressedGenes(cc, do.fast = FALSE,
                                         thresh.pc = 0, thresh.fc = 0, thresh.p = 0.05)
cc <- CellChat::identifyOverExpressedInteractions(cc, variable.both = TRUE)
if (!nrow(cc@LR$LRsig)) stop("No candidate LR pairs: inspect symbol/DB coverage and thresholds")
message("[3/5] Scoring candidate interactions")
cc <- CellChat::computeCommunProb(cc, type = "triMean", raw.use = TRUE,
                                 population.size = FALSE, nboot = 1000, seed.use = 1L)
cc.prefilter <- cc
saveRDS(cc.prefilter, file.path(out_dir, "cellchat_prefilter.rds"))
cc <- CellChat::filterCommunication(cc, min.cells = 10, min.samples = 1)
message("[4/5] Summarizing networks")
cc <- CellChat::aggregateNet(cc, thresh = 0.05)
has.lr <- any(cc@net$prob > 0 & cc@net$pval < 0.05)
# subsetCommunication throws on empty results in this version; guard before calling.
lr.table <- if (has.lr) CellChat::subsetCommunication(cc, thresh = 0.05) else
  data.frame(source=character(), target=character(), interaction_name=character(),
             prob=numeric(), pval=numeric(), pathway_name=character(),
             ligand=character(), receptor=character())
if (!nrow(lr.table)) {
  warning("No retained interactions: save QC and do not force network plots")
} else if (length(unique(cc@LR$LRsig$pathway_name)) >= 2L) {
  cc <- CellChat::computeCommunProbPathway(cc, thresh = 0.05)
  # Check dimensions before pathway-specific consumers; singleton outputs can drop dimensions.
  if (length(dim(cc@netP$prob)) == 3L && length(cc@netP$pathways)) {
    cc <- CellChat::netAnalysis_computeCentrality(cc, slot.name = "netP")
  } else warning("Inspect singleton/empty pathway output before pathway analysis")
} else warning("Single candidate pathway: retain LR results and handle the version-specific pathway edge case separately")
message("[5/5] Saving inference and provenance")
saveRDS(cc.prefilter, file.path(out_dir, "cellchat_prefilter.rds"))
saveRDS(cc, file.path(out_dir, "cellchat.rds"))
saveRDS(db.use, file.path(out_dir, "CellChatDB_used.rds"))
saveRDS(x$audit, file.path(out_dir, "input_audit.rds"))
write.table(lr.table, file.path(out_dir, "ligand_receptor.tsv"), sep = "\t",
            row.names = FALSE, quote = FALSE)
writeLines(capture.output(sessionInfo()), file.path(out_dir, "sessionInfo.txt"))
```

The example's 1000 permutations is a computational choice for finer Monte Carlo resolution, not a guarantee of valid biological inference. A pilot can use fewer permutations, clearly labeled. Report exact thresholds, candidate rule and DE backend. For comparisons, decide the candidate universe and keep settings comparable rather than changing thresholds after seeing desired results.

Export full raw `net$prob`/`net$pval` (retained in RDS), pathway table when dimensionally valid, aggregate matrices, tested LR list, and gene/subunit coverage. Interpret any independently applied multiplicity correction explicitly; do not silently label native p-values as q-values.

## Optional analysis and reproducibility

For shallow coverage, inspect dropout/subunits before considering `smoothData(cc, adj=PPI.human)` (or PPI.mouse). Then use `raw.use=FALSE`; current code reads `data.smooth`. Smoothing is optional and changes predictions. Older tutorials may use `projectData`/`data.project`; do not use positional arguments to the current smoothing function.

Save normalization, species/DB selection, model/package commit, candidate rule, summary type/trim, smoothing, population weighting, permutation seed/count, thresholds, spatial settings and donor/sample structure. Not all parameters (e.g. scale.distance in the reviewed snapshot) are reliably preserved in `@options$parameter`; save your own parameter list. Record input and used-DB SHA-256 or another clearly identified checksum and maintain a project environment lockfile.

`population.size=FALSE` removes explicit abundance weighting, but does not remove all consequences of unequal sampling, estimation uncertainty or dropout. Downsampling can support sensitivity analysis; preserve rare groups/sample structure and document the selection seed. Estimate memory: scoring densifies the signaling matrix, and bootstrap group summaries grow with nboot. Avoid unrestricted parallel workers for large HD data.
