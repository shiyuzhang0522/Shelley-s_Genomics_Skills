# Paper and atlas analysis guide

Source: Domínguez Conde, Xu, Jarvis and colleagues, *Cross-tissue immune cell analysis reveals tissue-specific features in humans*, Science 376:eabl5197 (2022), DOI https://doi.org/10.1126/science.abl5197. Page numbers below refer to the supplied 13-page publisher PDF, including its opening research summary. Read the full paper component for exact wording and figures.

## Distinguish the datasets and counts

| Quantity | Meaning |
|---|---|
| 12 deceased adult donors; 16 tissues | Newly profiled donor-matched atlas; not the training-reference breadth |
| 357,211 | High-quality total cells in the new atlas |
| 329,762 | Immune cells within that atlas |
| 19 studies; 20 tissues | Initial curated public reference |
| 32 broad / 91 fine types | Initial high-hierarchy (low resolution) / low-hierarchy (high resolution) model vocabularies |
| 15 broad / 43 fine predictions | Labels resolved in the new data by the corresponding initial classifiers |
| 41 curated types | New-study identities incorporated during the update described in Fig. 5 |
| 101 types/states | Combined updated reference vocabulary, not 101 types independently discovered in the new samples |

Do not conflate all these counts or equate them to present-day model files. Figures and text use multiple annotation stages and some plotted categories include doublets. In the B compartment, 11 plotted categories include two doublet categories; the narrative summarizes nine biological states.

## Scientific contribution across the whole paper

The scientific goal is to compare immune cell identity and tissue adaptation across donor-matched sites, beyond blood-only immunology. CellTypist supplies an initial shared vocabulary, followed by lineage-specific clustering, expert review, marker analysis, external datasets, and experimental validation. The paper is both an immune atlas and an annotation-method study.

The initial immune-focused reference retained broad epithelial, endothelial and fibroblast umbrella labels as fallbacks (supplement p18). Thus immune-focused does not necessarily mean every available model label is immune. These broad classes do not establish comprehensive nonimmune or melanoma-state coverage; inspect each actual model.

- **Figure 1, pp2–4:** Assemble/harmonize reference labels, scale/select features, train L2 logistic regression via mini-batch SGD, predict new cells, and refine with overclustering/majority voting. Broad and fine classifiers distinguish major compartments and finer states. Representation in training affects performance. Reported performance is tied to the tested datasets/splits, not a universal accuracy promise.
- **Figure 2, pp4–6:** Macrophages show strong tissue associations, with alveolar, intestinal and erythrophagocytic programs. Iron-recycling macrophages share features across spleen, liver and some lymph nodes. Migratory DCs express CCR7/LAMP3, with AIRE-associated lymph-node and CRLF2-associated lung states. TNIP3 intermediate macrophages are largely driven by one trauma donor; do not generalize this to a universal healthy population. Validation includes smFISH and immunofluorescence.
- **Figure 3, pp5–6:** B states include progenitors, naive, memory, age-associated B cells (ITGAX/TBX21/FCRL2), germinal-center states, plasmablasts and plasma cells. Quiescent ITGA8/CERCAM plasma cells differ from proliferating plasmablasts. BCR sequencing connects isotype usage, somatic hypermutation and clone distribution; memory clones are broadly distributed while plasma-cell clones are more tissue-restricted. These repertoire conclusions require receptor data, not expression labels alone.
- **Figure 4, pp7–8:** T and innate lymphocyte states span naive/central memory, effector, resident-memory, regulatory, MAIT, gamma-delta, NK and ILC populations. Gut-associated CCR9/ITGAE/ITGA1 states differ from CX3CR1 effector-memory and CRTAM-rich states. ITGAD/CRTAM gamma-delta states receive orthogonal support, but gut gamma-delta identity could not be confirmed by gamma-delta receptor sequencing because samples were unavailable. Shared clonotypes can span states/tissues; this suggests common precursors or transitions but is not direct lineage tracing.
- **Figure 5, p9:** Tissue composition differs across myeloid/B/T compartments. Update the model using curated and externally checked identities, yielding the 101-label reference. This is not unconstrained automatic self-training.
- **Discussion, pp9–10:** Donor matching limits some between-person confounding but does not remove effects of critical illness, tissue procurement, age, sex, activation, assay or dissociation. Disease and spatial applications require their own validation.

## Original methodology in context

The main Methods (p10) report Cell Ranger 6.1.1, Hashsolo demultiplexing, count/gene QC, Scrublet and Scanpy 1.6.0. They explicitly report BBKNN and scVI integration compared with kBET. Do not describe the whole study as uncorrected simply because the CellTypist classifier is not an integration method. Exact QC boolean logic and full model/benchmark settings should be checked in the supplementary methods and scripts, not inferred from abbreviated main prose.

The paper's model uses two rounds of training: choose the top 300 genes by absolute coefficient from each cell type and take their union (3278 genes in the reported run) for the second round. Training-reference scaling parameters and model feature names matter during inference. Reference-label harmonization is a curation process, not a synonym for batch correction; however, the authors used integration to support that curation. It included removal, correction, subdivision and mining of labels, rather than only renaming. Merging matrices, normalization, batch correction, classification and majority voting remain distinct operations.

Supplementary pp18–25 specify an initial 738,647-cell reference, scVI with dataset/protocol covariates for reference integration/curation, and a 75% fine-label cluster-agreement rule with broad-label fallback during label propagation. The reported classifier uses 1000 cells/batch, 100 batches/epoch and 30 epochs, with performance plateau near 10 epochs. Low-hierarchy L2 alpha=1e-4 and high-hierarchy alpha=1e-3 were selected with 10% held-out cells. Classifier expression is normalized to 10,000 counts and log1p transformed with reference gene means/SD reused on query shared genes; p25 explicitly excludes batch-corrected expression from classifier training. Do not confuse this historical random-cell holdout with a modern donor-held-out validation recommendation. The supplement's claim that L2 requires weights > 0 is mathematically incorrect: L2 penalizes squared magnitude and allows negative weights.

The original software citation is CellTypist 0.1.6, Zenodo https://zenodo.org/record/5736560 (main reference 24). The operational guide audits a newer pinned version and explicitly marks differences. Do not present current train() defaults as the original paper's settings.

Supplementary pp28–31 distinguish three thresholds/settings: independent one-versus-rest probabilities use 0.5 for probability matching; query Leiden overclustering uses resolution 25; a 70% cluster vote is illustrated to flag low-consensus groups as Heterogeneous. None equals the 75% reference-label-propagation rule above. Keep individual and voted labels. Current defaults are recorded separately in the software workflow.

The paper benchmark uses 10,000 randomly held-out cells with 5,000/50,000/250,000 reference training subsets, shared HVGs across compared methods, and timing that excludes preprocessing. Read Figs S13–S14 and the detailed method-specific settings before quoting superiority or speed. Query-independent pretrained models and query-dependent procedures have different training/usage costs. Supplementary p31 reports high/low-hierarchy precision 0.97/0.91, recall 0.88/0.84 and F1 0.95/0.89 from the reference validation; the figures summarize per-class metrics (median), so do not calculate a single harmonic mean of the displayed aggregate precision/recall or call these pooled-cell accuracy. Rare types depend strongly on training support.

Tissue enrichment in the main figure captions uses donor-stratified Poisson regression with BH correction, including tissues with >50 lineage-specific cells in at least two donors. Figure 3 B-cell clone plot uses expanded clones >10 cells; Figure 4 receptor-overlap caption uses expanded clones >1 cell; the TCR narrative additionally focuses on clones >20 cells. These thresholds serve different analyses.

## Atlas notebook audit

Primary code: https://github.com/Teichlab/TissueImmuneCellAtlas , pinned commit `49a5441d71e7315eae77d433da702f5b52eb4403` (master). Historical archive cited by paper: https://doi.org/10.5281/zenodo.6334988. The inspected checkout is not asserted byte-identical to that archive.

| Source notebook | Source-confirmed steps and interpretation |
|---|---|
| `TICA_01_doublet_calling.ipynb` | Scrublet plus clustering-based scores and adjusted doublet P values; do not substitute CellTypist scores for doublet detection |
| `TICA_02_5prime_preprocessing.ipynb`, cell 14 | Read 10x matrices, add sample-prefixed barcodes and metadata, compute QC, normalize to 1e4 and log1p; preserve normalized all-gene data in `.raw` |
| `TICA_02_3prime_hashtagged_preprocessing.ipynb` and `TICA_02_5prime_hashtagged_preprocessing.ipynb` | Corresponding preparation for hashtagged protocols; inspect exact sample-specific filters before adapting |
| `TICA_03_integration.ipynb`, cells 15–27, 43–55 | Concatenate prepared datasets, assign chemistry, import doublet scores, exclude adjusted-doublet-P<0.1, and load an existing immune object plus external labels. Despite its name, the saved code cells do not show an executable scVI workflow; an import alone is not integration |
| `TICA_04_myeloid.ipynb`, cells 8–15 | Restore `.raw`, subset myeloid, save `.raw`, select HVGs, scale capped at 10, run BBKNN ridge regression with chemistry as batch and `new_predicted_labels` as confounder, PCA, BBKNN by donor, UMAP and Leiden |
| `TICA_04_myeloid.ipynb`, cells 21–25 and later | Majority votes using existing predicted labels versus Leiden; also resolution 20 overclusters; marker tests and explicitly mapped/manual subdivisions |
| `TICA_05_B.ipynb`, cells 10–17 | Restore all-gene normalized data, subset B, preserve `.raw`, select HVGs and mark immunoglobulin/VDJ list non-HVG, scale, ridge chemistry regression preserving predicted labels, PCA and donor BBKNN |
| `TICA_06_TILC.ipynb`, cells 11–20 | Similar T/ILC workflow; excludes receptor genes from HVG flag and additionally regresses mitochondrial fraction before scaling/integration; repeated subset/manual refinement later |
| `TICA_06_TILC_TCR.ipynb` | Scirpy repertoire workflows and annotation-linked clonotype analyses; requires receptor input and correctly matched cell IDs |

These are exploratory notebooks with hard-coded `/mnt/Science_revision/` paths, external intermediate objects and curation CSVs, some positional `.values` assignments, and inherited annotations. They are evidence of the authors' process, not a standalone rerunnable pipeline. Replace positional transfers with verified barcode joins when adapting. The selected notebook code was statically inspected, not executed on original atlas data. Do not claim an absent notebook step was absent from the study when the paper explicitly reports it.

## Interpretive cautions and source discrepancies

- Model coefficients are discriminative features conditional on the fitted classifier, not causal markers or automatically differential-expression significance.
- A confident classifier can still mislabel an unseen type. Majority voting may improve noisy predictions but erase a rare subtype in a heterogeneous cluster.
- Figure 3F caption states significant isotype contrasts, while adjacent prose says hypermutation did not differ significantly and describes a tendency. Preserve/report this discrepancy rather than selecting the preferred claim without underlying statistics.
- Main body spells an iron-export marker `SCL40A1`, whereas Fig. 2 gives `SLC40A1`; use the verified gene symbol for analysis and note the source typo when quoting.
- RNA CRTAM validation and activation-dependent protein detection are distinct; RNA expression does not guarantee unstimulated surface-protein detection.

## Reusable outputs

Retain automated labels, overcluster assignments, voted labels, curated labels and the evidence for changes as separate fields. Preserve donor/sample/tissue/protocol metadata. Produce sample-wise QC, marker panels, uncertainty summaries, and donor-aware comparisons. Check classifier performance on independently held-out donors/studies before claiming cross-tissue or cross-assay generalization.
