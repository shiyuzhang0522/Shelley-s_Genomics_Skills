# RCTD model and implementation

## Reading map

Read the [published article](https://pmc.ncbi.nlm.nih.gov/articles/PMC8606190/), especially Methods: Statistical model, Fitting the model, Supervised estimation, Gene filtering, Platform effect normalization, Robust Cell Type Decomposition, and Cell type identification by model selection. The complete supplied main PDF and its six main figures have been directly reviewed; see [main-PDF interpretation](main-pdf-review.md) for benchmark denominators and source inconsistencies. All 71 supplied supplementary pages are now reviewed; see [practical caveats](supplement-review.md) and the [mathematical audit](supplement-mathematics.md).

## Mathematical model

For spot i, gene j and reference type k:

\[
Y_{ij}\mid\lambda_{ij}\sim\operatorname{Poisson}(N_i\lambda_{ij}),\quad
\log\lambda_{ij}=\alpha_i+\log\sum_k\beta_{ik}\mu_{kj}+\gamma_j+\epsilon_{ij}.
\]

N is total captured UMIs; mu is a type-specific relative expression profile; beta is the RNA mixture; alpha scales the spot; gamma adjusts gene-specific platform effects; epsilon adds residual variation. Beta is nonnegative and sums to one in the paper's parametrization. The conditional Poisson mean equals variance; random expression rates allow extra variation. The paper uses a robust heavy-tailed modification of the random-effect distribution. It validates simulated mixtures, cross-platform transfer and brain spatial patterns; these do not establish guaranteed performance in melanoma or HD. Missing reference types and similar profiles are key limitations. The original paper uses doublet penalty 25 and confidence gap 10; distinguish them from current public API defaults.

## Source-derived mechanics

The following describes [legacy revision 9f5dc33](https://github.com/dmcable/spacexr/tree/9f5dc33c8060f946c6072a138b70e189636e1435), not a reimplementation of supplementary derivations.

1. **Reference means (`R/processRef.R`).** `get_cell_type_info` divides each reference cell's gene counts by that cell's `nUMI`, then averages normalized vectors within each label, including zero entries. It is the mean of cell-specific ratios, not pooled counts divided by pooled UMIs. Hence high-depth cells do not automatically get more weight in the reference mean. Class abundance does not directly set the target mixture.
2. **Gene selection (`R/utils.R`, `R/spacexr.R`).** For each type, compare its expression to the equally weighted mean of the other types; use natural-log fold change with epsilon 1e-9. Require expression and log-fold-change thresholds. This is marker selection, not a DE p-value test. Spatial bulk counts must be at least `MIN_OBS=3`. The literal mitochondrial pattern is lower-case `mt-`, case-sensitive; do not claim all human `MT-` genes are automatically removed. `prepareBulkData` additionally requires gene bulk counts >=10 for the bulk fit.
3. **Bulk calibration (`R/platform_effect_normalization.R`).** `fitBulk` sums spatial counts, estimates target mixture weights and builds `get_norm_ref` profiles. For a gene, the correction matches the observed spatial bulk fraction to the reference mixture fraction. One gene correction is shared across types. The current bulk objective uses log-expression residuals (`get_der_fast(..., bulk_mode=TRUE)`); avoid describing every numerical implementation detail as identical to the paper's hierarchical formulation.
4. **Residual scale (`choose_sigma_c`).** Select up to 1,000 eligible spots with `nUMI > UMI_min_sigma` (strictly greater, default 300), alternate fitting and table-based likelihood comparisons, for up to 8 epochs. The recorded sigma is dataset-level in this implementation. A low-depth dataset can have zero eligible spots even after passing `UMI_min`.
5. **Optimization (`IRWLS.R`, `prob_model.R`).** Iterative quadratic-program updates enforce nonnegative weights; likelihood tables and cubic splines accelerate evaluation. The public fit paths use `constrain=FALSE`, so the sum can absorb spot scale. Supplement Eq. (21) explains this as w = beta exp(alpha). Normalize full weights for fraction summaries while retaining raw values. Numerical stopping is not a guarantee of global optimality; the source and code differ in sigma fitting, interpolation and Hessian regularization. Heavy tails appear in `ht_pdf_norm`; current likelihood code caps counts using table-dependent `K_val`. Do not independently clip counts or patch internals without versioned validation.
6. **Doublet search (`RCTD_helper.R`).** An initial full fit selects candidate types with raw weight >0.01, with fallback candidates if needed. Candidate pairs are scored; plausible alternative pairs determine confidence. Compare a singlet fit to the best pair with a penalty. Current code searches candidate pairs, rather than simply accepting the two largest full weights. `calc_log_l_vec` is a negative-log-likelihood score (smaller is better), not a probability. The stored `singlet_score` on rejected spots may be an arbitrary placeholder; never interpret its difference as a calibrated test.
7. **Multi mode.** Greedily add types if score improvement exceeds the penalty, up to the configured cap; check alternatives and refit selected weights. It is not exhaustive best-subset inference.

## Interpreting RNA units

One T cell contributing 1,000 captured UMIs and one melanoma cell contributing 3,000 implies RNA fractions 0.25 and 0.75, although cell fractions are 0.5/0.5. If reliable captured-UMI-per-cell estimates s_k exist, a model-based relative cell fraction is proportional to beta_ik/s_k, renormalized across types. Capture differences, cell size, nucleus versus whole-cell references and cell state undermine naive use of mean scRNA UMI totals as universal conversion factors. The maintainer confirms the RNA units in issues [108](https://github.com/dmcable/spacexr/issues/108#issuecomment-1263553481) and [159](https://github.com/dmcable/spacexr/issues/159#issuecomment-1577218989).

## Assumptions to check

Reference profiles must distinguish the target types and adequately span them. Platform effects are shared across types, so state shifts and type-specific technical effects can remain. Spatial coordinates do not regularize the default likelihood. Low-depth and similar-type mixtures can be unresolved. A high weight or a confident classification is conditional on the available reference and model, not proof that the reference is complete.

Do not use the paper's conditional gene-count allocation as independent single-cell measurements. Attribution uncertainty and shared-effect assumptions persist; the legacy `get_decomposed_data` helper is deprecated. Use a justified downstream inference model and biological replicates.
