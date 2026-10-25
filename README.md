# Shelley's Genomics Skills

Reusable skills for genomics research, co-created by Shelley and Morgan.

## Available skills

| Skill | Purpose |
|---|---|
| [NG_Figure.Skill](skills/ng-figure/SKILL.md) (`ng-figure`) | Nature Genetics-compatible figures and reproducible R/Python plotting, with editable PDF export and quality checks. |
| [SpaCET to gsMap](skills/spacet/SKILL.md) (`spacet`) | Tumor spatial deconvolution, barcode-aligned sparse AnnData export, and an audited gsMap handoff. |
| [gsMap](skills/gsmap/SKILL.md) (`gsmap`) | Spatial transcriptomics–GWAS integration, input preparation, spatial LDSC, and downstream reports. |

## Using NG_Figure.Skill

Invoke the installed skill with `$ng-figure`, for example:

> Use $ng-figure to refine this plot for Nature Genetics and export an editable PDF.

The skill separates verified journal requirements from aesthetic defaults, checks final figure dimensions and fonts, and uses restrained, informative colors. It includes R export recipes, Python helpers, and a PDF inspection utility.

The self-contained skill folder is `skills/ng-figure/`. Preserve its relative folder structure when adding it to a compatible agent's skills directory.

## Using SpaCET to gsMap

The workflow uses two companion skills. Keep each folder intact when installing it in a compatible agent's skills directory:

- `skills/spacet/`: SpaCET workflow, R export recipe, Python converter, synthetic regression tests, and interpretation guidance.
- `skills/gsmap/`: downstream gsMap workflow and bundled upstream documentation, with its original skill and MIT license retained for attribution.

Example request:

> Use $spacet to prepare my tumor spatial samples for gsMap, then use $gsmap to review the GWAS inputs and analysis plan.

The bridge preserves raw retained-gene counts and continuous fractions, aligns observations by identifiers, and audits annotation-related exclusions. Installing these skills does not install R/SpaCET, gsMap, or reference datasets.

## Validation

Created 16 October 2026. Skill structure, Python PDF export, error detection, and a toy forest plot were tested. R recipes were reviewed but not executed; native Illustrator and macOS Preview checks were unavailable. Individual figures still require scientific and visual review. Official guidance and its verification date are recorded inside the skill.

SpaCET/gsMap packages were added on 25 October 2026 from the installed skills without changing their contents. Both passed the skill-format validator. The SpaCET provenance records 17 passing synthetic regression tests on 22 October 2026; a repeat run during this repository import could not start because `anndata` is absent from the current environment. R/SpaCET deconvolution and the full gsMap/GWAS workflow have not been executed here. See [SpaCET provenance and tested scope](skills/spacet/references/sources.md).

## Contributors

- **Shelley (Shiyu Zhang; [@shiyuzhang0522](https://github.com/shiyuzhang0522))** — repository owner and scientific lead; defines requirements, reviews outputs, and sets research priorities.
- **Morgan (OpenAI ChatGPT)** — AI assistant supporting skill design, documentation, code development, and validation at Shelley's direction. This acknowledgment does not represent a separate GitHub account or human contributor.

## Ongoing maintenance

Use this repository to version future genomics skills and improvements. Shelley retains ownership and directs the work; Morgan can help implement requested updates through the connected tools.

For each update:

1. Read the current repository version and agree on the intended behavior from the task context.
2. Update the skill and its relevant scripts or references together.
3. Run the checks appropriate to the change and document any untested behavior.
4. Commit a concise explanation of the change. When the skill is also installed in ChatGPT, keep that installed version and this repository aligned.
