# Study design: melanoma, Visium HD and downstream use

These are analysis recommendations inferred from RCTD's data model and inspected implementation, not melanoma/HD performance claims from the original paper.

## Reference design

- Cover malignant melanoma states, normal melanocytes if plausible, keratinocytes, fibroblasts, endothelial/perivascular populations and relevant immune populations. Do not force a normal melanocyte into a malignant label because normal melanocytes were absent from the reference.
- Establish malignancy in the reference using the study's labels, CNV evidence, matched genetics/pathology or other justified independent evidence. Melanocytic marker expression alone does not establish cancer.
- Related malignant states can be less identifiable than broad lineages. Use broad classes first, class-aware confidence or a planned hierarchical analysis. Avoid interpreting a small difference between similar reference profiles as a definitive state assignment.
- Include enough high-quality cells across donors/states without confounding every cell type with a different platform. Use donor holdouts or alternate-reference fits for sensitivity where feasible. Reference cell counts need not mirror tissue prevalence.
- Retain raw RNA counts for estimation even if integration embeddings helped annotate cells. Document whether the reference is single-cell or single-nucleus; the shared platform correction cannot guarantee removal of every type-specific bias.

## Spatial unit

For conventional Visium, mixed-cell spots typically motivate full or multi mode. For Visium HD, explicitly identify 2/8/16-micron bins, another aggregation, or cell/nucleus segmentation and the particular software/output. Do not assume bin diameter implies a complete cell. A segmented object may include neighboring RNA or omit cytoplasm. Review counts, detected genes, segmentation boundaries and tissue context before choosing doublet mode.

Do not impose the original mouse Slide-seq UMI thresholds as universal biological QC. Inspect the count distribution and test a defensible range; report exclusions and calibration eligibility. Sparse HD bins can require appropriate aggregation before deconvolution, rather than arbitrary lowering of every cutoff.

## Per-sample calibration and scalability

Use a common, documented reference across samples when comparative interpretation is intended, but preserve sample-level platform calibration. Pilot representative tissue regions and profile memory. Legacy internals convert selected genes across spots to dense arrays; sparse input does not remove all memory costs.

Running complete RCTD independently on random chunks re-estimates platform effects and sigma in each chunk. If scaling requires chunking, either accept and document this as a sensitivity-tested approximation, or design and validate a fixed-calibration workflow against an unchunked pilot. Do not provide an untested slot-editing shortcut as equivalent to the original pipeline.

## Validation

Use histology, coherent marker panels, confidence/depth maps, held-out markers where possible and alternative references. Investigate predictions absent from expected anatomy. Test broad versus fine labels and mode sensitivity. Retain rejections and ambiguous calls, including their spatial distribution; a forced complete label map hides model failure.

## Combining with gsMap or other spatial traits

Join by explicit sample ID plus exact spot/cell barcode. If the two analyses use different bins or segmentation, define a spatial aggregation/mapping and validate it; never join by row order. Keep the original RCTD units as RNA fractions. RCTD weights sum to one, so all types plus an intercept are collinear; choose a justified compositional analysis or reference category and assess spatial dependence. Account for donor/sample clustering and distinguish descriptive association from causal cell-type effects. Do not choose an RCTD reference or thresholds to maximize the gsMap association.

Multiple sections/tissue blocks from one donor remain clustered within that donor for population inference. Preserve sample-level estimates and quantify between-donor variability. Biological replication is not the number of spots.

## C-SIDE boundary

RCTD estimates mixtures; C-SIDE performs a separate gene-expression inference task with its own covariates, identifiability and replicate requirements. Do not copy relaxed vignette FDR/cell thresholds into real data. Do not call RCTD's fitted gene allocation an independently measured single-cell expression matrix. Consult the C-SIDE paper and current package guidance before promising that analysis.
