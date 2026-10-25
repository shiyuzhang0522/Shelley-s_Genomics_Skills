# Troubleshooting and database maintenance

Treat issue reports as context. Reproduce against the installed version and actual source; an open thread, a closed label, or a user workaround does not establish a general fix. Capture a minimal object, exact call, package/OS versions, dimensions, labels and traceback. Do not upload patient data or file GitHub issues without explicit user authorization.

## Diagnose by symptom

| Symptom | First checks | Reviewed evidence |
| --- | --- | --- |
| Metadata length/order warning | Unique barcodes, layer coverage, explicit name-based alignment | [77](https://github.com/jinworks/CellChat/issues/77); constructor relabels instead of reorders |
| NA labels or group '0' | Remove/resolve missing annotation, rename zero label, drop unused levels | Maintainer response in [16](https://github.com/jinworks/CellChat/issues/16) |
| No signaling genes/candidates | Species, symbols, full gene universe, DB categories, subunits, candidate rule | subsetData and identifyOverExpressedInteractions source |
| projectData missing / PPI argument error | Inspect exports/version; pinned smoothData needs named adj argument | [185](https://github.com/jinworks/CellChat/issues/185), checked against current source; later user replies conflict |
| computeCellDistance unavailable | Confirm repository/version and actual exports; don't substitute unrelated function blindly | [297](https://github.com/jinworks/CellChat/issues/297) |
| Spatial NA/Inf or empty links | Units, sample IDs, finite geometry, ranges, k.min, distance scale, group sizes | [18](https://github.com/jinworks/CellChat/issues/18), [6](https://github.com/jinworks/CellChat/issues/6), [92](https://github.com/jinworks/CellChat/issues/92) |
| Merged spatial datasets confusing | Pool versus compare, per-sample coordinate calibration, sample-specific neighborhoods | [10](https://github.com/jinworks/CellChat/issues/10), spatial tutorial |
| Missing groups / lifted networks changed | Drop unused levels; inspect name/value mapping after lift | [53](https://github.com/jinworks/CellChat/issues/53), unresolved [108](https://github.com/jinworks/CellChat/issues/108) and source |
| Replicate interpretation unclear | Keep donor unit; min.samples is expression consistency, not donor-level testing | [300](https://github.com/jinworks/CellChat/issues/300), [364](https://github.com/jinworks/CellChat/issues/364); [224](https://github.com/jinworks/CellChat/issues/224) unresolved |
| Unexpected sampling influence | Check population.size; FALSE removes explicit weighting, not all sampling variability | [68](https://github.com/jinworks/CellChat/issues/68); spatial question [397](https://github.com/jinworks/CellChat/issues/397) lacks a maintainer resolution |
| Plot scales differ | Common scale/limits; compare raw matrices, inspect merged plotting route | [20](https://github.com/jinworks/CellChat/issues/20) |
| Multi-condition plot error | Reproduce with recorded version; use raw tables/simple networks while isolating plotting bug | Maintainer fixes and conditional line.on workaround in closed [375](https://github.com/jinworks/CellChat/issues/375) |
| Installation fails | Read first real compiler/dependency error; use correct Bioconductor installer and project library | [226](https://github.com/jinworks/CellChat/issues/226), [305](https://github.com/jinworks/CellChat/issues/305); user workarounds, not universal fixes |

The protocol's troubleshooting table covers AnnData/R conversion, igraph edge-attribute errors, and centrality on merged objects. Historical version downgrades and XQuartz/Xcode suggestions require diagnosis; don't reinstall a user's graphics stack or change a shared environment as a blanket fix. The printed `updateCellchat` is a capitalization error: actual API is `updateCellChat`. Preserve old objects and update a copy; object migration does not recompute inference with a new DB/method.

## No expected pathway

Check the exact species-specific pathway name and selected DB category. Verify all ligand/receptor subunits were measured, sufficiently detected, and pass the chosen candidate rule. Use `computeAveExpr` and underlying expression. A trimean can be zero for sparse expression; a documented truncatedMean sensitivity analysis is reasonable, but don't tune until a preferred signal appears. Check filters, spatial feasibility, sample support and p-value boundaries. A missing prediction is not proof of absent signaling.

## Database customization

Read the full Update-CellChatDB tutorial and actual `updateCellChatDB` formals before building custom databases. Provide ligand/receptor columns, unique interaction identities, evidence/source/version, species symbols, category and meaningful pathway mapping. Complex row names referenced in interactions must match subunit tables (`subunit_1`, etc.); cofactor names must match cofactor tables (`cofactor1`, etc.). Include geneInfo `Symbol` or an explicitly supported species target.

Audit symbol conversion, duplicated IDs, missing subunits, annotations and row counts before/after updates. When merging, built-in entries precede custom entries and duplicate interaction names can be dropped; custom rows do not automatically override built-ins. Save the actual resulting DB and assign `cc@DB <- db.new`; don't edit/rebuild the user's installed package merely to change an analysis database.

Without meaningful pathway names, LR scoring and pathway analysis are different capabilities. The tutorial's warning names computeCommunProb as pathway-level, but it is computeCommunProbPathway and downstream pathway summaries that need correct grouping. Empty pathway strings are not biological annotations.

Nonprotein signaling often uses enzyme/mediator expression proxies. Include it intentionally and interpret coverage separately. Current subsetDB defaults exclude these interactions; record whether they are present.

## External scores

`updateCCC_score` imports another method's source/target/ligand/receptor/score table for CellChat visualization. If P values are missing it can fill them with zero. Those are placeholders; they do not become valid CellChat significance results. Preserve original method, score semantics, real P values and missingness. Likewise inspect zero padding from lifting and fallback P values from rankNet before making significance claims.
