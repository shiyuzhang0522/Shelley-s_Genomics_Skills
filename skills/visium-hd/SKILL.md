---
name: visium-hd
description: Explain, plan, adapt and audit Visium HD analysis using the three-section CRC workflow from Oliveira et al., Nature Genetics 2025 (10.1038/s41588-025-02193-3) and its source code. Use for joint Seurat sketch/manual annotation, RCTD, 8-µm bins, nuclear aggregation of 2-µm squares, tumor periphery, macrophage niches, ROI/density analysis, LIANA, or adaptation to three melanoma samples.
---

# Visium HD

Public edition: includes the operational guidance, authored scientific notes and supporting code. Use [paper sources](references/paper-sources.md) for original articles and figures; converted full-text reading packets are not redistributed here.

Ground analysis in the CRC paper and pinned author code. The three spatial sections are **P1CRC, P2CRC, P5CRC**, from different patients; distinguish them from the full five-patient multimodal study.

## Read the relevant evidence

- [Code and workflow map](references/code-workflow.md): actual functions, parameters, inputs/outputs and discrepancies.
- [Three-section plan](references/three-section-plan.md): execution order, checkpoints and adaptation decisions.
- [Paper sources](references/paper-sources.md): article, supplementary material and reading boundaries; use the original sources for exact figures and wording.
- [Provenance](references/provenance.md): source versions, coverage and validation limits.
- [Author source snapshots](references/source-code/README.md): inspect relevant scripts before writing implementation code; preserve the [license](references/source-code/LICENSE.md).

Treat scripts as evidence until execution is requested. Do not run them wholesale: inspect hard-coded paths, undefined objects, metadata joins and coordinate handling. Separate **paper-described**, **code-observed**, **adaptation**, and **unverified** statements. Cite section/figure and pinned code path for exact settings.

## Establish inputs

Inspect project files before asking for information. Record sample/patient IDs, tissue/treatment context, chemistry, Space Ranger version, count matrices, coordinates, scale factors, H&E and resource limits. Choose the spatial unit explicitly. Preserve raw counts and sample-specific barcode/coordinate mappings. Do not silently apply this probe-based FFPE workflow to other HD chemistries or newer cell-segmentation output.

## Follow the workflow

1. Inspect each section's tissue mask, registration, UMI/features distributions and coordinate units. Do not apply the Flex single-cell QC quantiles as spatial-bin thresholds.
2. Combine 8-µm matrices with sample-qualified unique barcodes. Normalize, select variable genes and sketch using leverage scores. The paper describes **15%**, but `Figure_3.R` sets **240000 bins**; calculate the intended budget and record sample representation.
3. Cluster with **20 PCs/resolution 0.8**, inspect markers and histology, and assign broad identities. Recluster within broad groups with **25 PCs/resolution 0.1**, then interpret subtype markers. Retain unknown/mixed profiles. Never reuse the authors' cluster-number label vector on new data.
4. Project annotations to all bins and review every section. The source uses 50 dimensions for projection despite 20 for initial clustering; preserve this distinction and check software compatibility.
5. Build RCTD reference from raw scRNA counts and named labels; verify exact barcode alignment and gene overlap. Run **per section** in doublet mode. The paper specifies **minimum 100 UMIs**, while the source omits an explicit threshold; resolve filtering/defaults for the actual spacexr version. Keep singlet, doublet_certain, doublet_uncertain and reject calls.
6. Compare manual and RCTD labels at common resolution and barcode universe using markers/histology. Agreement is not independent ground truth. Do not force subtype labels onto unresolved bins.
7. For small T cells or nuclear analysis, use StarDist H&E nuclei, map native 2-µm squares into polygons, sum counts per nucleus and inspect marker-expression overlays, as in the source. Re-running clustering or RCTD on this matrix is an additional analysis, not a demonstrated step of the published nuclear branch. Call these **nucleus-aggregated profiles**, not validated whole cells. Check scale, transforms, crop origins, overlaps and unmapped squares.
8. Select downstream branches after annotation QC: tumor periphery, macrophage subclustering, singlet-bin density, ROI expression/enrichment, per-patient LIANA, or optional Xenium/TCR validation. Consult the code map for branch-specific settings.

## Preserve scientific distinctions

- Merging, JoinLayers, scaling, sketching and projection do not themselves remove batch effects. No explicit Harmony/CCA/RPCA/IntegrateLayers correction was found in the reviewed three-section spatial path. Treat added correction as an adaptation and assess batch versus biology first. The word “integrated” alone does not establish a correction algorithm.
- An 8-µm bin can include partial or multiple cells. Sketching enriches rare profiles; use the full annotated universe for composition and state denominators and unresolved fractions.
- A labeled scRNA reference does not require spatial segmentation. It can support 8-µm bins or nucleus-aggregated targets.
- Bin-level tests do not establish patient-level replication. The spatial biological sample size is three patients, not the number of bins.
- For melanoma, replace CRC references/markers and tumor-definition rules; re-evaluate thresholds and states. Melanocytic identity alone does not prove malignancy.
- The original segmentation is StarDist-based nuclear aggregation, not Bin2Cell. Label alternative segmentation pipelines as adaptations.

## Deliver and validate

For explanation, give the answer, source evidence and relevant uncertainty. For planning, provide an input manifest, ordered outputs/checkpoints, annotation decisions and resource estimates based on actual dimensions. For implementation, parameterize paths/IDs, separate source fixes from biological changes, smoke-test representative inputs before large runs, and record versions/seeds.

Creation-time validation covers the reading package and source mapping. It does not establish execution of the biological pipeline or reproduction of the published figures. Read provenance before claiming exact reproducibility.
