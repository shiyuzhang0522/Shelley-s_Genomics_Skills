# Validate and align CellChat inputs without changing expression values.
# source() this file, then call check_cellchat_inputs().
check_cellchat_inputs <- function(expression, metadata, group_col = "celltype",
                                 sample_col = "samples", normalization,
                                 coordinates = NULL, spatial_factors = NULL,
                                 min_cells = 10L) {
  fail <- function(...) stop(..., call. = FALSE)
  if (missing(normalization) || length(normalization) != 1L ||
      is.na(normalization) || !nzchar(normalization)) {
    fail("Declare the normalization procedure; it cannot be inferred from values")
  }
  if (!is.matrix(expression) && !inherits(expression, "dgCMatrix")) {
    fail("Use a numeric genes-by-cells matrix or dgCMatrix")
  }
  vals <- if (inherits(expression, "dgCMatrix")) expression@x else as.vector(expression)
  if (!is.numeric(vals) || any(!is.finite(vals)) || any(vals < 0)) {
    fail("Expression must be finite and nonnegative; reject residuals and scaled assays")
  }
  if (nrow(expression) < 2L || ncol(expression) < 2L || !any(vals > 0)) {
    fail("Expression is empty, all zero, or too small")
  }
  valid_names <- function(x) !is.null(x) && !anyNA(x) &&
    all(nzchar(x)) && !anyDuplicated(x)
  if (!valid_names(rownames(expression)) || !valid_names(colnames(expression))) {
    fail("Require unique nonempty gene symbols and cell barcodes")
  }
  if (!is.data.frame(metadata) || !valid_names(rownames(metadata))) {
    fail("Metadata must have unique cell barcodes as row names")
  }
  ids <- colnames(expression)
  if (!setequal(ids, rownames(metadata))) fail("Expression and metadata barcode sets differ")
  reordered <- !identical(ids, rownames(metadata))
  metadata <- metadata[match(ids, rownames(metadata)), , drop = FALSE]
  if (!identical(ids, rownames(metadata))) fail("Metadata alignment failed")
  if (!all(c(group_col, sample_col) %in% colnames(metadata))) {
    fail("Metadata requires the specified cell-group and sample columns")
  }
  if (identical(group_col, sample_col) || identical(group_col, "samples")) {
    fail("Cell-group and sample columns must be distinct; samples is reserved for sample IDs")
  }
  if (!identical(sample_col, "samples") && "samples" %in% names(metadata) &&
      !identical(as.character(metadata$samples), as.character(metadata[[sample_col]]))) {
    fail("The selected sample column conflicts with metadata$samples")
  }
  for (key in c(group_col, sample_col)) {
    v <- as.character(metadata[[key]])
    if (anyNA(v) || any(!nzchar(trimws(v)))) fail("Missing labels in ", key)
    metadata[[key]] <- if (is.factor(metadata[[key]])) droplevels(metadata[[key]]) else factor(v)
  }
  # The upstream constructor/model specifically reads metadata$samples.
  metadata$samples <- metadata[[sample_col]]
  if ("0" %in% levels(metadata[[group_col]])) fail("Rename the unsupported cell-group label '0'")
  if (nlevels(metadata[[group_col]]) < 2L) fail("Require at least two represented cell groups")
  if (length(min_cells) != 1L || !is.finite(min_cells) ||
      min_cells < 0 || min_cells != as.integer(min_cells)) fail("min_cells must be a nonnegative integer")
  sizes <- table(metadata[[group_col]])
  removed <- names(sizes)[sizes <= min_cells]
  if (length(removed)) warning("Pinned filterCommunication excludes groups with <= min_cells: ",
                               paste(removed, collapse = ", "), call. = FALSE)
  if (all(vals == floor(vals))) warning("All stored expression values are integers: verify normalized input", call. = FALSE)
  spatial <- !is.null(coordinates)
  if (!spatial && !is.null(spatial_factors)) fail("Spatial factors supplied without coordinates")
  if (spatial) {
    if (!is.matrix(coordinates) || !is.numeric(coordinates) || ncol(coordinates) != 2L ||
        any(!is.finite(coordinates)) || !valid_names(rownames(coordinates))) {
      fail("Coordinates must be a finite numeric two-column matrix with unique barcodes")
    }
    if (!setequal(ids, rownames(coordinates))) fail("Coordinate and expression barcode sets differ")
    coordinates <- coordinates[match(ids, rownames(coordinates)), , drop = FALSE]
    samples <- levels(metadata[[sample_col]])
    if (!is.data.frame(spatial_factors) || !valid_names(rownames(spatial_factors)) ||
        !setequal(samples, rownames(spatial_factors)) ||
        !all(c("ratio", "tol") %in% names(spatial_factors))) {
      fail("Provide one named spatial-factor row per sample with ratio and tol columns")
    }
    spatial_factors <- spatial_factors[match(samples, rownames(spatial_factors)), , drop = FALSE]
    if (!is.numeric(spatial_factors$ratio) || !is.numeric(spatial_factors$tol) ||
        any(!is.finite(spatial_factors$ratio)) || any(!is.finite(spatial_factors$tol)) ||
        any(spatial_factors$ratio <= 0) || any(spatial_factors$tol < 0)) {
      fail("ratio must be finite positive microns per input unit; tol must be finite nonnegative microns")
    }
    xy <- data.frame(sample = metadata[[sample_col]], coordinates)
    if (anyDuplicated(xy)) warning("Duplicate coordinates within a sample: inspect rounding/segmentation", call. = FALSE)
  }
  list(expression = expression, metadata = metadata, coordinates = coordinates,
       spatial_factors = spatial_factors,
       audit = list(normalization = normalization, metadata_reordered = reordered,
                    group_column = group_col, source_sample_column = sample_col,
                    n_genes = nrow(expression), n_cells = ncol(expression),
                    group_sizes = sizes, sample_by_group = table(metadata[[sample_col]], metadata[[group_col]]),
                    groups_excluded_by_pinned_filter = removed,
                    min_cells = min_cells, spatial = spatial))
}
