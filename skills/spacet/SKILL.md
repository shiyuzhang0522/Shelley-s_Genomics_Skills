---
name: spacet
description: Run, explain, and troubleshoot SpaCET tumor spatial transcriptomics deconvolution and bridge per-sample outputs to gsMap. Use for Visium or Visium HD melanoma analysis, malignant and immune/stromal fractions, major-lineage labels, barcode alignment, sample metadata, custom references, and optional spatial interactions.
---

# SpaCET to gsMap

Analyze each tissue section separately with the upstream R package. Preserve continuous fractions and raw retained-gene expression. A dominant lineage summarizes a mixed spot; it is not a single-cell identity. Never replace gene expression with fraction estimates.

## Intake and source checks

Inspect files and existing results before asking for missing inputs. Record sample, patient, section, organism, cancer type, platform, observation unit (spot/bin/cell), and HD bin size. Mark unknown metadata explicitly; do not infer donor ancestry from country or laboratory.

Read [workflow](references/workflow.md) for upstream R calls, [bridge](references/bridge.md) for export/conversion, [validation](references/validation.md) for interpretation, and [gsMap handoff](references/gsmap-handoff.md) for downstream choices. Consult [sources](references/sources.md) for exact source versions and tested scope.

Inspect R/SpaCET and `gsmap --help` before execution. Skill installation does not install these packages, an MCP server, GWAS data, or LD resources. Use isolated environments or provide code for the user's chosen environment when dependencies are absent. Distinguish prepared code from completed analysis.

## Workflow

1. Create one object per section and selected bin size. Keep raw counts, provenance and QC retention counts. Restrict multimodal inputs to Gene Expression. Choose QC thresholds for the platform; report all exclusions.
2. Confirm gene symbols, unique IDs, genes-by-spots orientation in R, and coordinate/metadata alignment. The inspected SpaCET constructor retains the duplicate-symbol row with highest total expression rather than summing duplicates. Resolve and record mappings before analysis where possible; do not silently suffix or uppercase symbols.
3. Use the official `SpaCET.deconvolution` with a verified dictionary code. Check `SKCM` in the installed dictionary for cutaneous melanoma; do not silently change the requested code to `PANCAN`. Native automatic signature selection can itself fall back to a pan-cancer expression signature: record and report `malRes$sig` alongside the requested code. Save the complete object, settings, version and `sessionInfo()`.
4. Preserve `propMat` intact. Parent lineages and sublineages coexist: their combined sum is not a probability partition. Obtain major lineages from `Ref$lineageTree`. Keep Unidentifiable separate.
5. Validate malignant/major-lineage spatial patterns with markers, H&E and tissue quality. Investigate rare/ambiguous sublineages; hierarchical regression does not establish their accuracy. Use optional custom-reference, malignant-state and interaction workflows only when relevant, after checking upstream interfaces.
6. Export with the R recipe in [bridge](references/bridge.md), then run `scripts/spacet_to_gsmap.py`. The converter checks IDs, count values, coordinates, hierarchy and labels, and writes an h5ad plus audit. Do not align tables by row position or reconstruct barcodes by guessing from coordinate IDs.

## AnnData contract

- `X`, `layers['count']`: sparse spots × genes, unnormalized retained-gene counts.
- `var_names`: unique symbols compatible with gsMap gene resources.
- `obsm['spatial']`: x/y with units and axis convention recorded.
- `obs_names`: sample-prefixed source IDs; retain SpaCET IDs and barcode/source IDs in `obs`.
- `obsm['spacet_fractions']`: all continuous fraction columns, without renormalizing or adding parent and child lineages.
- `obs['spacet_major_dominant']`: descriptive major-lineage maximum, with top fraction, margin and tie flag.
- `obs['gsmap_annotation']`: only created under an explicit dominant-major policy or from reviewed labels. The default creates no modelling labels. Any thresholds are analysis choices, not validated SpaCET defaults.

Never scale expression by the dominant fraction or invent cell-type-specific expression. The 10x constructor renames bins/spots; use `@input$metaData$barcode` for the original mapping. Images are not embedded by this bridge; use recorded units and matching image transforms for overlays.

## gsMap handoff

Use the installed `gsmap` skill for resource/GWAS preparation and analysis. Verify exact CLI flags; never invoke unavailable MCP tools by invented names. At the inspected gsMap commit, annotated latent training removes null labels and classes with fewer than 30 spots; annotations also constrain gene-score neighborhoods. Review the converter's predicted removal audit before running. Do not create a biological Mixed/Unknown class merely to keep uncertain spots.

For no-annotation sensitivity analysis use supported step-by-step stages: current quick mode requires an annotation argument. Keep policies consistent across samples and use fresh work directories when inputs/settings change. Preserve patient/section nesting. Spot enrichment and pooled Cauchy significance are not independent-patient replication, causal effects, or cell-abundance tests. Check GWAS ancestry/LD compatibility separately from tissue donor ancestry.

## Verification and maintenance

Report actual execution scope and material limitations. Format checks do not validate biology. Run `python scripts/test_bridge.py`, the host skill validator, and a fresh-agent task after substantive changes; save tested scope in [sources](references/sources.md). Commit and push only this skill directory to persist updates.

For a separately requested full-paper reading package, use Paper2Agent's supported `paper_bundle.py` workflow, page/source review and strict verification. The linked `pdf_to_skill.py` is its internal PDF engine, not an installer. This operational skill is not a verified transcription of the complete paper.
