# Spatial melanoma design

These are added analysis-design recommendations, not claims that the original paper validated this exact melanoma pipeline.

## Data units and replication

For Visium HD, establish whether observations are segmented cells or bins. Check segmentation and annotation confidence. Bins can contain partial or multiple cells; never automatically equate bins with biological cells. Preserve donor, sample, section, region, and condition metadata.

For ordinary Visium, a mixed spot is not a purified sender or receiver. SpaCET fractions describe composition, not cell-type expression. Use a matched single-cell reference, justified expression deconvolution, or an explicitly exploratory spot-level design. Do not manufacture cell-type expression by multiplying spot counts by fractions without a justified measurement model.

Compare the same receiver type across conditions/regions. For example, contrast malignant-cell programs in interface versus interior within donors. Do not default to malignant-versus-immune DE as a communication-induced receiver program. Use donor-level pseudobulk or an appropriate replicated model, preserving pairing. Thousands of bins or sections from one donor do not supply patient replication.

## Sender evidence

Define plausible sender populations using annotation and a justified neighborhood. Record distance units, threshold, section boundaries, and whether spatial restriction preceded candidate selection. Compare neighborhood definitions; never connect unrelated sections. Include receivers as senders only for intentional autocrine analysis.

Standard NicheNet does not model spatial distance. Proximity is additional evidence. Preserve ligand expression by sender type, receptor expression in receivers, and target enrichment separately. Activity cannot uniquely assign a ligand expressed by several sender populations.

## Bridge to gsMap and SpaCET

gsMap supplies trait-associated spatial context; NicheNet tests which ligands may explain a receiver expression program. Define a defensible expression contrast and annotate results with gsMap evidence. Do not pass spot P values or SpaCET fractions as gene expression. GWAS association is not proof of paracrine causality.

If exploring FUMA/MAGMA/gsMap-derived genes, label the analysis a curated gene-set analysis. Restrict to receiver-tested expression and prior coverage, distinguish it from observed downstream response, and retain an independent expression-based analysis where possible. Do not reuse selection evidence as purported independent validation.

## Prioritize hypotheses

Check reproducibility across donors, sender/receptor expression, coherent receiver targets, and independent spatial evidence. Vary detection thresholds, program definitions, background, model version, and candidate scope. Use perturbation or orthogonal experiments to evaluate mechanism.
