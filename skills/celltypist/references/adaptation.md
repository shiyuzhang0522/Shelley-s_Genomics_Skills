# Adapt CellTypist to melanoma and Visium HD

These are analytical recommendations, not claims that the 2022 immune-atlas paper validated melanoma or Visium HD.

## Choose the unit and scope

| Input | Interpretation | Additional checks |
|---|---|---|
| Dissociated scRNA-seq cell | Single-cell transcriptome, subject to doublets/ambient RNA | Reference tissue/disease coverage, QC, doublets |
| Single nucleus | Nuclear transcriptome | Nuclear versus whole-cell domain shift and marker detection |
| Segmented spatial cell or nucleus aggregate | Counts assigned to an inferred polygon | Segmentation quality, count assignment, merged/split objects, background |
| 8 micrometer fixed bin | Spatial measurement that can contain partial/multiple cells | Mixed signatures, count depth, histology; label is a dominant expression identity hypothesis |

Do not call a bin a confirmed cell. CellTypist predicts classes; it does not estimate mixtures. Multiple probability-threshold matches are not deconvolution fractions and do not establish a doublet. Use a suitable mixture method such as RCTD if composition is the question, with its own validated input requirements.

## Reference selection

For a whole melanoma section, determine broad compartments including immune, stromal, endothelial, epithelial if present, and melanocytic/tumor populations. The paper's immune reference retains some broad nonimmune fallback labels (epithelial, endothelial, fibroblast), but cannot establish comprehensive nonimmune/tumor subtypes. Either use an appropriate broad model/reference or first identify immune candidates independently, then use immune-specific subtyping. Inspect actual model vocabulary and training metadata each time; do not assume a current pretrained melanoma model exists.

For custom training, require matched count matrix and per-cell labels, unique sample+barcode keys, donor metadata and gene identifiers. Check one-to-one label/count alignment explicitly. Curate disease states and rare types; hold out donors or studies. A melanocytic identity alone does not prove malignancy; use appropriate orthogonal tumor evidence.

## Three-sample workflow

1. Audit each sample's counts, segmentation, QC, markers and library quality separately. Confirm whether samples represent three independent patients, repeated sections, or paired timepoints.
2. Use one documented label vocabulary and model across comparable samples. Per-sample inference does not require inventing three different annotation schemes.
3. Preserve sample labels when concatenating. Merge/JoinLayers is not batch correction. Decide on integrated embeddings only after examining batch and biological confounding; retain uncorrected normalized expression for CellTypist.
4. Evaluate individual predictions by sample before majority voting. Choose overclusters per sample or jointly with explicit validation; neither strategy is mandatory. If custom overclusters are supplied as an array, ensure exact observation order.
5. Compare automated labels with manual markers, independent clusters and histology. Review conflicting cells/bins, rather than allowing voting to conceal them. Keep a confidence and uncertainty column.
6. Map labels spatially and inspect tissue boundaries, sparse bins and implausible mosaics. Distinguish ambient expression and mixed bins from rare biology.
7. Compare methods on a predefined review set. Use appropriate concordance at matched granularity, per-class performance where independent labels exist, and sensitivity to depth/segmentation/cluster resolution. Concordance between two reference methods is not independent truth.
8. Use patient/sample as the replication unit for condition comparisons. Thousands of cells or bins do not create thousands of independent biological replicates.

## Update safeguards

The paper's iterative update includes manual curation, cross-comparison and external validation. Do not automatically recycle predicted labels into training and then evaluate on those same cells. Keep baseline and adapted model versions, donor-held-out evaluations, and provenance of every label revision.
