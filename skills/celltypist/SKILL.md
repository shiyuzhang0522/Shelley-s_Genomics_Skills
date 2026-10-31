---
name: celltypist
description: Explain, plan, run and audit CellTypist cell-type annotation, majority voting and custom model training from single-cell expression data. Use for the cross-tissue immune atlas paper, model selection, normalization, uncertain labels, reference validation, batch effects, and adaptations to melanoma or Visium HD bins and segmented cells.
---

# CellTypist

Public edition: includes the operational guidance, authored scientific notes and supporting code. Use [paper sources](references/paper-sources.md) for original articles and figures; converted full-text reading packets are not redistributed here.

Use the paper as scientific evidence and the pinned software audit as the implementation contract. Distinguish original paper methods, current software behavior, and proposed adaptations. Do not insist on reproducing the paper when the user's data justify changes.

## Read the relevant reference

- For the whole paper, figures, methods and supplementary evidence: [paper sources](references/paper-sources.md). Open the original figures for numerical or visual claims.
- For main findings, cohort/model counts, interpretation, and the paper's atlas analysis code: [paper and atlas guide](references/paper-and-atlas.md).
- For executable API examples, preprocessing, model inspection, custom training, output semantics, and version-specific issues: [software workflow](references/software-workflow.md).
- For melanoma, spatial observations, uncertainty and validation decisions: [adaptation guide](references/adaptation.md).
- For original source identities and review limits: [provenance](references/provenance.md).

## Establish the task

1. Determine whether the user wants an explanation, pretrained annotation, custom reference training, model comparison, or reproduction. Ask only for missing details necessary for the next step.
2. Identify species, tissue and disease, assay, observation unit (cell, nucleus, segmented aggregate, fixed spatial bin), normalization state, gene identifiers, sample/donor/batch structure, and intended label granularity.
3. Inspect the selected model's actual labels, features, metadata, provenance and checksum. Do not infer coverage from a filename. An immune model is not a complete tumor-tissue classifier.
4. Preserve raw counts and unique observation IDs. For AnnData prediction, supply all available genes in log1p counts normalized to 10,000 per observation. Do not substitute scaled expression, residuals, integrated values, or latent embeddings. Follow the input-format-specific behavior in the software guide.

## Annotate and validate

1. Match biological gene identifiers and inspect model-feature overlap. Normalize before selecting overlap; do not fabricate measurements for genes absent from the assay. Report overlap and missing important markers rather than inventing a universal passing cutoff.
2. Obtain individual predictions first. Preserve decision scores and independent per-class probabilities; these are neither cell proportions nor necessarily calibrated correctness probabilities.
3. If appropriate, apply majority voting over sufficiently fine expression-based clusters. Retain both initial and voted labels. Inspect discordance, minority populations, rare cells and heterogeneous clusters. Spatial proximity alone is not a cell-type cluster.
4. Validate with positive/negative marker panels, independent clustering, sample-wise consistency, quality metrics, reference coverage and morphology/spatial evidence where available. Retain uncertain or unrepresented identities. Do not interpret every forced best-match prediction as a known true type.
5. Treat manual refinements as evidence-based changes with original label, revised label, confidence/reason, and supporting markers retained. The original paper combined automated annotation, expert curation and external validation.
6. Keep batch correction for embeddings/clustering separate from the expression matrix used by the classifier. The paper's atlas used integration; CellTypist does not itself imply batch-corrected input. Assess batch and biology before choosing a correction approach.

## Train or update a model

Use curated labels; separate biological types from states and artifacts. Partition validation by independent donor/study before fitting scaling or selecting features. Include per-class precision, recall, F1, confusion, rare-class support and out-of-reference checks. Do not report random-cell split performance as independent-donor generalization.

Consult the software guide for L2 logistic regression, one-versus-rest scores, feature selection, and explicit SGD/mini-batch options. Do not silently equate current defaults with paper training. Incorporate newly validated labels and version the resulting reference; avoid feeding unreviewed predictions back as truth.

## Deliver results

Record software/model versions, inputs, preprocessing, label vocabulary, overlap, prediction mode, majority-voting parameters, sample/donor IDs and validation evidence. Return annotation tables keyed by observation ID, expression/spatial diagnostics, and an explicit account of uncertainty and adaptations. State whether code was actually executed; a synthetic smoke test is not biological validation or reproduction of the atlas.
