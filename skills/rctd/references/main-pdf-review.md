# Main PDF: scientific interpretation and benchmark limits

Directly reviewed the user's 15-page published PDF on 2026-10-31, including all six main figures, Methods, and two appended reporting-summary pages. Read the [article text and source images](paper-sources.md) for exact evidence. The separate 71-page Supplementary Information is now reviewed; see [supplement caveats](supplement-review.md). Page numbers below refer to the supplied PDF.

## What the model estimates

Pages 2 and 11 give the conditional Poisson model with mean `N_i * lambda_ij`; the log rate contains a cell-type profile mixture, spot scaling, gene-specific platform effect and residual variation. The random effects are initially described as Gaussian, then modified for heavier tails using an approximation to a Cauchy–Gaussian mixture. The [supplement mathematical audit](supplement-mathematics.md) records its derivation, printed formula inconsistencies and differences from inspected code.

The paper explicitly describes unobserved proportions of counts, and Figure 3 uses sampled **UMI fractions** as truth. This supports the existing RNA/count-contribution interpretation. Singlet and doublet mean one or two cell types. Figure 3a shows that a smaller minority RNA contribution is harder to detect; a singlet call does not establish physical purity.

Reference means are average normalized expression within an annotated type (p11). The four-stage estimation fits reference profiles, selects genes, calibrates platform effects on spatial pseudobulk, then fits spatial mixtures while treating estimated profiles and platform effects as fixed. This plug-in procedure does not automatically propagate all reference/calibration uncertainty into final assignments.

The paper's model-selection rule maximizes log likelihood minus `V` times type count, with `V=25`; the alternative-pair confidence gap is `delta=10`. It is an AIC-like penalized rule and an ad hoc confidence procedure, not a posterior probability or textbook AIC with a universal penalty. Current API defaults and pair-search implementation differ; use [versions](versions.md).

## Interpret benchmarks with their denominators

| Evidence | What was evaluated | What it does not establish |
|---|---|---|
| Figure 2, pp2–4 | Cerebellum cross-platform snRNA reference → scRNA test; 89.5% classification accuracy among 3,960 single cells | Guaranteed accuracy in melanoma, HD bins or an incomplete reference |
| Figure 3b and Methods | Cell-class identification among confident calls; four pairs of similar types were collapsed into broader classes | The reported 98.2% is not accuracy over every spot at fine cell-type resolution |
| Figure 3c–d and Methods | UMI-proportion prediction and RMSE; Methods states proportion estimation was fitted using the two true contributing types | These proportion errors alone do not evaluate the complete process of identifying unknown types and estimating their fractions |
| Figure 4 | Marker/anatomical concordance without per-pixel ground-truth spatial labels | Independent truth for every label or estimated fraction |
| Figure 5 | Cluster-based interneuron subtype assignment; 25 of 27 reference subtypes represented | Recovery of all 27 subtypes or globally ground-truthed subtype accuracy |

**Source panel-reference inconsistency:** Methods p12 calls proportion estimation “Fig. 3b,c” and class identification “Fig. 3d, top”. The printed figure/caption instead shows b=class accuracy, c=proportion prediction, d=proportion RMSE. Preserve the original text and use visible panels/captions to identify each metric; do not silently change the quoted source.

The reported 97.1% within-cluster agreement concerns confident pixels in presumed single-interneuron spatial clusters, not accuracy against independent cell-level truth. The historical ≥100-UMI simulation result is not a universal reliable-depth threshold. Three/four-type simulations used 10,000 UMIs per pixel. Supplementary Figures 12–13 have now been directly reviewed; their cell-class and conditional-confidence denominators are documented in the supplement guide.

## Cell-type-specific expression and downstream claims

Equation 4 (p12) allocates an observed gene count using the fitted mixture and reference expression:

\[
E[Y_{ikj}\mid\beta,Y_{ij}]
=Y_{ij}\frac{\beta_{ik}\hat\mu_{kj}}
{\sum_{k'}\beta_{ik'}\hat\mu_{k'j}}.
\]

This is a conditional expectation, potentially with large sampling variance, under the strong assumption that the gene-specific residual effects are shared across contributing cell types. It is not directly observed cell-type-specific expression. Do not use allocated counts as independent single-cell measurements or interpret zeros/precision without the allocation uncertainty.

Figure 6 uses local-regression smoothing and downstream spatial tests; this does not put spatial smoothing into the core RCTD mixture likelihood. Environment-associated expression is observational and hypothesis-generating, not demonstrated causal cell–cell signaling. Preserve donor-level replication and use a suitable downstream inference model.

## Input and design details worth retaining

- The Smart-seq2 reference was gene-length normalized following a TPM approach (p12). Prefer raw counts for UMI references; a full-length non-UMI reference requires its own justified linear-scale length normalization and compatible total/QC semantics. This does not authorize log-transformed or integrated residual inputs.
- ROIs were cropped anatomically and spatial spots filtered to at least 100 UMIs. The reporting summary's general “no data excluded” statement must not be used to deny this explicit preprocessing. Record actual ROI/QC attrition.
- The main discussion acknowledges shared-across-types platform effects and missing-reference problems. A missing type can be confidently assigned to a related available type; low confidence is not a reliable out-of-reference detector.
- Subtype analysis first selected confident broad-type pixels, then refit with subtype profiles while constraining broad classes to those already detected. A naive independent second run need not reproduce that procedure.
- The paper's approximately 15-minute, 11,626-pixel benchmark and 4-GB recommendation are historical, dataset-specific observations, not resource guarantees for Visium HD.

Remaining work: execute the R templates in the chosen installed implementation and validate the actual dataset. The supplied supplement is reviewed; the separate Supplementary Table 2 cited by the main article was not included and is still unreviewed.
