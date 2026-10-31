# Three-section analysis plan

This is a reusable design, not an executed analysis. Use P1CRC, P2CRC and P5CRC for original-study reproduction. The wider single-cell atlas comes from five patients/eight FFPE blocks. The paper uses Space Ranger 3.0, Cell Ranger 8.0.0 and Seurat 5; do not assume current software reproduces old objects.

## Dependency and output contract

The manual branch jointly clusters the three spatial sections. The RCTD branch uses a separately annotated single-cell reference and deconvolves each section. Neither method requires the other's predictions as training labels; Figure_3 attaches RCTD results for comparison.

| Stage | Inputs | Outputs and checks |
|---|---|---|
| Manifest | sample_id, patient_id, SR outs, H&E, chemistry, bin unit, versions | One row/section; unique identities and verified files |
| Per-section QC | filtered H5, tissue_positions.parquet, scale factors, image | UMI/features/tissue summaries and registered overlays; no unexplained barcode mismatch |
| Combine | three 8-µm matrices | Explicit gene alignment, unique sample-qualified barcodes, preserved raw counts |
| Sketch | normalized expression and variable genes | Selected bin IDs, seed, sample representation; paper 15% versus source fixed 240000 |
| Level 1 | sketch PCs/neighbors/clusters | Marker/evidence table and broad labels; 20 PCs/resolution 0.8 |
| Level 2 | each broad group | Subclusters, marker tables and labels; 25 PCs/resolution 0.1 |
| Projection | annotated sketch | Full barcode-keyed annotations and confidence; marker/spatial review per sample |
| RCTD reference | raw scRNA counts and cell labels | Exact barcode/gene alignment; class counts; source retains labels with >25 cells |
| RCTD | per-section raw counts, coordinates, reference | Class, first/second labels, weights and exclusion report; reconcile minimum 100 UMIs explicitly |
| Compare | manual and RCTD outputs | Matching label vocabulary/barcode universe, disagreements, histology and denominator checks |
| Nuclear branch | H&E, native 2-µm counts/positions | Polygons, square-to-nucleus map, gene-by-nucleus counts, unmapped fraction and geometry overlays |
| Downstream | validated annotations and physical coordinates | Per-sample boundary/subtype/density/ROI/LIANA results with defined filters |

## Annotation decisions

Use multiple positive and negative markers, expression prevalence/specificity, sample distribution and morphology to justify identities. A cluster dominated by one patient can reflect biology or technical variation. Examine evidence before adding integration. Broad identities may contain several clusters; cluster numbers have no portable biological meaning.

The source's exploratory FindAllMarkers thresholds are Level 1 logfc.threshold=0.2/min.diff.pct=0.2 and Level 2 0.1/0.1, only.pos=TRUE and adjusted P<0.05. These identify cluster markers; they are not patient-level differential-expression tests. Save cluster, identity, markers, conflicting evidence, section distribution, confidence and reviewer notes. Keep uncertain/mixed labels explicit.

Keep raw counts for RCTD; do not replace them with integrated, scaled or log-transformed values. Preserve scRNA sample identity and verify count/label barcode alignment. Doublet calls describe cell-type mixtures within a unit, not exactly two intact cells. Do not treat second_type as a confident second identity for reject/doublet_uncertain. Report unresolved fractions and singlet-only exclusions because small T cells can be disproportionately excluded.

## Nuclear aggregation

Use the paper's StarDist nuclei plus native 2-µm squares when reproducing the study. Newer Space Ranger cell outputs and Bin2Cell are alternatives, not the same method. An 8-µm annotation can identify an ROI but copying it to smaller squares does not infer their identities anew.

Verify scale, image origin, transforms and square centers before aggregation. Resolve the documented coordinate-alias hazard in a project copy before running the original crop branch. Treat overlaps and unassigned squares explicitly. Save nucleus ID, constituent barcodes, area, square count, raw UMI total and centroid; test count conservation for uniquely assigned squares. Reassess QC for nuclear counts instead of blindly using 8-µm thresholds. The paper/code nuclear branch aggregates counts and plots marker expression; a new full nuclear clustering/RCTD annotation workflow is an adaptation, not established as an original paper step.

## Downstream design

The Methods describe a 50-µm tumor periphery, excluding isolated tumor singlets with fewer than 25 same-label neighboring bins. Nearby macrophages are clustered per patient with 10 PCs/resolution 0.2. The broader all-section macrophage analysis uses 15 PCs/resolution 0.2. Consult code-workflow.md for differences in exact selectors and implementation.

Density uses singlet bins and 2D kernel density scaled to a maximum of 1; this is relative concentration, not an absolute cells/mm² estimate. Confirm physical units: array indices and downscaled pixels are not µm. The paper describes three macrophage-rich ROIs and a cold region, radius 350 µm; scripts implement exemplar-region selections with different N settings. Save explicit ROI masks and selection criteria. Hallmark enrichment identifies associated programs, not causality.

Run LIANA per patient with aggregate_rank <=0.01 and record the actual region and cell-type universe. The rank is not the probability of physical binding. Assess spatial coexistence and expression; the source is LIANA 0.1.12. Substituting newer LIANA, CellChat or NicheNet is an adaptation. Xenium and sorted T-cell VDJ validation require additional assays and cannot be reconstructed from HD alone.

## Adaptation to three melanoma samples

Reuse the joint design while replacing the CRC reference, markers, cluster labels and tumor definitions. Inspect project metadata for primary/metastatic site, subtype and treatment before choosing a reference. Melanocytic identity alone is not proof of malignancy. Preserve common label vocabulary but allow patient-specific tumor states. Record every departure from the CRC workflow.

With three patients, assess patient-wise consistency and uncertainty; bins are not independent patient replicates. Do not compute cell-type composition from the biased sketch or compare singlet-only proportions without disclosing excluded bins.

## Execution acceptance

The author scripts require adaptation; see the code map for defects and missing objects. Validate loading, raw counts, barcode joins, projection and coordinates on representative inputs first. Record versions, spacexr patch/source, seeds, runtime/memory and checkpoint paths. A smoke test validates mechanics, not biology. Compare with the paper's metadata only after matching inclusion rules; do not claim numerical reproduction without a complete successful original-data run.
