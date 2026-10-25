# gsMap handoff

Use the existing gsmap skill for full installation, resource, GWAS and pipeline guidance. The bridge supplies gene expression, coordinates and optional composition-derived labels; it does not supply GWAS or LD resources.

At source commit `ffb561db3e5a92ddabf7dc7b8f203c25e4d9f627`:

- `find_latent_representation.py` drops null annotations and classes with fewer than 30 observations when an annotation is supplied. Those labels are encoded for model training.
- `latent_to_gene.py` constrains spatial neighborhoods by annotation and removes nulls when using an annotation.
- `config.py` makes annotation required for `RunAllModeConfig` (quick mode), but optional for individual latent/gene-score configs. Do not pass the string `None` as a substitute for omission.
- Preprocessing expects counts in a selected layer; it normalizes/log-transforms its working matrix internally. The bridge stores raw counts in both X and `layers['count']` so early gene filtering also sees counts.
- Quick resources use 1000G EUR and a Gencode v46 gene annotation lifted to GRCh37. Verify GWAS variant identifiers/build and any custom resources. Human ST with human GWAS needs no mouse homolog file.

## Annotated quick-mode example

Only run after choosing/validating `gsmap_annotation`, inspecting the bridge audit and checking resource compatibility:

```bash
gsmap --help
gsmap quick_mode --help
gsmap quick_mode \
  --workdir /path/to/new/sample01_major_run \
  --sample_name sample01 \
  --gsMap_resource_dir /path/to/gsMap_resource \
  --hdf5_path /path/to/sample01.major.h5ad \
  --annotation gsmap_annotation \
  --data_layer count \
  --sumstats_file /path/to/CM.sumstats.gz \
  --trait_name CM
```

GWAS inputs commonly include SNP, A1, A2, Z and N. Confirm allele alignment and the meaning of N, especially for case–control data, using the actual summary-statistic provenance and current gsMap documentation. Never manufacture N or convert P to signed Z without a verified direction.

## Unannotated or sensitivity mode

The bridge default produces no gsMap labels. This is intentional. Use the step-by-step `run_find_latent_representations` and `run_latent_to_gene` commands without `--annotation` when supported by installed help, followed by resource-specific LD score and spatial LDSC stages. Read the existing gsmap step-by-step reference for exact resource paths. Annotation-based report/combination stages have their own requirements; do not promise a full quick-mode report with no labels.

Keep all fractions and descriptive dominance in the input for later interpretation. Do not turn uncertain spots into a single biological Mixed class solely to satisfy quick-mode arguments. Reviewed broad tissue-region labels are an alternative if they have independent support and their role in modelling is understood.

gsMap can filter additional genes/spots internally. After execution compare output obs_names and LDSC spot IDs with the bridge input; report actual retained counts, not only predictions from the 30-spot annotation rule. Use new work directories when counts, QC or labels change because intermediate results can be reused. Retain a sample/patient/section manifest across runs.

Annotation eligibility is not model-readiness validation. Quick mode defaults to `n_comps=300`; confirm the selected PCA dimension is compatible with retained observations and available variable genes. Tiny synthetic bridge fixtures test formatting and identity, not model training. Also verify neighbor counts, resource capacity, and gene overlap for the actual dataset.
