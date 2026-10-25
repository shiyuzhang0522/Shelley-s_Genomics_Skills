---
name: cellchat
description: Explain, run, compare, and troubleshoot CellChat v1/v2 cell-cell communication analysis from human or mouse single-cell RNA-seq and spatial transcriptomics, including melanoma Visium/Visium HD. Use for ligand-receptor networks, CellChatDB selection, Seurat/SCE/AnnData inputs, spatial calibration, pathway/centrality/pattern analysis, and condition comparisons. Keep Spatial CellChat v3 separate; do not treat inferred networks as causal or donor-level statistical evidence.
---

# CellChat

Infer directed, group-level ligand-receptor networks from normalized expression and a curated molecular database. Explain the model before interpreting its plots. Use downstream receiver programs/NicheNet as complementary evidence, not as CellChat input requirements.

## Read the relevant reference

- [Method rationale](references/rationale.md): both papers, model, null hypothesis, network interpretation.
- [Core workflow](references/workflow.md): installation, input conversion, validated preflight, current-v2 analysis recipe.
- [Spatial and multiomics](references/spatial.md): units, contact/diffusion, Visium HD, samples, RNA/ADT.
- [Comparisons and visualizations](references/comparisons.md): sample design, lifting, graph roles, NMF, embeddings, plotting.
- [Troubleshooting](references/troubleshooting.md): reviewed issues, version mismatches, missing signals, database changes.
- [Sources and coverage](references/sources.md): exact snapshot, every tutorial, paper/issue coverage, validation limits.

## Establish the question and version

Read available metadata and environment first. Record species, assay, normalization, gene identifier type, observation unit (cell/segmented cell/bin/mixed spot), group annotations, sample/section and donor identifiers, condition/contrast, and intended inference. Ask only for missing design choices that materially change the analysis.

This skill's code baseline is `jinworks/CellChat` commit `75253cd0c9e68410e6e721a6d3a0419a1d7e358f`, DESCRIPTION `2.2.0.9001`. Inspect `packageVersion("CellChat")`, installed source/exports, and object version. Current README also links a separate `jinworks/SpatialCellChat` v3 package; do not mix constructors, object slots, or single-cell-pair claims into v2. Route a requested v3 task to a fresh review of that repository.

Cite the 2021 Nature Communications paper and, for versions >=1.5, the Nature Protocols article published online in 2024 (journal issue 2025). Preserve DOI identity rather than assuming the year in its DOI is the journal year.

## Protect input meaning

Use genes-by-cells nonnegative normalized expression with species-matched symbols. `raw.use=TRUE` means unsmoothed normalized signaling expression, not raw counts. Do not use scaled/integrated residuals, UMAP coordinates, gsMap P values, or SpaCET fractions as expression. Inspect Seurat v5 layers and AnnData matrix provenance; avoid double normalization, HVG-only matrices, and accidental densification.

Source [check_inputs.R](scripts/check_inputs.R) and call `check_cellchat_inputs()` with explicit normalization and sample IDs. It validates values/names, aligns metadata/coordinates by barcode, checks spatial factors, and reports group-size exclusions while preserving sparse input. It cannot certify biological annotation, symbol mappings, normalization provenance, or coordinate units.

Never permit the constructor's fallback of relabeling mismatched metadata row names. Preserve donor IDs separately from sample/section IDs. Remove missing labels and unused factor levels deliberately; do not invent cell types for mixed spots.

## Run explicit, reproducible inference

1. Select and save the actual species-specific DB and interaction categories. Audit gene/complex coverage. Database choice changes the tested universe; current tutorial secreted-only and full-DB analyses are different scopes.
2. Run `subsetData`, gene overexpression filtering, and LR candidate selection. Set the DE backend and `variable.both` explicitly: current default TRUE requires both endpoints selected, while older tutorial prose describes the either-endpoint FALSE rule. Candidate selection is not interaction significance.
3. Choose expression summary, smoothing, population weighting, permutations, seed, and spatial settings. Use `smoothData(..., adj=...)` for this snapshot only when justified, then `raw.use=FALSE`. Do not tune settings solely to recover an expected pathway.
4. Run `computeCommunProb`, preserve the prefilter object, filter group/sample support, then summarize LR/pathway/network tables. Check empty/degenerate outputs before optional analyses. Current `min.cells=10` removes groups with <=10 cells; `nboot` is a permutation count.
5. Keep raw arrays, used DB, group/sample counts, tested interactions, parameters, input checksums, full tables, and `sessionInfo()`. Inspect tables and underlying expression before plotting.

## Interpret within the model

CellChat's `prob` is a model score, not calibrated binding probability, measured contact frequency, causal effect, or proof of downstream regulation. Complexes and cofactors matter; inspect all required subunits and distinguish unmeasured from zero expression.

The current permutation test shuffles cell-group labels and computes strict upper-tail frequencies. A zero P value is finite-permutation output, not literal zero uncertainty. Interaction P values are not automatically FDR-adjusted. Pathway sums, centrality, NMF patterns, and embeddings are summaries of inferred networks, not independent confirmation.

For comparisons, harmonize preprocessing, DB, labels, settings, and plotting scales. Pooled cells do not supply independent donor replication. Default `rankNet(do.stat=FALSE)` for descriptive graphics: its optional test uses graph edges, and some insufficient-data cases receive placeholder zero P values. Imported `updateCCC_score` P=0 values can also be placeholders. Never report either as patient-level evidence.

For spatial data, verify units from actual files, distinguish physical conversion `ratio` from numeric `scale.distance`, and keep unrelated sections separate. `distance.use=FALSE` still applies spatial feasibility filtering. `min.samples` is an expression-consistency filter, not per-donor spatial/permutation significance. Read the spatial reference before applying the recipe to HD.

## Deliver and scope

Return the design, normalization/DB/version provenance, QC and omissions, LR/pathway tables, a few clearly labeled plots, sensitivity/replicate evidence, and limitations. Use the ng-figure skill for requested publication styling. Do not claim a physical mechanism or statistically established condition effect from a visually attractive network.

Source review covers both main papers and all nine narrative tutorial/FAQ Rmd files. Supplements and rendered tutorial graphics are not exhaustively reviewed; the issue review is targeted, not the entire tracker. Consult the coverage reference for test scope. Keep every future runtime result separate from what was verified when this skill was built.
