# CellTypist software workflow

## Contents
- [Source and scope](#source-and-scope)
- [Input contract](#input-contract)
- [Model logic](#model-logic)
- [Annotation](#annotation)
- [Majority voting](#majority-voting)
- [Custom training](#custom-training)
- [Validation and interpretation](#validation-and-interpretation)
- [Melanoma and Visium HD adaptation](#melanoma-and-visium-hd-adaptation)
- [Version-specific traps](#version-specific-traps)

## Source and scope

This reference describes official CellTypist **1.7.1**, commit `fe357564a6625d3b1732a022fd39f18e55696e80`, inspected 2026-10-29. It is not a claim that the 2022 paper used every current option. The paper's method emphasizes SGD and mini-batches; current `train()` defaults to conventional logistic regression. Model files evolve separately from package versions: record model filename, SHA-256, model description, label list, feature list, source, and download date.

Primary sources, all pinned:

- [README and usage](https://github.com/Teichlab/celltypist/blob/fe357564a6625d3b1732a022fd39f18e55696e80/README.md)
- [train.py](https://github.com/Teichlab/celltypist/blob/fe357564a6625d3b1732a022fd39f18e55696e80/celltypist/train.py)
- [classifier.py](https://github.com/Teichlab/celltypist/blob/fe357564a6625d3b1732a022fd39f18e55696e80/celltypist/classifier.py)
- [models.py](https://github.com/Teichlab/celltypist/blob/fe357564a6625d3b1732a022fd39f18e55696e80/celltypist/models.py)
- [annotate.py](https://github.com/Teichlab/celltypist/blob/fe357564a6625d3b1732a022fd39f18e55696e80/celltypist/annotate.py)
- [CLI](https://github.com/Teichlab/celltypist/blob/fe357564a6625d3b1732a022fd39f18e55696e80/celltypist/command_line.py)
- [large-dataset tutorial](https://github.com/Teichlab/celltypist/blob/fe357564a6625d3b1732a022fd39f18e55696e80/docs/notebook/celltypist_tutorial_cv.ipynb)
- [change history](https://github.com/Teichlab/celltypist/blob/fe357564a6625d3b1732a022fd39f18e55696e80/CHANGELOG.md)

The implementation is MIT-licensed. This reference summarizes and links source; no pretrained model or source code is bundled here. Consult the package's LICENSE before redistribution of its code. Install only trusted pickle models because model loading deserializes Python objects.

## Input contract

| Input | Expected expression | Processing |
|---|---|---|
| CSV/TXT/TSV/TAB/MTX path | Raw read/UMI counts | CellTypist normalizes each cell to 10,000 then natural-log1p transforms |
| AnnData or H5AD | `log1p(count / cell_total * 10000)` | It applies reference scaling; do not pre-z-score input |
| Array/DataFrame for `train()` | Already log1p normalized to 10,000 | Supply matching labels and, for arrays, genes |

Use cells as rows and genes as columns. For gene-by-cell text/MTX, explicitly request `transpose_input=True`; do not rely on heuristic auto-transpose. Annotation MTX needs one gene name per line and one cell barcode per line, in exact matrix order. A raw 10x `features.tsv` with several columns is not automatically the required one-column gene-symbol file; extract the correct column or read the matrix through Scanpy first.

Keep all measured genes through normalization and preferably annotation. Do not pass only variable genes, PCA embeddings, integrated expression, Pearson residuals, Seurat scale.data or SCT residuals as the classifier matrix. Preserve raw counts separately. Do not normalize or log again if the object already has the required transformation. Remove empty cells and verify finite nonnegative values before transforming.

Match species and identifiers to `model.features`. Models commonly use gene symbols; reconcile Ensembl IDs with an explicit, versioned mapping and resolve duplicates before running. Making duplicate symbols unique with suffixes prevents exact matching for those suffixed genes; this is not a biological resolution of duplicates. Never pad unmeasured genes with zeros as though they were genuinely measured and absent. Record the count and fraction of model features observed. The classifier accepts any nonzero feature overlap; that is not a scientific adequacy threshold.

Read `classifier.py:267-331` carefully when input layers are ambiguous. `.X` is checked first; `.raw.X` is used only if `.X` fails its range check. The code checks the first 1000 rows for range and only the first row for the approximate sum of 10,000 after expm1; these are sanity checks, not comprehensive validation. AnnData prediction can warn rather than fail on a wrong total. Training fallback to `.raw` is triggered by negative values in `.X`, so do not rely on the same fallback behavior across training and prediction. Build an explicit classifier AnnData with the correct full-gene matrix instead.

## Model logic

For type k and a cell's log-normalized gene expression x:

1. Use the reference scaler: `z_g = (x_g - reference_mean_g) / reference_sd_g` when `with_mean=True`; skip subtraction otherwise.
2. Cap values above 10; the source does not symmetrically clip below -10.
3. Compute `s_k = intercept_k + sum_g(weight_kg * z_g)` using overlapping genes.
4. Report `p_k = sigmoid(s_k)`.

The CPU logistic classifiers use one-versus-rest classification. Positive and negative coefficients are informative; top markers are model-discriminative features, not causal genes. The probabilities for multiple types are independent sigmoid transforms and **need not sum to one**. They are neither deconvolution fractions nor guaranteed calibrated posterior probabilities in a new tissue or platform.

`mode='best match'` returns the class with the largest decision score for every cell, including cells unlike all reference classes. `mode='prob match'` selects all types with `p_k > p_thres` (strict greater-than; default 0.5), yielding zero, one, or several labels separated by `|`. Zero labels is intended to become `Unassigned`; see the string-truncation trap below. Multiple passing labels are not proof of a physical doublet. No passing labels is not proof of a new cell type.

## Annotation

Choose a biologically suitable model after inspecting its training scope and labels. `Immune_All_Low.pkl` is the fine-grained immune model and `Immune_All_High.pkl` is the coarser immune model; "Low" and "High" refer to annotation hierarchy, not model quality. Do not silently accept the default immune model for a whole tumor.

```python
from pathlib import Path
import celltypist
from celltypist import models
import scanpy as sc

# Only if this model is appropriate for the biological compartment.
models.download_models(model='Immune_All_Low.pkl')
model = models.Model.load('Immune_All_Low.pkl')
print(model.description)
print(model.cell_types)
print(len(model.features))

# Prepared beforehand with full-gene log1p normalization to 10,000.
adata = sc.read_h5ad('query_log1p_10k.h5ad')
pred = celltypist.annotate(adata.copy(), model=model, majority_voting=False)
out = Path('celltypist_results')
out.mkdir(exist_ok=True)
pred.to_table(str(out), prefix='query_')
annotated = pred.to_adata(insert_labels=True, insert_conf=True)
annotated.write_h5ad(out / 'query_annotated.h5ad')
```

Keep `predicted_labels`, `decision_matrix`, and `probability_matrix`. `to_adata()` adds labels and confidence but its default confidence is row-maximum probability corresponding to the initial prediction. If using majority-voting labels, explicitly set `insert_conf_by='majority_voting'`; it uses the probability for the voted label when available, with row-maximum fallback for special labels. Do not mistake this fallback for confidence that a cell is truly unknown or heterogeneous.

For input known to contain raw counts, prepare a clean AnnData copy with `sc.pp.normalize_total(..., target_sum=1e4)` followed by `sc.pp.log1p(...)`; retain raw counts and sample/cell IDs elsewhere. When joining annotations back to the original object, join by unique sample-prefixed barcode, never by assumed row order after filtering.

CLI example (create the destination first):

```bash
mkdir -p celltypist_results
celltypist --indata query_log1p_10k.h5ad \
  --model /absolute/path/selected_model.pkl \
  --outdir celltypist_results --prefix query_
```

CLI modes are `best_match` and `prob_match`; Python modes contain spaces. An absolute local model path supports offline use in this version. Download selected models beforehand; do not force-update production model files during an analysis.

## Majority voting

Voting is optional and **off by default**. It does not train a new classifier. It assigns every cell in each overcluster its most frequent initial label. `min_prop` sets the required fraction supporting this label; lower support becomes `Heterogeneous`. Default `min_prop=0` means the most frequent label wins even without a strict >50% majority. It does not average probabilities or update the decision/probability matrices.

```python
pred = celltypist.annotate(
    adata.copy(), model='/absolute/path/selected_model.pkl',
    majority_voting=True, over_clustering='fine_cluster', min_prop=0.6,
)
# 0.6 is an illustrative analysis choice, not the paper/software default.
```

`fine_cluster` must exist in `.obs`; alternatively pass a correctly ordered label array or one-label-per-line file. A mislabeled column name can be interpreted as a file path. Preserve exact barcode order and review cluster size and purity. In v1.7.1, annotation skips voting for <=50 cells even when an explicit overclustering is provided.

Without supplied clusters, the source uses Leiden on an existing connectivity graph, or constructs one using up to 2500 highly variable genes, 50 PCs and 10 neighbors. Default Leiden resolutions rise with cell count: 5 (<5000), 10 (<20000), 15 (<40000), 20 (<100000), 25 (<200000), and 30 otherwise. These are heuristics, not universally appropriate settings; tiny feature sets can fail the fixed 50-PC graph path. Existing PCA/neighbors can come from a different analysis, so record their provenance. Voting can use deliberately batch-corrected embedding-derived clusters while classifier expression stays log-normalized; the two roles must be separated and validated.

Compare raw predictions with voting: voting can remove isolated mislabels but can also erase rare populations in heterogeneous clusters or propagate a systematic error. Never vote by whole tissue region or broad immune compartment merely because a region has one dominant type. If a global multisection object uses per-sample cluster numbers, prefix cluster IDs with sample IDs before supplying them so unrelated clusters numbered "0" are not pooled.

## Custom training

Required inputs are a reviewed reference cell-by-gene expression matrix, matching cell labels, species/identifier mapping, donor/study metadata, and a planned independent validation split. Harmonizing cell-type label names is a curation operation, not batch correction. Preserve a mapping from original to harmonized labels and evidence for relabeling or exclusions.

```python
import numpy as np
import celltypist

# ref is an AnnData with full-gene log1p-10k expression and curated labels.
np.random.seed(42)  # Needed for mini-batch sampling's global numpy RNG.
model = celltypist.train(
    ref, labels='cell_type',
    feature_selection=True, top_genes=300,
    use_SGD=False, max_iter=1000, n_jobs=4, random_state=42,
    details='Curated reference; see separately saved donor split and label map',
    source='Reference accession and processing release',
    version='analysis-specific version',
)
model.write('custom_reference.pkl')
```

This illustrates current API usage, not a literal reproduction of the paper's training parameters. `top_genes` must be less than the number of retained expressed genes. For a small synthetic demonstration choose fewer features. The two-pass feature selection first fits SGD, takes the union of the largest absolute coefficients per type (default 300 per classifier row), then fits the selected training algorithm to those genes. Scaler parameters are subset from the first scaling pass, not relearned on query data.

Current defaults: `use_SGD=False`, `mini_batch=False`, `feature_selection=False`, `with_mean=True`, `C=1`, `alpha=0.0001`. The default CPU solver is lbfgs through 50,000 cells and sag above that. Automatic `max_iter` is 1000 below 50,000 cells, 500 below 500,000, and 200 otherwise. These are computational defaults rather than convergence guarantees.

For SGD, set `use_SGD=True`; `alpha` is L2 strength. For very large data, optionally also set `mini_batch=True`, tune `batch_size`, `batch_number`, `epochs`, and `balance_cell_type`. Defaults are 1000 cells/batch, 100 batches/epoch and 10 epochs. Each epoch samples without replacement up to `min(batch_number*batch_size, n_cells)`; cells can reappear across epochs. Balanced sampling increases rare-type selection probability but cannot create more distinct rare cells within an epoch. `n_jobs` does not provide mini-batch parallel training. Set both `np.random.seed` and classifier `random_state` for reproducibility.

The default centered scaling densifies sparse training input and can dominate memory before mini-batching. Estimate RAM from cells × genes × dtype size plus working copies. `with_mean=False` can preserve sparsity, changing model preprocessing; record and validate the tradeoff. Feature selection, representative reference downsampling and explicit thread limits can help. Downsampling should preserve donor/tissue/type diversity rather than simply cap a heterogeneous broad label.

## Validation and interpretation

Hold out donors or complete studies before selecting genes, fitting the scaler, or tuning parameters. Random cell splits from the same donor can overstate transfer performance. Check per-type precision/recall/F1, macro averages, confusion matrices, rare populations, reference-absent types and probability behavior. Keep independent validation labels separate from predictions and avoid retraining on unreviewed pseudo-labels.

Validate label assignments with marker combinations, absence of incompatible markers, morphology/spatial context where available, and concordance across samples. Inspect ambiguous/low-support groups manually. Neither a confident label nor high cluster agreement proves biological correctness. Do not declare automatic novel-cell discovery from `Unassigned`.

Deliver per-cell/barcode predictions, voted labels when used, uncertainty flags with criteria, sample-level composition summaries, overlap statistics, model checksum, normalization recipe, software/environment versions, graph provenance, seeds and label-map decisions. Use patients/samples as experimental units when making biological comparisons; many cells/bins do not create independent patient replication.

## Melanoma and Visium HD adaptation

The original paper is a cross-tissue immune study, not validation of a pan-melanoma or spatial-bin classifier. Treat these as adaptations:

- For whole melanoma tissue, first identify broad compartments with appropriate evidence or a broad reference. Use immune models within supported immune compartments. Some immune models include broad nonimmune fallback labels: the paper's initial reference retained epithelial, endothelial and fibroblast umbrella classes (supplementp18). Such fallback labels do not constitute comprehensive stromal/tumor subtyping or establish melanoma malignancy; inspect the actual model vocabulary and training scope.
- For custom melanoma models, obtain dissociated scRNA-seq count matrices with per-cell labels and donor metadata, match labels to exact sample/barcode IDs, curate the ontology, and validate across held-out patients/studies. Tumor states and treatment effects can be patient-specific. Do not equate melanocytic identity with malignancy; assess malignancy independently using suitable biological evidence.
- Cell/nucleus-segmented HD profiles are closer to single-cell inputs but require segmentation, contamination, count-depth and gene-overlap assessment. An 8 µm square may mix cells. A classifier label describes the best-supported expression identity and cannot yield cell fractions or prove that a bin contains one cell.
- RCTD deconvolves mixtures given reference profiles; CellTypist classifies expression profiles. Multiple CellTypist labels or independent sigmoid scores are not RCTD proportions. Keep the unit of each result explicit.
- For three samples, apply one frozen model and consistent preprocessing to each, retain sample identity, and evaluate sample-specific failures. Joint clustering can help harmonize names, but is not mandatory and does not itself remove batch effects. Integration decisions should follow diagnostics and biological confounding, not a blanket requirement to reproduce the CRC paper.

## Version-specific traps

1. **scikit-learn compatibility.** v1.7.1 passes `multi_class='ovr'` to `LogisticRegression`. A local constructor check with scikit-learn 1.8.0 raises `TypeError` because that parameter has been removed. The package declares only a lower sklearn bound, so unrestricted installation may select incompatible versions. A synthetic training/annotation test succeeded with sklearn 1.5.2, Scanpy 1.11.1, AnnData 0.11.4, numpy 2.3.5 and pandas 2.2.3. Prefer a fresh pinned environment and record its full lock/freeze; do not assume all newer dependency combinations work. This is one tested combination, not an exhaustive compatibility claim.
2. **Truncated unknown label.** `models.py:159-162` constructs a fixed-width numpy string array before assigning `Unassigned`. When every cell has no passing class, the array can have width 1 and output `U`; shorter longest labels can similarly truncate the intended word. Reproduced on a synthetic model using `p_thres=1`, which deliberately makes all probabilities fail the strict threshold. Derive the unknown mask from probabilities and repair output to object/string dtype before downstream use; do not use string equality alone.

```python
threshold = 0.5
pred = celltypist.annotate(adata.copy(), model=model,
                          mode='prob match', p_thres=threshold,
                          majority_voting=False)
labels = pred.predicted_labels['predicted_labels'].astype(object)
labels.loc[~pred.probability_matrix.gt(threshold).any(axis=1)] = 'Unassigned'
pred.predicted_labels['predicted_labels'] = labels.astype('category')
```

3. **Model mutation and memory.** Prediction temporarily subsets coefficients to overlapping genes and then restores them. Load a separate model per worker rather than sharing one mutable model across concurrent threads. Prediction may densify centered sparse matrices. Batch independent cell predictions if needed, but run intended global or within-sample majority voting after collecting predictions, not arbitrarily within computational chunks.
4. **Harmonization versus integration.** The software history says the later CellHint functionality was split out in v1.6.0. Do not infer that current CellTypist classification automatically harmonizes label vocabularies or performs batch integration.

Implementation checks performed: actual synthetic 180-cell/90-gene training and held-out 90-cell prediction for conventional LR, SGD and mini-batch SGD, each with two-pass feature selection; model save/reload; supplied-cluster majority voting; sigmoid/probability consistency; table and H5AD output; probability-threshold unknown handling; and CLI with a local model. Synthetic separated classes yielded 100% accuracy in these runs; this only verifies exercised implementation paths and is not a biological benchmark. Downloaded public models, automatic Leiden graph construction, GPU mode, whole melanoma and Visium HD data were not tested.
