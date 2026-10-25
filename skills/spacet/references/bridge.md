# Export and convert

## Contents
- R export
- Python conversion
- Labels and validation

## R export

Run after QC and deconvolution, with the complete object `obj` loaded. This recipe uses public object slots; it does not rerun or replace SpaCET. Keep one export per section/bin size. Check the installed package structure before adapting an older result.

```r
library(Matrix)
library(jsonlite)

export_spacet <- function(obj, outdir, metadata,
                          x_col="coordinate_x_um", y_col="coordinate_y_um") {
  stopifnot(!dir.exists(outdir))
  counts <- obj@input$counts
  ids <- colnames(counts)
  coord <- as.data.frame(obj@input$spotCoordinates)
  md <- obj@input$metaData
  if (!is.null(md)) md <- as.data.frame(md)
  prop <- obj@results$deconvolution$propMat
  tree <- obj@results$deconvolution$Ref$lineageTree
  stopifnot(length(ids) > 0, !anyDuplicated(ids), !anyNA(ids),
            !anyDuplicated(rownames(counts)), !is.null(prop), length(tree) > 0,
            !anyDuplicated(rownames(coord)), !anyDuplicated(colnames(prop)),
            setequal(ids, rownames(coord)), setequal(ids, colnames(prop)),
            all(c(x_col, y_col) %in% colnames(coord)))
  # Join by the unchanged SpaCET IDs, never by current row order.
  coord <- coord[ids, , drop=FALSE]
  prop <- prop[, ids, drop=FALSE]
  if (!is.null(md) && "barcode" %in% names(md)) {
    stopifnot(!anyDuplicated(rownames(md)), setequal(ids, rownames(md)))
    source_id <- as.character(md[ids, "barcode"])
    source_kind <- "barcode"
  } else {
    source_id <- ids
    source_kind <- "spacet_id" # Do not claim these are original barcodes.
  }
  stopifnot(!anyNA(source_id), !anyDuplicated(source_id), all(nzchar(source_id)))
  spots <- data.frame(spot_id=ids, source_id=source_id,
                      source_id_kind=source_kind,
                      x=coord[[x_col]], y=coord[[y_col]], check.names=FALSE)
  fractions <- data.frame(spot_id=ids, t(prop), check.names=FALSE)
  lineage <- do.call(rbind, lapply(names(tree), function(parent) {
    data.frame(parent=parent, child=as.character(tree[[parent]]))
  }))
  metadata$spacet_version <- as.character(packageVersion("SpaCET"))
  metadata$selected_signature <- obj@results$deconvolution$malRes$sig
  metadata$coordinate_columns <- c(x_col, y_col)
  metadata$expression_source <- "SpaCET input counts after recorded constructor/QC processing"
  dir.create(outdir, recursive=TRUE)
  write_table <- function(x, name) write.table(
    x, file.path(outdir,name), sep="\t", quote=TRUE,
    row.names=FALSE, col.names=TRUE, na="")
  Matrix::writeMM(counts, file.path(outdir,"counts.mtx"))
  write_table(data.frame(gene_symbol=rownames(counts)), "genes.tsv")
  write_table(spots,"spots.tsv")
  write_table(fractions,"fractions.tsv")
  write_table(lineage,"lineage.tsv")
  jsonlite::write_json(metadata, file.path(outdir,"metadata.json"),
                       auto_unbox=TRUE, pretty=TRUE, null="null")
  capture.output(sessionInfo(), file=file.path(outdir,"sessionInfo.txt"))
  message("Export complete: ", outdir)
}

# EDIT these values using the actual sample record.
metadata <- list(
  sample_id="sample01", patient_id="unknown", section_id="section01",
  organism="human", platform="Visium", observation_unit="spot",
  donor_ancestry="unknown", cancer_type="SKCM",
  coordinate_units="um",
  coordinate_convention="SpaCET coordinate_x_um / coordinate_y_um; preserve native axes",
  gene_identifier="human_gene_symbol", qc_description="Record actual QC thresholds here"
)
export_spacet(obj, "sample01_spacet_export", metadata)
```

For HD bins set platform to `VisiumHD`, observation_unit to `bin`, and supply numeric `bin_size_um`. Segmented cells use `cell`. For manual/older objects without micrometre columns, explicitly select x/y columns and record real units; do not rename image pixels to micrometres. Standard Visium's `array_row/array_col` grid is staggered: use the derived physical coordinates or image pixel x/y, not raw row/column indices as Euclidean coordinates. `pixel_col` is x and `pixel_row` is y. SpaCET may flip physical y; do not apply a second transform without checking the image.

The export writes post-constructor input counts. It cannot restore duplicate gene rows discarded previously by SpaCET. Preserve original input files and record the preprocessing policy. The recipe does not export an H&E image or a Scanpy spatial-image transform.

## Python conversion

In an isolated Python environment install `anndata==0.11.4`, `pandas>=2.2,<3`, `numpy`, `scipy`, and `h5py`. Use the gsMap environment if it has compatible versions; do not downgrade an existing environment without checking it. The bridge has no Scanpy or gsMap import dependency.

```bash
python /path/to/spacet/scripts/spacet_to_gsmap.py \
  --bundle sample01_spacet_export \
  --output sample01.gsmap.h5ad
```

This preserves fractions and descriptive dominance without creating a modelling label. It writes `sample01.gsmap.audit.json`. Count columns correspond to spots.tsv row order; gene rows correspond to genes.tsv row order, as ensured by the R export. Fractions and reviewed labels may be shuffled: they are joined by `spot_id` with an exact one-to-one set match. No automatic intersection or barcode suffix removal occurs.

## Labels and validation

To construct dominant-major labels, explicitly choose all three thresholds. The following are illustrative choices, not defaults or validated biological cutoffs:

```bash
python /path/to/spacet/scripts/spacet_to_gsmap.py \
  --bundle sample01_spacet_export --output sample01.major.h5ad \
  --label-mode dominant-major \
  --min-fraction 0.5 --min-margin 0.1 --max-unidentifiable 0.3
```

Only candidates obtained from parent names in the lineage tree, plus Malignant if present, compete. Ties/all-zero candidates remain unlabeled; low dominance, small margins and large unknown fractions remain unlabeled. All original fraction columns survive. These are descriptive quality gates, not calibrated confidence probabilities. The upstream `SpaCET.calculate.mostAbundantCellType` excludes Unidentifiable and resolves ties by first reference entry; the bridge deliberately exposes ties and requires an explicit label policy.

Alternatively provide a reviewed TSV with columns `spot_id` and `annotation`, one row per exported SpaCET ID. Blank annotations remain missing; do not write a literal `NA` unless that is intentionally a class name.

```bash
python /path/to/spacet/scripts/spacet_to_gsmap.py \
  --bundle sample01_spacet_export --output sample01.reviewed.h5ad \
  --label-mode reviewed --reviewed-labels reviewed_labels.tsv
```

Review expected gsMap annotation exclusions in the audit. The bridge itself retains every input spot. Gene symbols are structurally checked, not validated against HGNC or the selected gsMap GTF; inspect overlap with the actual reference before launching. Never treat a successful h5ad write as a successful biological analysis.
