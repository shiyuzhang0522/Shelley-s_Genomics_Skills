# Workflow and R recipe

## Prepare input lists

Prefer explicit steps to the all-in-one Seurat wrapper. Inspect actual assay/layer names and metadata first. For a Seurat v5 object, check RNA layers and their normalization; join appropriate split layers only on a working copy when required. Use RNA detection rather than integrated/scaled residuals. Set cell-type identities deliberately before calling `get_expressed_genes()`.

The reviewed tutorial calls `get_expressed_genes(receiver, seuratObj, pct = 0.05)` and applies it to each sender type separately, then takes their union. A 5% threshold is an example, not universally optimal. For sorted bulk, define expression using a suitable bulk filtering rule rather than a single-cell detection fraction.

Prepare four UTF-8, one-symbol-per-line text files, with no header:

- `receiver_expressed.txt`: expressed receiver genes.
- `receiver_tested.txt`: eligible receiver genes actually assessed in the contrast/program design, including nonsignificant genes. For an external program, define an appropriate measured eligibility universe.
- `program.txt`: selected receiver response/program genes.
- `sender_expressed.txt`: union of expressed genes across chosen sender types. Retain per-type lists separately for attribution.

Also save a design record separately as text/JSON; it is not read as a gene list. Record species, contrast, donor structure, detection and selection rules, and all original counts.

Supply matched `ligand_target_matrix.rds` and `lr_network.rds`. File renaming is optional: change paths explicitly. Do not transpose an unverified matrix until row/column identities establish orientation. Do not use only significant genes as the tested universe.

## Adaptable R recipe

This recipe runs both modes. For an explicitly sender-agnostic-only task, omit the sender input and focused branch; do not invent sender populations. This is a source-checked recipe, not an executed benchmark. Edit `input_dir` and a new `out_dir`, verify the above inputs, and run on a small example first. Installation and model downloads are in sources.md. This recipe assumes the v2 model and current API.

```r
stopifnot(requireNamespace("nichenetr", quietly = TRUE))
input_dir <- "nichenet_inputs"
out_dir <- "nichenet_results"
if (dir.exists(out_dir)) stop("Choose a new output directory to preserve prior results")
read_genes <- function(filename) {
  x <- trimws(readLines(file.path(input_dir, filename), warn = FALSE))
  x <- x[nzchar(x)]
  if (!length(x)) stop("Empty gene file: ", filename)
  if (any(grepl("[[:space:]]", x))) stop("Expected one symbol per line: ", filename)
  if (anyDuplicated(x)) warning("Deduplicating repeated symbols in ", filename)
  unique(x)
}
message("[1/5] Reading input gene sets and species-matched priors")
receiver <- read_genes("receiver_expressed.txt")
tested <- read_genes("receiver_tested.txt")
program_raw <- read_genes("program.txt")
sender <- read_genes("sender_expressed.txt")
lt <- readRDS(file.path(input_dir, "ligand_target_matrix.rds"))
lr <- as.data.frame(readRDS(file.path(input_dir, "lr_network.rds")))
if (!is.matrix(lt) || !is.numeric(lt)) stop("Expected a numeric target-by-ligand matrix")
valid_names <- function(x) {
  !is.null(x) && length(x) > 0L && !anyNA(x) && all(nzchar(x)) && !anyDuplicated(x)
}
if (!valid_names(rownames(lt)) || !valid_names(colnames(lt))) stop("Invalid prior dimnames")
if (!all(c("from", "to") %in% names(lr))) stop("LR network needs from/to columns")
lr <- unique(lr[, c("from", "to"), drop = FALSE])
lr$from <- as.character(lr$from)
lr$to <- as.character(lr$to)
if (anyNA(lr) || any(!nzchar(lr$from)) || any(!nzchar(lr$to))) stop("Invalid LR symbols")

message("[2/5] Defining the eligible universe and candidate ligands")
background <- Reduce(intersect, list(receiver, tested, rownames(lt)))
program <- intersect(program_raw, background)
if (!length(program) || length(program) >= length(background)) {
  stop("Need a nonempty program and background with both program and nonprogram genes")
}
if (length(background) < 5000L) warning("Small receiver universe: inspect coverage and eligibility")
if (length(program) / length(background) > 0.5) warning("Program occupies over half the universe")
expressed_receptors <- intersect(receiver, lr$to)
agnostic <- intersect(unique(lr$from[lr$to %in% expressed_receptors]), colnames(lt))
focused <- intersect(agnostic, sender)
if (!length(agnostic) || !length(focused)) stop("Empty candidates: inspect species, symbols and expression")
if (any(!is.finite(lt[, agnostic, drop = FALSE]))) stop("Nonfinite prior scores")
if (any(lt[, agnostic, drop = FALSE] < 0)) stop("Unexpected negative prior scores")

message("[3/5] Scoring both ligand sets against the same receiver program")
score <- function(candidates) {
  a <- as.data.frame(nichenetr::predict_ligand_activities(
    geneset = program, background_expressed_genes = background,
    ligand_target_matrix = lt, potential_ligands = candidates, single = TRUE
  ))
  required <- c("test_ligand", "auroc", "aupr", "aupr_corrected", "pearson")
  if (!all(required %in% names(a))) stop("Resolve package/model version: missing score columns")
  if (anyNA(a$test_ligand) || anyDuplicated(a$test_ligand) ||
      !setequal(as.character(a$test_ligand), candidates)) stop("Returned ligand identities differ from inputs")
  if (any(!is.finite(a$aupr_corrected))) stop("Undefined ligand activity; inspect constant/degenerate predictions")
  a <- a[order(-a$aupr_corrected, a$test_ligand), , drop = FALSE]
  a$rank <- rank(-a$aupr_corrected, ties.method = "min")
  a
}
activities <- list(agnostic = score(agnostic), focused = score(focused))

message("[4/5] Extracting links; top-k is a display choice, not significance")
top_k <- 20L
top_n_targets <- 250L
links <- lapply(activities, function(a) {
  top <- head(a$test_ligand, top_k)
  x <- do.call(rbind, lapply(top, function(ligand) {
    as.data.frame(nichenetr::get_weighted_ligand_target_links(
      ligand = ligand, geneset = program, ligand_target_matrix = lt, n = top_n_targets
    ))
  }))
  x[!is.na(x$target) & is.finite(x$weight) & x$weight > 0, , drop = FALSE]
})

message("[5/5] Saving tables and reproducibility information")
dir.create(out_dir, recursive = TRUE)
write_tsv <- function(x, file) write.table(x, file.path(out_dir, file), sep = "\t",
                                         row.names = FALSE, quote = FALSE, na = "NA")
for (mode in names(activities)) {
  write_tsv(activities[[mode]], paste0("ligand_activities_", mode, ".tsv"))
  write_tsv(links[[mode]], paste0("ligand_target_links_", mode, ".tsv"))
}
lr_candidates <- lr[lr$from %in% focused & lr$to %in% expressed_receptors, , drop = FALSE]
write_tsv(lr_candidates, "focused_ligand_receptor_candidates.tsv")
write_tsv(data.frame(gene = program_raw,
                    expressed_receiver = program_raw %in% receiver,
                    eligible_tested = program_raw %in% tested,
                    prior_covered = program_raw %in% rownames(lt),
                    retained = program_raw %in% program), "program_coverage.tsv")
write_tsv(data.frame(metric = c("receiver_expressed", "receiver_tested", "program_input", "program_retained", "background", "agnostic", "focused"),
                    n = c(length(receiver), length(tested), length(program_raw), length(program), length(background), length(agnostic), length(focused))),
          "qc_counts.tsv")
saveRDS(list(background = background, program = program, agnostic = agnostic, focused = focused,
             top_k = top_k, top_n_targets = top_n_targets), file.path(out_dir, "analysis_parameters.rds"))
input_files <- file.path(input_dir, c("receiver_expressed.txt", "receiver_tested.txt", "program.txt",
                                    "sender_expressed.txt", "ligand_target_matrix.rds", "lr_network.rds"))
write_tsv(data.frame(file = input_files, md5 = unname(tools::md5sum(input_files))), "input_md5.tsv")
writeLines(capture.output(sessionInfo()), file.path(out_dir, "sessionInfo.txt"))
message("Finished: ", normalizePath(out_dir))
```

Also save the design record, prior download URLs and source-provided checksums, and input SHA-256 when available. Attach per-sender ligand detection/abundance to the LR table before assigning sender labels. The supplied table contains candidate edges, not significant edges. An empty filtered target-link table is a valid result to investigate, not permission to invent links.

## Troubleshoot and inspect

| Symptom | Check |
| --- | --- |
| Very low prior overlap | Species, Ensembl versus symbols, aliases, duplicate handling, matrix orientation |
| No focused ligands | Receiver receptors, sender detection, intended sender scope, prior coverage |
| Weak/negative activities | Program/background definition, coverage, prior limitations; do not infer repression |
| Many tied or zero links | Top-n cutoff and zero weights; retain raw scores and label weak evidence |
| Receptor heatmap differs from expression | Prior LR confidence and measured expression are different quantities |
| Different results between tutorials | Package version, prior version, background, sender scope, ranking metric |

Inspect ligand activity bars, ligand-target heatmaps, and separate sender/receptor expression plots. Report top-k and target-n explicitly. For replicated designs evaluate stability across donors and consider the current MultiNicheNet workflow; do not invent between-condition significance from differences in NicheNet rank.
