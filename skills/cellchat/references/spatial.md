# Spatial and multiomics workflows

## Scope and data unit

Pinned CellChat v2 infers group-to-group communication informed by spatial proximity; it does not directly infer a graph of individual cell pairs. The current README's v3 SpatialCellChat link belongs to another repository/API. Use `createCellChat(..., datatype="spatial")` for this skill, not the FAQ's newer `createSpatialCellChat` constructor.

Establish whether observations are segmented cells, bins, or mixed spots. CellChat does not perform annotation, malignant-cell calling, segmentation, or deconvolution. A most-likely cell-type label does not purify a mixed Visium spot. SpaCET fractions describe composition, not cell-specific expression. Use an appropriate reference/deconvolution strategy or clearly describe spot-level exploratory results. gsMap scores can annotate hypotheses but are not expression input or proof of ligand-mediated causality.

## Calibrate actual coordinate files

Require two finite numeric columns, barcode-aligned with expression and metadata. Record their units and the export/software version. `ratio` means micrometers per input-coordinate unit. `tol`, `interaction.range`, and `contact.range` are in micrometers. `scale.distance` is a separate numeric distance-weighting scale; it is not pixel conversion.

Do not blindly copy the FAQ's `ratio=1` for Visium HD: Space Ranger `pxl_row_in_fullres`/`pxl_col_in_fullres` are pixels. Verify any converted centroid export separately. Official [Space Ranger spatial outputs](https://www.10xgenomics.com/support/software/space-ranger/latest/analysis/spatial-outputs) explain calibration fields and recommend calibrated microscope pixel dimensions. `spot_diameter_fullres` is a visualization estimate for traditional Visium; its 65 µm example should not automatically be replaced by a 55 µm physical capture diameter. For HD, the documented field refers to the 2 µm square side. Check actual bin size/export meaning, avoid double conversion, and validate plausible neighbor spacing. Do not apply traditional Visium spot spacing to segmented HD cells.

Choose tolerance/contact ranges from the measurement unit and biology, then assess sensitivity. A default 10 µm cell size is not appropriate for all cell types or unsegmented bins. Xenium/CosMx/Slide-seq/Stereo-seq exports also require format-specific unit checks; historical issue examples are not universal constants.

## Spatial model and parameters

For each group pair within each sample, current code finds nearest target observations, summarizes distances with a 10% trimmed mean, and requires at least `k.min` distinct nearby target indices. It does not count all possible close pairs. Group-distance summaries are symmetrized; LR direction still comes from expression.

| Parameter | Meaning |
| --- | --- |
| ratio | Physical coordinate conversion, per sample |
| tol | Tolerance added to distance cutoffs |
| interaction.range | Maximum modeled diffusible range |
| contact.range | Contact/juxtacrine center-distance restriction |
| scale.distance | Scale used before inverse-distance weighting |
| k.min | Nearby-neighbor support requirement for group adjacency |
| min.cells | Cell-group count filter; current code removes counts <= value |
| min.samples | Across-sample positive LR-expression consistency filter |

`distance.use=TRUE` multiplies by inverse scaled distance. `FALSE` retains spatial feasibility filtering but removes this inverse-distance weighting; it is not nonspatial analysis. Choose a common scale.distance for compared objects; inspect finite off-diagonal scaled distances, with source guidance aiming for minimum around 1–2. Diagnose units, empty spatial links and duplicated coordinates before adjusting a scale.

Current implementation treats secreted, ECM–receptor and nonprotein categories as diffusible; Cell-Cell Contact is contact-filtered by default. Some older text describes ECM differently. `contact.dependent.forced=TRUE` applies contact restriction to all categories and changes the model. Supply a justified contact.range when contact.dependent=TRUE. For secreted-only inference explicitly set contact.dependent=FALSE; the helper's range check runs before category routing.

Prefer distance-based contact thresholds for the baseline. The reviewed `contact.knn.k` branch has a source-inspected local-index concern; test a small known layout before relying on it rather than silently patching it. Also, outer `computeCommunProb(do.symmetric=...)` does not forward this argument to the helper at this snapshot; do not assume changing it alters behavior.

## One or multiple spatial samples

Run the same preflight as core analysis, adding coordinates and spatial factors. Distinct sections/FOVs need distinct `samples` even when coordinates overlap. Keep donor IDs separately. For a factor samples with levels `s1`, `s2`, create a data.frame with row names exactly those samples and columns ratio/tol; the validator reorders to sample-factor order. Merely naming rows is insufficient in the raw upstream call, which uses vectors in row order.

```r
x <- check_cellchat_inputs(expr, meta, normalization = normalization_description,
                          coordinates = coords, spatial_factors = spatial_factors)
cc <- CellChat::createCellChat(x$expression, meta=x$metadata, group.by="celltype",
                              datatype="spatial", coordinates=x$coordinates,
                              spatial.factors=x$spatial_factors)
# Choose DB, subsetData, gene and interaction selection as in workflow.md.
cc <- CellChat::computeCommunProb(cc, type="triMean", raw.use=TRUE,
  population.size=FALSE, distance.use=TRUE,
  interaction.range=range_um, scale.distance=shared_distance_scale,
  k.min=nearby_support, contact.dependent=TRUE, contact.range=contact_um,
  nboot=permutations, seed.use=1L)
cc.prefilter <- cc
cc <- CellChat::filterCommunication(cc, min.cells=min_group_cells,
                                    min.samples=expression_support_samples,
                                    rare.keep=FALSE)
```

All named variables above require explicit justified values, not universal constants. For secreted-only scope use contact.dependent=FALSE and omit contact.range. Keep inference and plotting checks from the core workflow.

Pooling same-condition samples is distinct from comparing conditions. Pooled spatial adjacency can be supported by only one sample; it is not automatically replicated. `min.samples` checks positive LR-expression products and group-size support, not each sample's spatial adjacency or permutation significance. `rare.keep=TRUE` can override exclusions. Retain per-donor/per-section support tables or independent analyses for reproducibility; pooled cell permutations are not donor-level tests.

There is also a source-inspected conditional-mask limitation: when support counts contain only zero or values >= min.samples, the current filter can leave zero-support edges unmasked. Treat min.samples as requiring an explicit per-edge support audit, not as a guaranteed replicate-support cutoff. This branch has not been validated on a full spatial dataset.

Multi-sample pooling must harmonize genes and annotations without discarding new cell types through first-sample factor levels. Use unique barcodes, then verify metadata/coordinates/sample factors. For between-condition comparisons infer separate objects; `mergeCellChat` merges inferred objects, not registered physical tissue. Use `sample.use` for spatial plots.

For millions of HD bins, do not materialize full all-pairs distances with `computeCellDistance` merely for QC. Use a representative, justified neighbor diagnostic and estimate memory. Scoring itself densifies signaling expression. Separate sections and rare groups must survive any resource-driven subsampling.

## RNA plus ADT

The tutorial's `preProcMultiomics` handles RNA/protein co-profiling, not arbitrary ATAC/metabolite integration. It expects RNA first, ADT second, rescales modalities, filters low relative protein values, and maps antibody names via DB geneInfo. Validate identical cell columns/order, nonnegative finite data, nonzero maxima, nonconstant ADT rows, antibody mapping, duplicates, and complex coverage before calling it.

Use both returned mixed expression and returned database; do not pair the mixed matrix with an unrelated unmodified DB. A constant ADT row causes a zero denominator in min–max scaling and must be diagnosed explicitly. Nonprotein DB signaling usually uses expression proxies for enzymes/mediators, not direct metabolite abundance. Tutorial author-local example paths are not downloadable data guarantees.
