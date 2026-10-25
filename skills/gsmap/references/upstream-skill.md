# gsMap Spatial GWAS Analysis

This skill runs gsMap to perform spatial GWAS enrichment analysis
by integrating spatial transcriptomics with GWAS summary statistics.

Always prefer MCP tools instead of manually writing gsMap shell commands.

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

Always prefer gsmap_quick_mode unless the user explicitly requests
step-by-step control of the pipeline.

______________________________________________________________________

# STEP-BY-STEP PIPELINE TOOLS

Use these tools only when the user requests detailed control
of the gsMap pipeline.

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
args=\[
"--annotation","cell_type",
"--data_layer","count",
"--epochs","200",
"--n_neighbors","15"
\]
)

______________________________________________________________________

# DATA REQUIREMENTS

gsMap requires the following inputs:

- spatial transcriptomics dataset (.h5ad)
- GWAS summary statistics
- gsMap reference resource
- homolog mapping file

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

Use documentation lookup only when necessary.
Prefer running MCP tools directly when the workflow is clear.

