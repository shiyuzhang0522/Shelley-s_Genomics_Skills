# Method rationale

## What the two papers establish

The 2021 paper introduces an expression- and knowledge-based model of communication, preserving multisubunit ligand/receptor structure and cofactors. It organizes the resulting networks with graph analysis, pattern discovery, and network similarity. Its validation includes consistency, comparisons, and biological/spatial plausibility rather than comprehensive signaling ground truth. Read the Introduction, Overview, Inference of intercellular communications, and Discussion in [the main article](https://pmc.ncbi.nlm.nih.gov/articles/PMC7889871/).

The protocol expands the practical workflow: database choice, inference, network interpretation, comparisons, and troubleshooting. Its detailed procedures concern scRNA-seq; current spatial workflows need the separate repository documentation. It retains the core expression/database model rather than introducing causal inference. Its formal citation is Jin, Plikus & Nie, *Nature Protocols* 20, 180–219 (2025), online 16 September 2024, [DOI](https://doi.org/10.1038/s41596-024-01045-4). The legitimate [NSF full-text copy](https://par.nsf.gov/servlets/purl/10560563) was reviewed; redistribute original notes, not the copyrighted article.

## Operational model at the pinned current v2 source

The following details are grounded in `R/modeling.R`, `R/utilities.R`, and `R/analysis.R` at the commit in sources.md; do not assume historical v1 binaries are identical.

1. Subset normalized expression to signaling genes. Divide by the maximum of that object's signaling matrix, then summarize each gene by cell group. The default trimean is `(Q1 + 2*median + Q3)/4`, not exactly a 25% trimmed mean. Sparse expression can yield zero; quantile interpolation matters at the boundary.
2. Estimate ligand/receptor complexes by geometric means over subunits. A measured zero subunit can zero a complex. An absent feature is a coverage problem, not proof of absent biology.
3. Adjust receptor expression by activating/inhibitory coreceptor terms. Combine ligand and adjusted receptor expression through a saturating Hill function, then apply agonist/antagonist, optional population-size, and (for spatial data) spatial factors.

Let `e[g,i]` denote normalized group expression and `H(x)=x^n/(Kh^n+x^n)`. A compact representation of the current implementation is:

```text
L_i = geometric mean of ligand-subunit expression
R_j = geometric mean of receptor-subunit expression
      × product(1 + activating-coreceptor expression in j)
      / product(1 + inhibitory-coreceptor expression in j)
A_i = product(1 + H(agonist expression in i))
I_i = product(1 - H(antagonist expression in i))
score_ij = H(L_i × R_j) × A_i × A_j × I_i × I_j
           × population_factor × spatial_factor
```

Missing modulation terms equal 1. Population weighting, when enabled, is `(N_i/N)*(N_j/N)`; otherwise it is 1. Nonspatial spatial factor is 1. Defaults include Kh=0.5, n=1, population.size=FALSE. Cofactor products mean the score need not lie in [0,1]. It is not a calibrated probability.

The original paper summarizes cofactors differently in its prose/equation; the current source multiplies individual terms. Use exact installed implementation for run documentation and the papers for rationale.

## Candidate selection and tests

`identifyOverExpressedGenes` selects cell-group markers, not donor-level condition DE. Current fast and slow paths filter nominal `pvalues < thresh.p` even when adjusted values are stored. `do.fast=TRUE` requires presto. Slow/fast fold-change definitions differ; keep backend/thresholds consistent in comparisons.

With `variable.both=TRUE`, both ligand/receptor identities must occur in the selected gene/complex pool. A selected complex requires all subunits represented and at least one selected subunit, not every subunit individually DE. FALSE permits either endpoint selected while both are measurable. This creates the global LR candidate universe, not a claim that each pair is active in every group pair.

For each candidate, cell-group labels are permuted while expression and group counts stay fixed. The current implementation computes:

`p = number of permuted scores strictly greater than observed / nboot`

Zero observed scores are assigned p=1. There is no plus-one correction or automatic multiple-testing adjustment in this calculation. P=0 means no larger score in the finite permutation sample; resolution is limited by nboot. The null is group-label exchangeability, not absence of a causal pathway or a donor-replicated condition effect. Spatial factors are held in the current scoring process; this is not a general spatial-autocorrelation-aware null.

The printed 2021 Methods Eq.3 shows the opposite inequality; flag that discrepancy when discussing exact software behavior, and follow the audited implementation. Do not reproduce the printed inequality as the current test.

## From interactions to networks

| Object or analysis | Meaning | Interpretation boundary |
| --- | --- | --- |
| net$prob / net$pval | Source × target × LR score/test arrays | Model/permutation output, not physical contacts |
| net$count | Number of retained LR edges per group pair | Depends on DB, candidate selection and threshold |
| net$weight | Sum of retained LR scores | Not concentration or number of communicating cells |
| netP$prob | Sum of retained LR scores assigned to each DB pathway | Not receiver-target enrichment |
| Weighted out-/in-degree | Sum of outgoing/incoming network weights | Putative sender/receiver role |
| Other centralities | Graph topology roles | Not intracellular causal intermediates |
| NMF patterns | Coordinated group/pathway network activity | Latent summaries, not independently validated programs |
| Functional similarity | Binary-edge Jaccard under aligned identities | Requires comparable source/target populations |
| Structural similarity | Network-topology similarity | Descriptive even when identities differ |

`computeCommunProbPathway` drops p>threshold, while `aggregateNet` drops p>=threshold. Exact boundary values can yield different outputs. Preserve raw arrays and explain the convention instead of silently altering upstream p-values.

CellChat and NicheNet address complementary questions: CellChat prioritizes plausible LR/group networks; NicheNet evaluates ligands against a receiver transcriptional program. Agreement supports prioritization, but neither proves causality. For melanoma/gsMap, GWAS spatial association and inferred communication are separate evidence layers.
