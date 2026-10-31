# Supplement: practical interpretation and caveats

Reviewed all 71 pages of the supplied Supplementary Information on 2026-10-31: mathematical derivations, experimental methods, Supplementary Table 1, all 27 figures and captions, and references. PDF page numbers below include the cover; printed page numbers differ. Read the [source packet](paper-sources.md) for exact source images/captions and the [mathematical audit](supplement-mathematics.md) for equations and implementation differences. These are reading and code-inspection findings, not a new RCTD performance experiment.

## Decisions to carry into analysis

1. **Estimate RNA contribution.** Equation (1), PDF p2, averages each reference cell's gene-count/full-library-UMI ratio within a label. Equations (2)–(4) mix UMI origins. Do not interpret fitted fractions as physical cell-number fractions or use observed scRNA library sizes as universal cell-size correction factors.
2. **Keep full-library totals and raw weights.** The free spot scale accommodates changes in the selected genes' overall expression mass. Equation (21), p6, uses `w = beta * exp(alpha)`, so raw fitted weights need not sum to one. Preserve them, audit nonnegativity/positive totals, and normalize only when forming RNA fractions. Selected-marker totals do not replace full-library `nUMI`.
3. **Treat confidence as conditional on the reference.** Figures 10–11 show missing-reference behavior; greater depth can increase confident assignments while a reference class is absent. The reported confidence curve is across the tested dataset, not proof that a particular fraction of missing-type cells are confidently wrong. Unknown-type discovery is not built into the method.
4. **Use broad labels where necessary.** Figure 7 shows poor same-class/related-type doublet detection even with balanced RNA. More depth or equal contributions cannot ensure separation of near-identical profiles. A singlet call is not proof of one cell, one nucleus or physical purity.
5. **Match mode to the measurement.** Figure 21's Visium analysis explicitly does not constrain type count. Multi mode uses a greedy, penalized search with a cap; neither its selected type count nor the cap is a physical cell count. Conventional Visium does not justify an automatic doublet assumption; HD also requires resolution/UMI/segmentation assessment.
6. **Report assignment coverage alongside accuracy/biology.** Confident-only maps omit difficult locations. Keep excluded, rejected, uncertain and nonconverged locations in audit tables. Inspect confidence versus depth and compartment rather than hiding low-depth regions.
7. **Do not equate numerical stability with correctness.** The likelihood is nonconvex. Figure 25 checks selected cerebellum pixels, not all possible inputs. Small updates, a convergence flag or reproducibility across references cannot certify a global optimum or correct biology.
8. **Follow the installed version.** Historical confidence/complexity thresholds 10/25, continuous sigma SGD and linear interpolation differ from the inspected public implementation. Record effective configuration rather than reconstructing software from printed equations.

## Evidence map and denominators

| Supplement evidence | Supported conclusion | Limit to retain |
|---|---|---|
| Figs 1–4, pp17–24 | Marker/anatomical comparisons and platform correction motivate mixture fitting | Qualitative patterns and selected simulations do not establish universal ranking over other tools |
| Fig 5, pp25–26 | Estimated fractions with more than two types differ strongly by dataset; Visium hippocampus is much more mixed in this analysis | These are model-estimated type counts, not measured cell counts or a default for every tissue |
| Figs 6–7, pp27–30 | Minority RNA and profile similarity affect doublet detection | Balanced RNA does not guarantee detection of similar types; retain the source panel discrepancy below |
| Fig 8, pp31–32 | Extra reference types absent from the target receive few confident predictions in this test | Extra reference types are a different problem from true target types missing from the reference; displayed counts are not a universal false-discovery rate |
| Fig 9, pp33–34 | Known Bergmann–Granule simulated doublets can be misclassified, with identifiable gene likelihood contributions | An influential gene in this comparison is not a universally specific marker or causal explanation |
| Fig 10, pp35–36 | Depth changes confident assignment coverage; panel c reports accuracy restricted to confident calls | No universal reliable-depth cutoff; high confident-only accuracy can coexist with low coverage |
| Fig 11, pp37–38 | Removing related subtypes or an entire class redirects predictions to available labels | The caption does not fully define confidence inclusion/normalization for the matrices; do not invent rejection rates |
| Fig 12, pp39–40 | Multi mode tested on exactly three/four types at 10,000 UMIs; reported cell-class accuracies 87.7%/91.0% | Panel a conditions on pixels predicted to contain at least k types. The two overall accuracy denominators are not fully specified in the caption; not whole-mixture or fine-subtype accuracy |
| Fig 13, pp41–42 | Unconstrained, class-aggregated RNA proportions in three/four-type simulations | Class aggregation hides related-subtype ambiguity; do not automatically equate the historical setting with a modern API without checking code |
| Figs 14–16, pp43–48 | Two reference platforms give 95.7% agreement among confident type predictions | Agreement is not accuracy against independent truth; reference vocabularies differ |
| Figs 17–19, pp49–54 | Predicted cortical/hippocampal localization is anatomically plausible | Sparse panels do not prove absence; categorical assignments and fraction maps are different outputs |
| Figs 20–22, pp55–60 | Marker concordance and spatial localization across Slide-seq/Visium; unconstrained Visium fit in Fig 21 | Marker panels are counts per 500 with distinct scales; weight panels are 0–1. These are not paired ground-truth accuracy measurements |
| Figs 23–24, pp61–64 | Gad1 ISH supplies external anatomy; confident clusters represent 25 of 27 reference interneuron subtypes | No claim of all 27 recovered, or per-spot independent subtype truth |
| Fig 25, pp65–66; Methods p7 | Tolerance and initialization sensitivity checks on selected cerebellum pixels | Empirical numerical stability; no universal optimum/identifiability guarantee |
| Fig 26, pp67–68 | Ward clustering of 27 reference subtype log-expression profiles | Reference taxonomy context, not independent validation of inferred spatial classes |
| Fig 27, pp69–70 | Historical sigma/likelihood traces stabilize on two datasets | The inspected code now uses discrete sigma selection; historical SGD plots do not validate that implementation on new data |

Do not transfer the mouse Slide-seq laboratory recipes (pp12–15), dataset-specific fitted sigma values (Table 1, p11), or historical runtime into default settings for a human melanoma project. Table 1 is preserved as an image and a checked CSV. The separate Supplementary Table 2 cited by the main article was not included in this PDF and has not been reviewed.

## Platform correction and Poisson assumptions

At a fixed total UMI count, categorical sampling yields multinomial counts with cross-gene dependence. Independent Poisson genes are a rare-category approximation, or arise after randomizing the total count with a Poisson distribution. Plugging the observed library size into the latter is an approximation. The cited N≥100 example and small gene probabilities motivate that example; they are not a universal validity or accuracy threshold.

Gene-specific platform correction is shared across cell types and estimated from target pseudobulk. It cannot guarantee correction of type-specific assay effects, state mismatch or absent populations. Gaussian pseudobulk concentration arguments require finite moments, sufficiently independent residuals and no dominant few weighted spots. Spatial dependence and highly unequal contributions can weaken that reasoning. Re-estimating calibration separately on arbitrary chunks changes the fitted model.

Equation (21)'s unnormalized `w` reconciles the free scale with simplex `beta`. Conditional Poisson mean equals variance, but random intensity introduces extra variability. Do not describe the baseline rate before the residual multiplier as the exact marginal mean without specifying the random-effect distribution.

## Convergence and version differences

The p7 tolerance experiment uses 1,000 cerebellum pixels: changing tolerance from 0.001 to 0.000001 gives mean L1 difference 0.0022, maximum 0.0047. The random-start experiment uses 50 starts for each of 50 pixels and reports maximum L1 discrepancy 0.000004. These are empirical results on tested inputs. A stopping tolerance is not a bound on error from biological truth or a certified optimum.

At pinned legacy revision `9f5dc33`, `solveIRWLS.weights` unconditionally resets `solution` to a uniform vector despite accepting that argument. Passing random starting vectors does not reproduce Figure 25c. Use a controlled versioned experiment if genuine multistart validation is required; do not silently patch production internals.

The supplement describes 500 sampled pixels and stochastic sigma updates; inspected code uses up to 1,000 eligible spots, discrete sigma candidates and up to eight epochs. Its bulk objective, Hessian regularization and spline evaluation also differ. Read [methods](methods.md) and [version table](versions.md) before specifying exact reproduction. A convergence flag records a numerical stopping rule, and legacy full mode does not retain all per-spot flags.

## Printed inconsistencies: retain source, annotate interpretation

These are review findings about the supplied document, not an official erratum and not evidence that RCTD is unusable.

| Location | Finding | Operational consequence |
|---|---|---|
| Fig 3 caption, p22 | Calls column 2 NMFreg; visible column 2 is RCTD | Identify methods from visible column headers |
| Fig 6 caption, p28 | Descriptions of panels b/c are reversed relative to the visible plots | Use b for proportions, c for doublet rate; retain original caption separately |
| Methods p5 after Eq (15) | Gives `E[epsilon] = exp(sigma²/2)` | That Gaussian identity belongs to `E[exp(epsilon)]` |
| Methods p9, Eqs (40)–(41) | Printed heavy-tail denominator lacks the absolute value used in code; the printed sigma derivative has a sign/factor inconsistency | Do not implement the printed formula blindly; consult the mathematical audit and pinned source |
| Methods pp7–9 | Nonconvex/global-optimum disclaimer coexists with overstrong local/global convergence wording and maximize/minimum wording | Report numerical convergence empirically; step-size sum conditions alone do not prove a global optimum |

The mathematical audit additionally records index/probability-normalization issues and an explicitly reviewer-derived limitation: exact inverse-square tails on a log random effect have divergent exponential moments, so the earlier finite-variance Gaussian concentration proof does not transfer literally to that robust extension. Per-count mixture probabilities remain finite. Current numerical quadrature is finite, and the current sigma routine does not use the printed derivative. Do not turn these distinctions into an unsupported runtime-failure claim.

## Downstream interpretation

Equations (44)–(49), p10, allocate gene UMIs with probability proportional to `beta * mu`. Shared multiplicative effects cancel across cell types; type-specific effects would not. The output is conditional expected allocation using fitted reference profiles and weights, not newly observed independent cell expression. Estimation uncertainty remains. Use justified downstream inference, donor-level replication and independent validation; do not claim causal interactions from local colocalization.

For melanoma, prioritize malignant/normal melanocyte separation, broad immune/stromal coverage, histology and marker checks, plus independent malignancy evidence where available. Compare reference donors/labels and reasonable mode settings. Save raw outputs and all uncertainty classes, then summarize RNA composition with explicit denominators.
