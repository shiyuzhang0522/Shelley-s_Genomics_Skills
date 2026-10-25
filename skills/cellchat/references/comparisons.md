# Comparisons, networks, and visualization

## Match the statistical unit to the question

For a descriptive condition comparison, the authors' workflow infers one object per condition and merges results. For population-level claims, preserve biological replicates and a donor-aware design; pooling thousands of cells does not create independent samples. Prefer per-donor support/sensitivity tables and a separately justified differential framework. Keep paired designs, unequal cell recovery, cell-type composition, and missing populations explicit.

Use consistent normalization/assay, species/DB, cell ontology, candidate selection, DE backend, summary method, population weighting, smoothing, and Monte Carlo settings. Each object's scoring matrix is divided by its own maximum; absolute score contrasts are model-dependent. Missing LR candidates and unmeasured genes are not automatically measured zero communication. Choose and report a comparable tested universe rather than quietly conflating untested, filtered and zero-score entries.

Infer independent objects, retain `object.list`, then use `mergeCellChat(object.list, add.names=names(object.list), cell.prefix=TRUE)` if barcodes would collide. Inspect names even when using automatic prefixes. Merging keeps shared data/metadata where appropriate; it is not batch correction, physical registration, or donor modeling. Compute centrality on each valid object before merged comparisons.

## Choose a comparison route

| Question | Route | Required caution |
| --- | --- | --- |
| More inferred links or summed strength? | compareInteractions, net$count/net$weight | Counts and weights are different; harmonize tested universe |
| Which group pairs change? | netVisual_diffInteraction, netVisual_heatmap | Verify order; difference is second minus first |
| Which pathways contribute? | rankNet(do.stat=FALSE), explicit pathway totals | Information flow is a score sum, not a causal flux |
| Which LR pairs change? | netVisual_bubble, subsetCommunication | Compare candidate coverage, p-values and raw expression separately |
| Which sender/receiver genes differ? | netMappingDEG after a justified DE analysis | Cell-level DE is not donor-aware by default |
| Similar network organization? | functional or structural similarity | Functional route needs aligned identities |

### Why not use rankNet stars as patient evidence?

The optional `rankNet(do.stat=TRUE)` test operates on vectorized source-target graph edges, not donor replicates. In this snapshot it also assigns p=0 to some <=3-informative-edge, missing, or NA cases. Those zeros may be fallbacks, not successful tests. Default to do.stat=FALSE and inspect raw per-donor evidence for condition claims. Do not reinterpret graph edges as biological replicates.

The DE mapping route uses `identifyOverExpressedGenes(group.dataset=..., pos.dataset=...)`, `netMappingDEG`, and `subsetCommunication` to associate sender-ligand/receiver-receptor expression changes with inferred interactions. Confirm actual filters: a tutorial comment describes both sides downregulated, but its `receptor.logFC=NULL` imposes no receptor-DE constraint. Preserve direction and cell-type context. If using external donor-aware DE, verify the import/mapping structure before substituting it.

## Different cell compositions

Drop unused levels when analyzing each dataset. For modest composition differences, use an explicit common label universe and inspect `liftCellChat` carefully. Current source uses membership-derived assignment indices without an explicit name permutation of values. Preserve each object's existing relative level order and verify dimensions, known entries, pathway arrays, and label-to-value mappings after lifting. If orders conflict, resolve and validate the ordering before lifting; do not just overwrite labels.

Padding represents absent/unobserved populations; it does not create measurements. Zero-padded scores or P values are not evidence of biological absence or significance. If composition differs greatly, avoid cell-pair differential graphs and functional similarity; structural comparisons may remain descriptive. Lifting labels does not make biologically noncomparable populations comparable.

## Higher-order analyses

1. `netAnalysis_computeCentrality(slot.name="netP")` precedes signaling-role network/scatter/heatmap plots. Weighted outdegree/indegree are inferred sender/receiver strengths; unweighted degree counts edges. Flow/information centrality errors can fall back to zero, so inspect degeneracy before biological interpretation.
2. `selectK` informs `identifyCommunicationPatterns(pattern="outgoing"/"incoming", k=...)`. NMF decomposes a group-by-pathway network summary, normalized by pathway maxima. Choose k using diagnostics and stability, not the example's number. Pattern indices from separate fits are not automatically corresponding biological programs.
3. Functional similarity compares binary edges with matching sender/receiver identities; structural similarity compares topology. Compute `computeNetSimilarity` or `computeNetSimilarityPairwise`, then embedding and clustering. Embedding distances and cluster membership are descriptive network summaries. `rankSimilarity` uses shared pathways; inspect condition-specific pathways separately.

## Plot after inspecting tables

- `netVisual_circle`/`netVisual_aggregate`: group/pathway networks; `netVisual_individual`: particular LR pairs.
- Bubble plots: selected sender-target/LR edges. Use current group names or verify indices against factor levels.
- `netAnalysis_contribution`/`extractEnrichedLR`: contributing LR pairs within a pathway. Inspect every required complex subunit's actual expression.
- Chord-cell and chord-gene plots have different sector meanings; label the units.
- Use common edge/color scales and legends across conditions (`getMaxWeight` where appropriate). Independently autoscaled panels can exaggerate differences.
- Signaling-role heatmap colors are row-scaled relative values; bar summaries answer different questions.
- Check pathway existence and zero/singleton arrays before plotting. Preserve empty results as meaningful diagnostics instead of forcing arrows.
- `runCellChatApp`/Explorer can aid inspection, but low-dimensional cell embeddings in `@dr` are neither expression nor physical coordinates. Original web Explorer DB coverage may lag current CellChatDB.

For manuscript outputs, use the ng-figure skill when requested; use restrained colors, explicit source/target directions, score definitions, thresholds and database provenance. Save tables alongside vector figures.
