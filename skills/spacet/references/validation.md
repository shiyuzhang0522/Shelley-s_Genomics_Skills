# Biological validation and interpretation

Check output completeness, finite fraction ranges and the parent/child hierarchy. Do not require all propMat rows to sum to one: it repeats broad parents and their children. Inspect the mutually exclusive major level plus Unidentifiable separately. Do not renormalize all categories to force a sum.

For each sample report before/after QC spot counts, library size and detected genes, retained fraction categories, Unidentifiable distribution, dominance/margin distributions, label counts and the spots gsMap would exclude. Investigate high unknown fractions jointly with coverage, tissue morphology and missing references; unknown is not a synonym for malignant or empty.

Compare inferred malignant areas to H&E or expert annotations and multiple lineage markers. Melanoma differentiation markers can vary by state; use panels and orthogonal evidence rather than declaring a single marker definitive. Immune sublineages require stronger evidence than broad lineage separation. Regional histology agreement does not establish exact fractions in every spot.

The 2023 paper describes a malignant-first dictionary approach, hierarchical immune/stromal deconvolution and spatial interaction inference. It evaluates simulations and eight real tumor ST datasets across seven cancer types. Melanoma scRNA profiles are present in the simulation/reference collection; this is not equivalent to a melanoma Visium HD validation dataset. Related sublineages remained harder to resolve. See the paper DOI in sources.md.

For independent per-sample deconvolution there is no user-created integrated embedding to evaluate with batch-mixing metrics. Explain this distinction to a reviewer and provide appropriate per-sample validation and cross-sample consistency instead. Do not claim such checks alone answer every concern about technical effects or rare populations.

Use a consistent broad-lineage policy across sections. Sensitivity analyses may compare broad labels, reviewed finer labels and supported no-annotation gsMap stages, using separate output directories. Record changes in included spots and model settings. Do not choose annotation thresholds based on which gives the smallest GWAS P value.

Spots/bins are spatially dependent and repeated sections can share patients. Preserve nesting in metadata and distinguish exploratory spatial enrichment from independent biological replication. Cauchy aggregation over spots is not a patient-level effect-size meta-analysis. Fraction–significance correlations are confounded by mixtures, coverage and spatial structure; they are not automatically causal or cell-specific genetic effects.

Visium HD binning and segmentation have different observation units. Do not mix resolutions in one sample's graph, infer ancestry from tissue location, or assume all bins are single cells. The bridge preserves physical coordinates but does not supply image registration or H&E segmentation.
