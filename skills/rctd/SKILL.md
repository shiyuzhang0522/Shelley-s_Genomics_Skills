---
name: rctd
description: Explain, plan, run and audit Robust Cell Type Decomposition (RCTD) with spacexr for Visium, Visium HD, Slide-seq and segmented spatial data. Use for reference preparation, cell-type annotation and RNA-mixture deconvolution, doublet/full/multi mode choice, confidence interpretation, melanoma reference design, barcode and gene matching, version migration and troubleshooting. Distinguish the dmcable and Bioconductor interfaces and RNA fractions from physical cell fractions.
---

# RCTD

Public edition: includes the operational guidance, authored scientific notes and supporting code. Use [paper sources](references/paper-sources.md) for original articles and figures; converted full-text reading packets are not redistributed here.

## Scope and evidence

Use this skill for scientifically defensible RCTD analysis and statistical explanation. Do not treat it as a segmentation, malignant-cell discovery, cell-counting or differential-expression algorithm.

Read [evidence and versions](references/versions.md) first for execution. Guidance is grounded in the user-supplied main PDF (all 15 pages, six main figures, Methods and appended reporting summary), pinned upstream code, tutorials and selected issues reviewed on 2026-10-31. The supplied 71-page Supplementary Information has also been reviewed, including derivations, Table 1 and all 27 figures. A separately cited Supplementary Table 2 was not supplied. R/spacexr execution was unavailable in the creation environment; R examples are source-reviewed templates, not runtime-certified pipelines. The Python result auditor is separately tested. State these boundaries if asked; never claim full paper reproduction or a tested RCTD installation.

Load resources as needed:

- [Main-PDF interpretation](references/main-pdf-review.md): benchmark denominators, source panel-reference inconsistency, expression allocation and historical input details.
- [Supplement caveats](references/supplement-review.md): missing types, benchmark denominators, convergence and source inconsistencies.
- [Supplement mathematical audit](references/supplement-mathematics.md): detailed derivations and paper/code differences; consult for equation-level questions.
- [Paper and supplement sources](references/paper-sources.md): retrieve exact source pages, figures and Table 1 when needed.
- [Model and implementation](references/methods.md): estimation, assumptions, paper/code differences.
- [R workflow](references/workflow-r.md): preparation, version-specific calls, pilot and outputs.
- [Issues and troubleshooting](references/issues.md): maintainer advice versus community suggestions.
- [Study design](references/study-design.md): melanoma, HD, reference coverage and downstream analysis.
- [Source review record](references/source-review.md): evidence coverage and remaining work.
- `scripts/audit_rctd_results.py`: validate exported legacy full/doublet results, normalize full weights, preserve uncertainty and reconcile expected barcodes. Read `--help`. It does not run RCTD, accept raw Bioconductor assays, or certify biology.

## Establish the analysis contract

1. Inspect accessible metadata/code before asking for known details. Establish organism, tissue, technology, measurement unit (spot, bin size, segmented cell/nucleus), raw counts, reference labels/provenance, sample/donor IDs, objective and compute environment.
2. Inspect `packageDescription('spacexr')`, exported functions and `sessionInfo()`. Record implementation, version, revision and library. The package name alone does not identify the API.
3. Use the existing implementation unless migration is requested/needed. Keep legacy `Reference`/`SpatialRNA`/`create.RCTD`/`run.RCTD` separate from Bioconductor `createRctd`/`runRctd`. Record dependencies before changing an environment.
4. For planning, state assumptions and proceed. For execution, resolve unknown orientation, labels or measurement unit before fitting.

## Scientific distinctions

- Interpret normalized weights as cell-type RNA/count contributions, not measured cell counts or physical cell fractions. Cell-number conversion needs defensible type-specific captured-RNA-per-cell factors and sensitivity analysis.
- Singlet/doublet means one/two inferred **cell types**, not an exact cell count. Two same-type cells can appear as a singlet; a weak minority RNA component may also escape doublet detection. Related-type mixtures can remain unresolved even with balanced RNA (Supplementary Figure 7).
- Use nonnegative raw spatial counts; prefer raw reference counts. Do not feed log expression, SCT residuals, scaled/integrated values, embeddings or negative values into the count model. The linear-expression reference exception in the issues guide is not permission to use arbitrary corrected matrices.
- Reference abundance is not a prior on target abundance. Label quality, coverage and profile separation matter. Missing types can map to related types with misleading confidence.
- RCTD does not independently establish malignancy; validate malignant/normal reference labels with independent evidence.
- Default RCTD has no spatial-neighbor smoothing term. Coordinates support maps/downstream work; platform correction is estimated across the target dataset.
- `first_type` is not necessarily the largest weight. Likelihood gaps, convergence flags and weights are not posterior classification probabilities. Higher depth cannot repair missing reference types, and numerical convergence does not certify a global optimum or biological truth.

## Prepare inputs

Require genes-by-cells/locations count matrices, unique nonempty identifiers, finite nonnegative counts, exact metadata alignment, named label factors without unused levels, and finite two-column coordinates. Keep sparse matrices; avoid whole-dataset dense conversion.

Compute and retain full-library `nUMI` **before** deliberate gene restriction. Document denominators for panels/subsets; do not replace full totals with selected-marker totals. Explain intentional differences between supplied totals and matrix sums. Never repair barcode mismatches by positional renaming.

Audit species, identifier namespace and overlap before changing thresholds. Resolve duplicate mappings biologically; `make.unique()` does not align genes. Check overlap after spatial expression filtering too. Save removed genes/cells/spots and reasons.

Inspect reference cells per label after QC, donor/batch balance, marker coherence, rare-type uncertainty, malignant/normal coverage and related subtypes. Begin with broad types when finer states cannot be separated. Set a seed before reference downsampling and sigma sampling. Save the original reference: legacy `keep_reference=FALSE` retains a small subset after calculating profiles.

## Choose mode by measurement unit

| Unit/goal | Starting choice | Caveat |
|---|---|---|
| Conventional Visium with several types per spot | `full`, with `multi` sensitivity analysis | Validate small full weights; multi imposes a cap and greedy selection |
| Near-cell-resolution with at most two plausible types | `doublet` | A spatial doublet need not be a scRNA-seq technical doublet |
| Justified finite cap above two types | `multi`, document cap | Cap is not a known number of physical cells |
| HD bins or segmented cells | Inspect bin size, segmentation and UMIs first | HD is not automatically single-cell |

Choose a biologically justified primary mode; do not select for the prettiest map.

## Fit and audit

1. Pilot a representative subset spanning major compartments, with sufficient spots for calibration. Use one core to debug an unfamiliar HPC/R environment.
2. Inspect retained spots, reference counts per type, bulk/regression genes, markers and sigma-fitting eligibility. Omit unchanged defaults from concise scripts but save complete effective configuration.
3. Use legacy `test_mode=FALSE` for scientific runs. Do not copy artificial expression changes or relaxed C-SIDE settings from toy vignettes.
4. Save provenance, seed, configuration, logs, prepared/fitted RDS and attrition. Respect scheduler CPUs; avoid nested parallelism. Profile memory: internal code densifies selected-gene matrices.
5. Preserve sample/donor identity. Prefer sample runs or the documented replicate interface to blindly pooling slides. Re-fitting platform/sigma stages on arbitrary chunks changes calibration; it is not equivalent acceleration.

## Interpret mode-specific results

**Legacy full:** `@results$weights` is spots by types. Preserve raw weights, check finite/nonnegative values and positive totals, then row-normalize. Full `fitPixels` does not retain per-spot convergence flags: absence is not proof of convergence. Tiny weights are not automatic presence calls.

**Legacy doublet:** use `results_df`, `weights_doublet`, convergence and class flags together. `weights` is the preliminary full fit. For singlets, report the selected type with weight one and ignore the candidate second weight. For `doublet_certain`, map two weights to that row's first/second labels. For `doublet_uncertain`, retain the confident first identity at supported resolution, but do not assert complete composition. Rejects have no confident identity. Preserve/flag nonconverged rows.

**Legacy multi:** inspect `cell_type_list`, `sub_weights`, `conf_list`, `conv_all`, `conv_sub`; attach barcodes from fitted-object order. Its result list is not a `$weights` matrix.

**Bioconductor:** assays are **types by spots**, opposite to legacy weights. Inspect assay name and `colData` confidence. Handle rejected/zero or partially confident columns separately; never normalize them blindly into confident mixtures.

## Biological validation and reporting

Map predictions, uncertainty, UMIs and marker expression alongside histology. Check multiple coherent markers and, where possible, independent markers excluded from fitting. Assess missing types, subtype ambiguity, reference/donor sensitivity, mode choice and depth-related confidence. Successful execution is not biological validation.

Report reference/labels, assay/resolution, identifiers, preprocessing/attrition, version/revision, mode/parameters, RNA units, confidence policy, convergence limits and sensitivity checks. Preserve unassigned locations in denominators; distinguish retained/confident-only summaries.

Use donor-level biological replication when several sections share a donor. Account for composition and spatial dependence; spots are not independent donors. For cell-type-specific DE, consult C-SIDE separately; do not treat RCTD-attributed counts as independently observed single-cell data.

Cite Cable et al., *Nature Biotechnology* 40, 517–526 (2022), DOI: 10.1038/s41587-021-00830-w. Cite the separate C-SIDE paper only when used.
