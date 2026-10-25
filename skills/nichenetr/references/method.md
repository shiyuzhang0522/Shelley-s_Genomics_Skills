# NicheNet: source-grounded notes (limited paper coverage)

## paper-notes

# NicheNet: source-grounded method notes

## Coverage and provenance

This is an original concise synthesis, not a transcription of the full paper. The publisher abstract and bibliographic record were accessible; the full article PDF and supplementary files were not retrieved or reviewed. A Paper2Skill verification of these notes establishes faithful packaging of these notes only, not full-paper coverage.

## Original paper

Browaeys R, Saelens W, Saeys Y. NicheNet: modeling intercellular communication by linking ligands to target genes. Nature Methods 17, 159–162 (2020); published online 9 December 2019. DOI: https://doi.org/10.1038/s41592-019-0667-5

NicheNet combines gene expression with prior signaling and gene-regulatory knowledge to propose ligands that may explain a transcriptional response in receiver cells. Its distinguishing goal is to connect extracellular signals to downstream target genes. The paper reports applications to tumor and immune microenvironments. Do not infer experimental proof of a proposed interaction from its predicted score.

## Practical implementation sources

Operational instructions in the parent skill use the authors' public R repository, not unreviewed full-paper methods. Reviewed snapshot: saeyslab/nichenetr commit 66f90d5eeafef280b2b2f339b3fd70ffec1781dd, DESCRIPTION version 2.2.1.1, accessed 2026-10-25.

Source: https://github.com/saeyslab/nichenetr/tree/66f90d5eeafef280b2b2f339b3fd70ffec1781dd

## Version boundary

The current repository tutorials use the v2 prior network and corrected AUPR ranking. Older v1 workflows emphasize Pearson correlation. Package release, prior-model release, and paper publication year are separate provenance fields. Do not describe the current v2 tutorial as an exact reproduction of the 2019 paper.

## Interpretation

Activity scores rank how well prior ligand-target predictions recover the selected receiver program against its background. They are not p-values, direct evidence of physical contact, causal effect sizes, or probabilities that communication occurs in the sample. Regulatory potential is unsigned: the prior alone does not establish activation versus repression.

## Conversion notes

- Only the original synthesized notes are packaged. Full-paper and supplementary-material conversion remains unavailable.
