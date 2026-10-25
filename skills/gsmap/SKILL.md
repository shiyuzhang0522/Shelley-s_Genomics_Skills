---
name: gsmap
description: Run, explain, and troubleshoot gsMap integration of spatial transcriptomics with GWAS summary statistics, including h5ad preparation, gene specificity scores, spatial LDSC, region-level Cauchy tests, and reports. Use for gsMap and spatial GWAS enrichment workflows.
---

# gsMap Spatial GWAS Analysis

This skill runs gsMap to perform spatial GWAS enrichment analysis
by integrating spatial transcriptomics with GWAS summary statistics.

Discover available tools first. Prefer the gsMap MCP tools below when connected. If they are unavailable, use the documented gsmap CLI through the execution environment; never invent or claim to have called unavailable tools.

______________________________________________________________________

# WHEN TO USE THIS SKILL

Use this skill when the user asks about:

- spatial GWAS enrichment
- integrating GWAS with spatial transcriptomics
- identifying trait-relevant cells
- identifying spatial regions associated with traits
- running gsMap analysis
- spatial LDSC analysis using spatial transcriptomics

Example requests:

Run gsMap on this dataset
Analyze spatial GWAS enrichment
Perform spatial transcriptomics GWAS analysis
Identify trait-relevant spatial regions

______________________________________________________________________

# DEFAULT WORKFLOW

Use the MCP tool:

gsmap_quick_mode

This tool automatically runs the full gsMap pipeline:

1. latent spatial representation learning
1. gene spatial score calculation
1. LD score generation
1. spatial LDSC enrichment analysis

Prefer quick mode when its reference resources and defaults fit the analysis. Use the step-by-step workflow for custom references, parameters, or when the user requests detailed control.

______________________________________________________________________

# STEP-BY-STEP PIPELINE TOOLS

Use these tools for detailed control or custom resources.

Pipeline order:

1. gsmap_find_latent_representation
1. gsmap_latent_to_gene
1. gsmap_generate_ldscore
1. gsmap_spatial_ldsc

Typical workflow:

latent representation
→ gene spatial scores
→ LD scores
→ spatial LDSC enrichment

______________________________________________________________________

# PASSING ADDITIONAL CLI PARAMETERS

Many gsMap tools support additional CLI parameters.

If the user specifies additional flags or hyperparameters,
pass them using the `args` parameter.

Example:

gsmap_find_latent_representation(
workdir="output",
sample_name="sample1",
hdf5_path="data.h5ad",
args=[
"--annotation","cell_type",
"--data_layer","count",
"--epochs","200",
"--n_neighbors","15"
]
)

______________________________________________________________________

# DATA REQUIREMENTS

gsMap requires the following inputs:

- spatial transcriptomics dataset (.h5ad)
- GWAS summary statistics
- gsMap reference resource
- homolog mapping file (only for cross-species gene conversion; omit for human ST with human GWAS)

If required resources are missing, download them using:

download_gsmap_resource_data

If the user wants to run a demo analysis or view example inputs, use:

download_example_dataset

______________________________________________________________________

# GWAS SUMMARY STATISTICS FORMAT

Expected GWAS columns:

SNP
A1
A2
Z
N

If the input GWAS file uses different column names,
run:

gsmap_format_sumstats

Additional column mappings can be passed using `args`.

______________________________________________________________________

# DOCUMENTATION LOOKUP

If parameters, flags, GWAS formatting options, or tool usage are unclear,
search the documentation using:

search_gsmap_docs

Examples:

search_gsmap_docs("format_sumstats usage")
search_gsmap_docs("find_latent_representation parameters")

If search_gsmap_docs is unavailable, read the bundled documentation or retrieve official repository documentation. Check the installed CLI help before relying on version-sensitive flags.


## ChatGPT runtime and source provenance

Installed from JianYang-Lab/gsMap, gsmap_vibe/gsmap_skill/SKILL.md,
commit ffb561db3e5a92ddabf7dc7b8f203c25e4d9f627 (retrieved 2026-10-22).
This adaptation adds skill metadata, optional MCP/CLI routing, bundled documentation,
and the correction that homolog conversion is optional for human data.
See references/upstream-skill.md for the unmodified upstream skill and LICENSE for attribution.

Read references/data-format.md for AnnData and GWAS input checks.
Read references/quick-mode.md for the documented end-to-end CLI and resource layout.
Read references/step-by-step.md for custom resources, individual stages, Cauchy combination, and reports.
Treat their mouse examples as examples; do not copy mouse homolog conversion into human analyses.

Before execution, inspect the available environment with command -v gsmap and gsmap --help.
Installing this skill does not install the gsMap Python package, its MCP server, or resource datasets.
If execution dependencies are absent, explain the missing dependency and use the official installation
instructions at https://github.com/JianYang-Lab/gsMap or prepare a script for the user's target environment.
Do not claim an analysis ran from a script alone.

Verify expression layer, spatial coordinates, gene identifiers, annotation column if used, summary-statistic
columns and sample-size meaning, and reference ancestry/genome-build compatibility before launching.
Quick mode's supplied resources use 1000G EUR; inspect custom resource needs before choosing a mode.
Use a fresh output directory if inputs or model settings change, since intermediate outputs may be reused.
For CLI fallback, use gsmap quick_mode or the exact run_* subcommands in the bundled tutorials;
MCP tool names are not interchangeable with CLI subcommand names.

Keep spot-level trait associations distinct from cell abundance, and avoid interpreting association P values
as effect sizes or evidence of causality. Identify mixed-cell spots as such. Preserve patient and section IDs
for multi-sample analyses; spots and repeated sections do not constitute independent patients.
Do not claim cohort-wide replication or robustness without examining actual results.
