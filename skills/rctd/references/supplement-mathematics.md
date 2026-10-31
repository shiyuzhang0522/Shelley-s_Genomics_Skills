# Supplementary Methods: mathematical audit

Reviewed 2026-10-31. Source: user-supplied `41587_2021_830_MOESM1_ESM.pdf`, PDF pages 1–11 (cover, then printed pages 1–10), DOI 10.1038/s41587-021-00830-w. Every page was visually inspected against its source preview; equations (40)–(41) received additional high-resolution inspection. This is an authored interpretation and audit, not a corrected transcription of the authors' supplement. The reading package preserves the printed equations, including their apparent errors, as full-page source images. No numerical RCTD experiment was run for this review.

Code comparisons refer specifically to the previously downloaded dmcable/spacexr revision `9f5dc33c8060f946c6072a138b70e189636e1435`, DESCRIPTION 2.2.1. They do not claim that the paper used this revision or that every other spacexr implementation behaves identically.

Read the [preserved supplement](paper-sources.md) alongside these authored interpretations. For practical decisions, use [supplement caveats](supplement-review.md).

Contents: parameters and units; Poisson approximation; platform normalization; optimization; robust-tail formula; conditional allocation; selection and Table 1; source discrepancies.

## Page coverage and source organization

| PDF page | Printed page | Reviewed content |
|---|---:|---|
| 1 | cover | Nature Portfolio supplementary cover, title and unedited-source notice |
| 2 | 1 | Authors/affiliations; Supplementary Methods; cell-type means; UMI sampling model; equations (1)–(4) |
| 3 | 2 | Predicted probability; multinomial-to-Poisson approximation; role of alpha; equations (5)–(10) |
| 4 | 3 | Gene-set mass and lognormal approximation; platform normalization starts; equations (11)–(14) |
| 5 | 4 | Pseudobulk concentration argument, normalization and estimated platform effect; equations (15)–(20) |
| 6 | 5 | Nonnegative unconstrained-scale weights; integrated likelihood; SQP setup; equations (21)–(27) |
| 7 | 6 | PSD Hessian modification, damping and convergence; gradient; equations (28)–(33) |
| 8 | 7 | Hessian and likelihood derivatives; sigma estimation begins; equations (34)–(37) |
| 9 | 8 | Sigma updates, heavy-tail density and derivative; quantitative concentration bound; equations (38)–(43) |
| 10 | 9 | Conditional UMI allocation; confidence-threshold advice; equations (44)–(49) |
| 11 | 10 | Multi mode, missing-reference experiments; equation (50); Supplementary Table 1 |

Keep PDF pages in source order. Do not move Table 1 away from its page-11 caption or move the continuation of sigma estimation on page 9 ahead of its setup on page 8. Full-page source images are deliberate: equations, explanatory prose and equation numbers remain together. Genuine section-heading text is provided for navigation, not as an attempted equation transcription. Page 11's Table 1 can additionally be exported as a verified CSV; that is a convenience representation of data already retained in the page image.

## Parameters, units and reference estimates

The indices in the intended model are pixel i, cell type k, gene j and UMI n; reference cells additionally use i within each type. Equation (1) is the arithmetic mean of each reference cell's normalized count Y/N, not a pooled-count total divided by pooled UMIs. Therefore each retained reference cell receives equal weight within its type. The estimate is conditional on correct labels, relevant sampling and meaningful positive full-library denominators. More reference cells reduce sampling variability but do not remove donor bias, label errors, state mismatch or systematic selection bias. The source's assertion of accuracy and unbiasedness is model-dependent, not a guarantee supplied by a large cell count alone. `R/processRef.R::get_cell_type_info` implements the mean of column-normalized profiles.

| Quantity | Scientific interpretation / units |
|---|---|
| Y(i,j), N(i) | Observed UMI counts, with N the full measurement library size rather than selected-marker total |
| mu(k,j) | Dimensionless mean relative gene expression within reference type k |
| beta(k,i) | Dimensionless UMI-origin mixture fraction across types, summing to one in the generative description |
| alpha(i), gamma(j), epsilon(i,j) | Natural-log multiplicative factors: pixel scale, shared gene/platform effect, residual gene-by-pixel effect |
| sigma_gamma, sigma_epsilon | Dimensionless Gaussian standard deviations in the initial model; central scale parameters, not finite standard deviations, under the exact inverse-square-tail model |
| w(k,i) = beta(k,i) exp(alpha(i)) | Nonnegative unnormalized RNA-contribution coefficient; sum w = exp(alpha) when beta sums to one |
| lambda-bar(i,j) in equation (21) | Baseline count intensity before the residual multiplier, despite the source calling it a predicted mean |
| delta for confidence; V for complexity | Log-likelihood-gap/penalty units; neither is a probability or percentage |

The paper reuses symbols: beta in (12) denotes a summed log random effect, unlike mixture beta; delta in the Chebyshev bound is a positive tolerance, unlike the model-selection confidence delta; alpha is both pixel scale and SQP/SGD step-size notation. Keep their meanings local. The Table 1 numbers are dataset-specific estimated noise parameters, not universal defaults. With Gaussian epsilon, the unconditional mean under (22) is lambda-bar exp(sigma_epsilon squared / 2), not lambda-bar. Under the exact robust positive log tail, that ordinary unconditional mean does not exist (see below).

The UMI-origin interpretation is particularly important: even perfectly estimated beta is not automatically a physical cell-number fraction. Different types may contribute different captured RNA per cell. Same-type multiple cells can be classified as a singlet type.

## Multinomial derivation and rate-model approximation

Pages 2–3 describe each UMI first selecting a cell type, then selecting a gene. Conditional independence of reads produces a multinomial count vector if the gene probabilities are valid and sum to one (or include a complementary category for unselected genes). A Poisson total with a fixed probability vector yields independent Poisson gene counts *unconditionally* on that total. Replacing its unknown mean by the observed N is a plug-in approximation. Conditioning back on the observed total restores multinomial dependence. The paper's second route uses the rare-category Poisson approximation for large N and small gene probabilities. For a fixed-total multinomial, gene variance is Np(1-p), and cross-gene covariance is −Np_j p_l; independent Poisson counts are an approximation, not an identity at fixed N.

The paper gives N at least 100 and reports that 98.7% of the genes used in one cerebellum prediction have probability below 10^-3. These are motivating conditions in that example, not a general guarantee across selected panels, abundant genes, tissue, technology or depth. At N=100 a Poisson total itself has 10% relative standard deviation; larger counts improve this particular plug-in argument.

There is also a literal probability-normalization limitation: unconstrained lognormal multipliers in equation (3) can produce delta values above one or gene sums above one. A single free alpha cannot enforce exact normalization separately for every cell type's randomly perturbed profile. The source handles total selected-gene mass approximately through alpha rather than specifying an exactly normalized categorical construction. The operational Poisson intensity model is interpretable without requiring those intensities to be exact categorical probabilities. This is a distinction between the motivating derivation and the fitted rate model, not evidence that the software cannot fit data.

## Pixel scale and platform normalization

Equations (11)–(13) use independence of Gaussian gamma and epsilon, their summed variance, and the lognormal mean to approximate a weighted sum over genes. The expectation identity is exact under those assumptions; replacing a realized weighted sum by its expectation requires concentration, dispersed gene weights and enough effectively independent genes. Dominant selected genes or correlated gene effects weaken that approximation. Choosing alpha = −sigma squared / 2 approximately preserves the reference selected-gene mass S_k; leaving alpha free lets overall marker mass change across platforms. It does not make the selected-marker fractions sum to one.

Pseudobulk S_j sums observed counts across pixels. Conditional Poisson additivity supplies (14); shared gamma remains a gene effect. In (15)–(18), residual exp(epsilon) terms are averaged with weights proportional to N_i beta(k,i) exp(alpha_i). Conditional on the fixed weights, independent Gaussian residuals have a finite common mean and variance. The relevant concentration condition is that no small number of large weighted pixels dominate the sum. The text says N_i alpha_i is bounded; the displayed variance actually depends on N_i exp(alpha_i). The former statement alone is insufficient for the displayed argument.

For clarity, under the Gaussian assumptions the reviewer derives

Var(B_kj) = Var(exp(epsilon)) times sum_i [N_i beta_ki exp(alpha_i)]^2 / (I Nbar)^2.

With beta at most one, the page-9 bound is at most max_i[N_i exp(alpha_i)]^2 Var(exp(epsilon)) / (I delta^2 Nbar^2) after applying Chebyshev. The printed denominator is **I delta^2 Nbar^2**, not I squared; the raw text extractor confuses delta and exponents. The bound tends to zero under appropriate boundedness relative to Nbar. A statement for each k,j is not automatically a simultaneous bound over an increasing collection of all genes/types; a union-bound or uniform-control condition would be needed for that stronger claim.

The bulk W weights are nonnegative and free in total scale. They combine UMI-weighted mixture proportions, pixel scaling and the residual expectation. They are not an ordinary unweighted average of spatial cell fractions. Large bulk gene counts support neglecting Poisson sampling when estimating gamma as log observed relative bulk expression minus log fitted relative expression, but zero/low counts and reference-zero predictions require care. The gene/platform factor is assumed common across cell types: type-specific platform distortions or missing target populations may be absorbed into imperfect bulk composition/effect estimates. This is empirical calibration on the target dataset; independently recalibrating arbitrary chunks changes the problem.

The pinned code uses a different bulk objective: `fitBulk` calls `decompose_full(..., bulk_mode=TRUE, constrain=FALSE)`; `get_der_fast` supplies derivatives of squared log prediction minus log observed count. This is not a literal implementation of the supplement's joint Poisson-lognormal W/sigma_gamma MLE. `get_norm_ref` uses normalized fitted bulk proportions and observed bulk expression to form gene-specific rescaling. Current code should be documented from its call path, not reconstructed solely from the historical equations.

## Likelihood, derivatives and optimizer caveats

Equations (21)–(26) integrate the Poisson conditional likelihood over a log-scale random effect and sum gene log likelihoods. Weights have a nonnegativity constraint, without a simplex constraint in this parameterization. With lambda>0, the derivative recurrences in (35)–(36) are mathematically correct:

- Q'_l = [l Q_l − (l+1) Q_(l+1)] / lambda.
- Q''_l = [(l+1)(l+2)Q_(l+2) − 2l(l+1)Q_(l+1) + l(l−1)Q_l] / lambda^2.

The negative-log-likelihood gradient and Hessian signs in (33)–(34) are consistent with differentiating −sum log Q. One subscript in (34) is inconsistent, as recorded below. Boundary lambda=0 needs a limit or numerical handling; these divided expressions should not be applied blindly there.

Pages 6–7 use sequential quadratic programming, replace negative Hessian eigenvalues by zero, solve a nonnegativity-constrained quadratic subproblem, and damp the step by 0.3. The stopping criterion is L1 change in weights below 0.001. The reported stricter-tolerance comparison uses 1,000 sampled cerebellum pixels; the random-start experiment uses 50 pixels and 50 starts each, with maximum L1 error 4.0×10^-6. Those are finite empirical checks, not proof of global convergence, universal convergence, identifiability or biologically correct classification. Small successive changes also do not by themselves certify a stationary point or a well-conditioned solution. The prose claims a local-optimum guarantee without specifying the assumptions that would establish it; fixed damping and curvature modification are not alone such a proof.

Pinned code still uses damping 0.3 and an L1 change criterion with a finite iteration limit, but `psd` floors eigenvalues at 10^-3 rather than exactly zero; `solveWLS` also normalizes curvature/gradient and adds a 10^-7 diagonal ridge. It floors predicted intensities and caps counts at the lookup-table maximum. `calc_Q_all` clamps lambda to the lookup range and uses cubic spline interpolation and derivatives of the stored log-likelihood values; the supplement describes linear interpolation of Q and recurrence-based derivatives. A separate fast linear interpolation helper remains in the code. These are concrete numerical changes, not proof of a scientific failure. Values of the supplied precomputed matrices were not independently regenerated in this review.

The paper initializes sigma at 1, fits 500 pixels, and alternates weight fitting with a stochastic update whose step is 0.0001/n (typically 10 iterations). Its step-sum conditions are standard necessary ingredients in some stochastic-approximation results, but they alone do not prove global minimization of this nonconvex problem. Equation (38) is gradient ascent on log likelihood, while surrounding prose sometimes says minimum. The finite iteration count, stochastic-gradient assumptions, parameter-domain control and other convergence hypotheses matter. Do not promote the paper's global-minimum wording into a user-facing guarantee.

Pinned `choose_sigma_c` instead samples up to the public `N_fit=1000` eligible spots, with depth strictly above `UMI_min_sigma`, initializes a table index 100 corresponding to sigma=1, and alternates fits with a local discrete candidate-sigma search. `chooseSigma` profiles additional overall multipliers 0.8, 0.9, 1.0, 1.1 and 1.2, samples up to one million gene-by-pixel entries, and searches nearby entries on the 0.10–2.00 candidate grid. Public normal mode uses up to eight epochs. This is not the derivative-in-sigma SGD algorithm printed in the supplement. Seed and effective configuration therefore matter.

## Robust-tail formula: source defect and mathematical boundary

Equation (40) visibly prints a Gaussian center and a tail proportional to 1/[sigma(z/sigma−c)^2] for both |z|>3sigma, with c=7/3 and a=(4/9) exp(−9/2)/sqrt(2pi). There is **no absolute value on z/sigma in the printed tail denominator**. These constants join the positive branch continuously and differentiably, but the printed negative branch does not match the center at −3sigma. The pinned code explicitly uses `(abs(x)-c)^2` in `ht_pdf_norm`, producing symmetric tails. Preserve the paper image and explain the difference; do not silently add the missing absolute-value bars in a quotation.

Equation (41) also visibly prints a tail derivative contribution [(-2/sigma^2)/(z/sigma−c)] p_sigma(z). Differentiating the printed tail at fixed z instead gives +2z/[sigma^2(z/sigma−c)] times p, in addition to −p/sigma. Differentiating the symmetric code tail gives +2|z|/[sigma^2(|z|/sigma−c)] times p. This explicit reviewer derivation shows a sign/factor inconsistency in the source, independently of the absolute-value issue. It does not establish what historical executed code used. Current pinned sigma selection does not use this printed derivative.

The source calls inverse-square tails almost as heavy as possible. Integrability only requires sufficiently faster-than-inverse-first-power decay; there are valid heavier tails than inverse square. More consequentially, under either printed or symmetric inverse-square **positive log-effect** tails, E[exp(epsilon)] and E[exp(2epsilon)] diverge. Thus the preceding Gaussian lognormal expectation and finite-variance Chebyshev proof do not transfer literally to that exact robust distribution. Sigma under the symmetric inverse-square model is a scale parameter; its ordinary variance is infinite. This is the reviewer's mathematical inference about the idealized distribution, not a result claimed by the paper, and not a runtime-failure claim. The per-count mixture probability Q_l remains finite, since it integrates a bounded Poisson probability against a proper mixing density. Numerical `get_Q` in the pinned code uses finite quadrature over log effects −20 to 20 at spacing 0.004, adding a further approximation; it was not executed or used to regenerate distributed tables here.

## Conditional expression allocation and its limits

Equations (44)–(49) derive a type-origin probability for a UMI of gene j proportional to beta_ki mu_kj. Shared alpha_i, gamma_j and epsilon_ij cancel across cell types in the Bayes ratio. The resulting expected type-specific count is observed Y_ij times that normalized ratio. This is an allocation conditional on fitted mixture weights and the reference profiles; it does not measure independent cell-type-specific expression directly. Cancellation depends on the multiplicative effect being shared across types. A genuine type-specific platform effect or state change does not cancel in the same way. The tower-law argument is valid because the conditional ratio is constant in the canceled effects; it does not propagate uncertainty in estimated beta or mu.

The denominator must be positive for the basic formula to be defined. The pinned helper `decompose_doublet_fast` adds epsilon=10^-10 and splits this tiny regularizer symmetrically between two types. It returns expectations and a conditional binomial variance. Neither the regularized helper nor the algebra turns allocated counts into independent observations appropriate for naive cell-type differential-expression testing.

## Selection, missing types and Table 1

Page 10 recommends exploring confidence delta, with the historical value 10: lower it if plausible results are rarely confident, increase it if inaccurate. It explicitly supplies no quantitative procedure guaranteeing a target classification accuracy without ground truth. Marker agreement and spatial priors are heuristics and should not be presented as independent ground truth when the same markers fitted the model.

Page 11's multi mode greedily adds the best next type and balances fit against V times the number of selected types, with historical V=25. This is an AIC-like criterion on a log-likelihood scale; it is not standard AIC with the usual fixed parameter penalty. Greedy selection does not guarantee the best subset over all possible combinations. The pinned code adds preliminary candidates only when unrestricted weights exceed 0.01, stops when improvement falls short of the configured penalty, and caps selected types. Confidence uses one-at-a-time substitutions among remaining candidates, not exhaustive posterior support for every mixture. The public pinned defaults are confidence 5 and complexity 20; lower-level helpers still display 10 and 25. Do not substitute the supplement's historical defaults for the installed public configuration.

The missing-reference experiments remove named cerebellar types, first one member of each related class and then both members. The paper reports that missing types often map to the available related type. That supports a practical coverage warning; it does not claim reliable open-set discovery or calibrated rejection of unknown types. Preserve distinctions between missing related subtypes and removal of an entire class.

Supplementary Table 1, verified visually, reports:

| Target dataset | sigma_gamma | sigma_epsilon |
|---|---:|---:|
| snRNA-seq Cerebellum | 0 | 0.77 |
| scRNA-seq Cerebellum | 1.28 | 0.88 |
| Slide-seq Cerebellum from snRNA-seq | 0.94 | 0.95 |
| Slide-seq Hippocampus | 0.51 | 0.80 |
| Visium Hippocampus | 0.70 | 0.45 |
| Slide-seq Cerebellum from scRNA-seq | 0.61 | 0.76 |
| Slide-seq Somatosensory Cortex (from Smart-seq2) | 1.36 | 0.52 |

## Source discrepancies retained rather than repaired

| Location | Visible source issue | Reviewer interpretation / limitation |
|---|---|---|
| p2 text above (1) | Refers to gene i and cell type j, although the equation uses k,j | Intended gene j, type k follows the equation and subsequent definitions |
| p2 final paragraph | Platform effect printed as lambda_j, though (3) defines gamma_j | Notation typo; retained in image |
| p3 (5) | Predicted probability sum uses beta_i,k mu_k,j and omits the delta factors from (2)–(3) | Inconsistent with the preceding perturbed gene probabilities; do not silently replace with a repaired equation |
| p4 before (12) | Subset expression is printed mu-hat_k,j identically S_k<1, without the sum needed by its prose meaning | S_k is the selected-gene mass in the surrounding argument |
| p4 platform opening | Platform effects printed gamma_i instead of gamma_j | Gene-index mismatch |
| p5 below (15) | beta_0 defined as E[epsilon_i,j]=exp(sigma_epsilon^2/2) | The stated value belongs to E[exp(epsilon)], not the zero-mean Gaussian epsilon |
| p5 (19) | Multiplicative factor printed exp(gamma_i) within gene-j calculation | Index inconsistency |
| p5 and p9 prose | Assumes N_i alpha_i bounded | Concentration expression depends on N_i exp(alpha_i), requiring stronger/different control |
| p6 (24) | Last Q argument carries lambda-bar_i after gene-j expressions | Index inconsistency |
| p8 (34) | A Q-prime subscript changes from Y_j to Y_i inside Hessian expression | Index inconsistency; derivative structure otherwise checks |
| p8–9 optimizer prose | Alternating maximization said to reach a local minimum; ascent step called global-minimum convergence | Objective-sign language and unsupported general guarantee |
| p9 (40)–(41) | Tail absolute-value omission and derivative sign/factor issue | Detailed independent derivation above; code uses symmetric tail |
| p9 end | Refers to beta_k,j rather than B_k,j when discussing deviation | Notation mismatch |
| p10 explanatory Bayes sentence | Gene i/type j/sample k wording conflicts with i=pixel,k=type,j=gene | Intended meaning recoverable from (46)–(48) |
| p10 (49) | Summation visibly uses i=1 to I while indicator indexes UMI n; conditional term uses Y_i,k | The UMI-count sum should range over UMIs and condition on gene counts; preserve the printed equation and label interpretation separately |

The page images are the authoritative source evidence for these defects. Raw PDF extraction loses signs, Greek letters, summation layout and superscripts and is not safe to reuse as source mathematics.
