# Shelley's Genomics Skills

Reusable skills for genomics research, co-created by **Shelley** and **Morgan (OpenAI ChatGPT)**.

## 1️⃣ NG_Figure.Skill

**Aim:** Create publication-ready figures for Nature Genetics, with appropriate dimensions, typography, restrained colors, and editable PDF export for Adobe Illustrator and macOS.

**Usage:** Provide your data, an existing figure, or an R/Python plotting script.

> Use $ng-figure to refine this plot for Nature Genetics and export an editable PDF.

[View skill →](skills/ng-figure/SKILL.md)

## 2️⃣ SpaCET to gsMap

**Aim:** Estimate malignant, immune, and stromal fractions in tumor spatial transcriptomics, then prepare aligned AnnData inputs for gsMap while preserving raw counts and continuous fractions.

**Usage:** Provide spatial expression counts, coordinates, and sample metadata.

> Use $spacet to deconvolve each tumor section and prepare its outputs for gsMap.

[View skill →](skills/spacet/SKILL.md)

## 3️⃣ gsMap

**Aim:** Integrate spatial gene expression with GWAS summary statistics to identify trait-associated spatial patterns and regions.

**Usage:** Provide a spatial AnnData file, GWAS summary statistics, and compatible reference resources. SpaCET outputs can be prepared using skill 2️⃣.

> Use $gsmap to check my inputs and run a spatial GWAS enrichment analysis.

[View skill →](skills/gsmap/SKILL.md)

---

**Getting started:** Add the relevant folder from `skills/` to your agent's supported skills directory, preserving its contents, then invoke it as shown above. Required software and datasets must be installed separately.

Sources, validation details, and limitations are documented within each skill.
