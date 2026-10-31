# Shelley's Genomics Skills

Reusable skills for genomics research, co-created by **Shelley👩‍💻** and **Morgan🤖**.

## 1️⃣ NG_Figure.Skill

**Aim:** Create publication-ready figures for Nature Genetics, with appropriate dimensions, typography, restrained colors, and editable PDF export for Adobe Illustrator and macOS.

**Usage:** Provide your data, an existing figure, or an R/Python plotting script.

> Use $ng-figure to refine this plot for Nature Genetics and export an editable PDF.

[View skill →](skills/ng-figure/SKILL.md)

## Spatial_Transcriptomic_Skills

Skills for spatial transcriptomics and complementary single-cell analyses.

### 2️⃣ SpaCET to gsMap

**Aim:** Estimate malignant, immune, and stromal fractions in tumor spatial transcriptomics, then prepare aligned AnnData inputs for gsMap while preserving raw counts and continuous fractions.

**Usage:** Provide spatial expression counts, coordinates, and sample metadata.

> Use $spacet to deconvolve each tumor section and prepare its outputs for gsMap.

[View skill →](skills/spacet/SKILL.md)

### 3️⃣ gsMap

**Aim:** Integrate spatial gene expression with GWAS summary statistics to identify trait-associated spatial patterns and regions.

**Usage:** Provide a spatial AnnData file, GWAS summary statistics, and compatible reference resources. SpaCET outputs can be prepared using skill 2️⃣.

> Use $gsmap to check my inputs and run a spatial GWAS enrichment analysis.

[View skill →](skills/gsmap/SKILL.md)

### 4️⃣ CellChat

**Aim:** Infer and compare cell–cell communication networks from ligand–receptor expression, including spatial constraints, signaling pathways, and sender/receiver roles.

**Usage:** Provide normalized expression, cell-type annotations, and sample metadata; include calibrated coordinates for spatial analysis.

> Use $cellchat to infer communication networks in my annotated spatial data and compare samples with consistent settings.

[View skill →](skills/cellchat/SKILL.md)

### 5️⃣ NicheNet

**Aim:** Prioritize ligands that may explain a receiver-cell gene-expression program and identify their predicted target genes.

**Usage:** Provide sender/receiver annotations, normalized expression, and a receiver gene set with a suitable background. For spatial data, define plausible sender neighborhoods.

> Use $nichenetr to rank candidate ligands explaining this receiver-cell gene program and extract ligand–target links.

[View skill →](skills/nichenetr/SKILL.md)

### 6️⃣ Visium HD

**Aim:** Plan and audit Visium HD analysis, including bin-level annotation, RCTD, nuclear aggregation and spatial neighborhoods, with explicit checks when adapting the published CRC workflow to melanoma.

**Usage:** Provide raw counts, bin or segmentation details, coordinates, histology and sample/patient metadata.

> Use $visium-hd to plan annotation and spatial analysis for my sections, distinguishing published settings from adaptations.

[View skill →](skills/visium-hd/SKILL.md)

### 7️⃣ CellTypist

**Aim:** Annotate cell types using reference models, assess majority voting and uncertainty, and train custom models with independent-donor validation.

**Usage:** Provide expression data, its normalization state, observation type and reference/model information.

> Use $celltypist to check my model coverage, annotate cells and evaluate uncertain or missing identities.

[View skill →](skills/celltypist/SKILL.md)

### 8️⃣ RCTD

**Aim:** Estimate cell-type RNA contributions from spatial mixtures, choose doublet/full/multi mode, and audit reference coverage, confidence and implementation differences.

**Usage:** Provide raw spatial counts, coordinates, a labeled single-cell reference and the installed spacexr version.

> Use $rctd to select an appropriate mode, prepare my reference and interpret RNA fractions and uncertain assignments.

[View skill →](skills/rctd/SKILL.md)

## Supporting skills and installed inventory

[Paper2Agent](https://github.com/shiyuzhang0522/Agent-Skill-Paper2Agent) supports paper/code review and skill construction. The imported [Google DeepMind science-skills](https://github.com/google-deepmind/science-skills) collection provides database, literature and molecular-analysis tools.

[Installed-skill inventory →](docs/installed-skills.md) records all **48 installed personal skills** checked on **31 October 2026**: eight hosted here and 40 referenced externally. Managed app/plugin skills are outside this personal-skill inventory.

---

**Getting started:** Add the relevant folder from `skills/` to your agent's supported skills directory, preserving its contents, then invoke it as shown above. Required software and datasets must be installed separately.

Sources, validation details, and limitations are documented within each skill.


The three new public editions include authored guidance and supporting code with links to original papers; converted full-text papers and figure/page images are not redistributed. Source-specific licenses and validation limits remain documented within each skill.
