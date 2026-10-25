---
name: nichenetr
description: Plan, explain, run, and troubleshoot NicheNet ligand activity and ligand-target analyses with the nichenetr R package. Use for prioritizing ligands that may explain receiver-cell gene programs in human or mouse single-cell, sorted bulk, or annotated spatial data, including melanoma Visium HD. Cover sender-focused versus sender-agnostic analysis, gene-set/background QC, v2 priors, Seurat inputs, and interpretation; not cell annotation, deconvolution, or causal validation.
---

# NicheNet

Generate testable ligand-to-target communication hypotheses. Keep receiver response genes, eligible background genes, and candidate ligands distinct.

## Route the request

- Explain the method using [method notes](references/method.md).
- Plan/run analysis using [workflow and R recipe](references/workflow.md).
- Adapt to melanoma spatial data, SpaCET, or gsMap using [spatial design](references/spatial-design.md).
- Check installation, model downloads, and version boundaries in [sources and environment](references/sources.md).

## Establish the design

Record species, measurement unit (cell, segmented cell, bin, mixed spot, sorted bulk sample), receiver type, senders, contrast or external gene program, donor/sample IDs, and biological question. Infer from supplied metadata; ask only for missing information that changes analysis.

Choose one receiver type per run. Compare the same receiver type across conditions. Use donor-aware differential expression or pseudobulk for replicated studies; cells and bins are not independent patients. With one sample per condition, label findings exploratory. Use annotated expression rather than UMAP coordinates, gsMap scores, or cell fractions to determine expression. Keep annotation and malignant-cell identification upstream.

## Validate inputs

1. Use species-matched official symbols. Audit Ensembl mapping, aliases, missing mappings, and duplicates; never silently capitalize mouse symbols.
2. Use matched prior versions and species: target genes in ligand-target matrix rows, ligands in columns; ligand-receptor network `from` = ligand, `to` = receptor. Record filenames, hashes, model release, package version, and commit.
3. Define expressed genes per receiver/sender population with explicit detection thresholds. Consider 5% and 10% sensitivity checks when suitable, not universal thresholds. Use RNA expression, not integrated residuals, for detection.
4. Define the receiver program from a justified contrast or independent gene set. Restrict to tested, expressed, prior-covered receiver genes. Use that eligible universe as background, including program genes. Report retained/excluded counts and program/background fraction.
5. Stop on empty candidates/program/background, program equal to background, duplicate/missing matrix names, or nonfinite selected scores. Investigate small universes rather than silently substituting every prior gene or using only significant genes as background.

## Score and interpret

Run sender-agnostic candidates (ligands with expressed receiver receptors) and sender-focused candidates (add expression in chosen senders), intersected with prior columns. An agnostic result does not identify a sender. Retain expression evidence for each sender rather than assigning pooled ligands to every population.

Call `predict_ligand_activities()` with the same program/background for both modes. For v2 rank descending `aupr_corrected`, retaining AUPR, AUROC, and Pearson. If corrected AUPR is absent, resolve version provenance; do not silently substitute Pearson. Changing only the candidate list does not alter an individual ligand's single-ligand score.

Choose an explicit top-k for inspection, not statistical significance. `get_weighted_ligand_target_links()` selects top-n targets across the prior before intersection with the supplied program; ties may exceed n. Remove NA and zero-weight links from supported predictions; preserve raw scores separately from display cutoffs.

Never call activity a p-value, causal effect, or measured interaction strength. Negative Pearson is not repression. The prior is unsigned; RNA expression does not prove secretion or receptor activation. A top-ranked ligand may have weak support. Inspect enrichment quality, targets, expression, coverage, and sensitivity before biological conclusions.

## Deliver

Return design, QC/excluded genes, all ligand rankings for both modes, ligand-target links, ligand-receptor candidates with sender evidence, and concise interpretation. Save parameters, input/prior checksums, versions, and `sessionInfo()`. Plot only after table review; use ng-figure when publication styling is requested. Keep donor replication, spatial proximity, and perturbation validation separate.

## Coverage and execution boundary

The skill is grounded in public code/tutorials and an abstract-level paper synthesis. Full-paper PDF, figures, and supplement conversion is incomplete because those sources were inaccessible. Paper2Skill verification covers only the authored notes. The R recipe was checked against upstream APIs but not executed at creation because R was unavailable; smoke-test in an R-enabled environment before a full analysis.
