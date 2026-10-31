# Pinned code-to-method map and three-sample workflow

This reference records a **static review**, not a successful analysis run. All 18 R files, the Python script, the environment YAML and README were read at repository commit `df5801cf5e681b33b5026626989a7635fdf26b99`. The coordinator verified that the 20 method/figure R/Python/YAML files match the [Zenodo archive](https://zenodo.org/records/15042463), ignoring final-newline differences; README differs. The downloaded archive MD5 matches the deposited metadata: `bde1f1a374511923af4b98aa58bec421`. Research scripts were not executed and bulk assay data were not downloaded. Paper evidence is the published article, DOI [10.1038/s41588-025-02193-3][paper], especially Methods sections named below. **Paper-described**, **code-observed**, and **recommended adaptation** are separate evidence classes. A script's existence does not establish that it runs unchanged or reproduces the publication.

## Contents

- [Scope, samples and units](#scope-samples-and-units)
- [Source map: every reviewed file](#source-map-every-reviewed-file)
- [Three-sample analysis sequence](#three-sample-analysis-sequence)
- [Function lookup](#function-lookup)
- [Software evidence and execution gates](#software-evidence-and-execution-gates)

## Scope, samples and units

The core spatial analysis combines **P1CRC, P2CRC and P5CRC**. The matched Flex reference atlas covers eight normal/CRC specimens; it is not a three-spatial-sample-only atlas. Keep patient/sample identity in every merged barcode and every inferential comparison. [Paper Results, “Visium HD maps the landscape of CRC at single-cell scale”; Figure_3.R lines 25–71][f3].

| Sample | Repository spatial output directory | Dominant tumor label used in main scripts | Published metadata filename | Example tumor boundary center | T-cell segmentation center |
|---|---|---|---|---|---|
| P1CRC | `~/VisiumHD/PatientCRC1/outs/` | `Tumor II` | `P1CRC_Metadata.parquet` | `s_008um_00556_00532-1` | `s_008um_00176_00486-1` |
| P2CRC | `~/VisiumHD/PatientCRC2/outs/` | `Tumor III` | `P2CRC_Metadata.parquet` | `s_008um_00587_00568-1` | `s_008um_00460_00073-1` |
| P5CRC | `~/VisiumHD/PatientCRC5/outs/` | `Tumor IV` | `P5CRC_Metadata.parquet` | `s_008um_00348_00165-1` | `s_008um_00365_00224-1` |

Sources: [Figure_5.R lines 26–31][f5], [Figure_4.R lines 40–46][f4], [Figure_6.R lines 86–91][f6], [README lines 126–146][readme]. These are publication-specific identifiers, not tumor labels or ROIs to transplant to new patients. **Conflict:** SupplementalFigure_8.R line 28 reverses the P1/P2 tumor labels; use the main manifest as the starting evidence and verify against supplied metadata and marker expression. [SupplementalFigure_8.R][s8]

- The native feature is a **2 × 2 µm square**; default downstream analysis uses **8 × 8 µm bins**; Space Ranger also supplies 16 × 16 µm bins. One 8 µm bin contains 16 native 2 µm features. An 8 µm bin is an analysis unit at single-cell scale, not a measured cell or nucleus.
- `GenerateSampleData(PATH, size="008um")` expects `PATH` to be a Space Ranger `outs` directory. It reads the selected bin-size tissue-position Parquet, scale JSON and optional graph-cluster/UMAP CSVs, plus the root `spatial/tissue_lowres_image.png`; it returns `list(images_tibble, bcs)`. `row`/`col` are array indices; `imagerow`/`imagecol` are full-resolution pixel coordinates; `*_scaled` are low-resolution plotting pixels. [AuxFunctions.R lines 6–88][aux]
- `GetSquare(Spot, SizeMicrons, ..., binsize=8)` treats `SizeMicrons` as approximate **side length**, uses rounded half-width in array bins and includes both boundaries. `GetSlice(..., SizeMicrons, ..., size="008um")` treats it as a **radius**, converts µm to full-resolution pixels and uses strict `<` distance. `Area=350` passed through `SelectEnrichedRegion` therefore means **350 µm radius**, not area or diameter. [AuxFunctions.R lines 190–205, 330–380, 481–512][aux]
- `GetDistance` and `SelectTumor` accept a `size` argument but hardcode multiplication by `8` when converting pixel distances to µm. They are only internally consistent with the 8 µm scale unless adapted. [AuxFunctions.R lines 553–623][aux]

## Source map: every reviewed file

| Pinned source | Actual purpose, inputs and outputs | What it does not supply |
|---|---|---|
| [README.md][readme] | Data links; method introductions; CLI and output descriptions; metadata schemas; common packages; sample-path template. | A complete environment lock or an executable orchestration plan. |
| [Methods/FlexSingleCell.R][flex] | Aggregated Flex H5, aggregation CSV and Cell Ranger UMAP → BPCells/Seurat object, QC, sketch, manual annotation, projection → `FlexSeuratV5.rds` and `FlexSeuratV5_MetaData.rds` (lines 14–150). | Automatic transferable annotation; robust portable paths. |
| [Methods/Deconvolution.R][deconv] | Flex counts plus Level2 metadata → `Reference`; 8 µm HD H5 and positions → `SpatialRNA`, `create.RCTD`, doublet-mode `run.RCTD` → per-sample RCTD RDS (lines 11–47). | A three-sample loop, exact spacexr build pin, explicit minimum-UMI argument. |
| [Methods/AuxFunctions.R][aux] | Data/coordinate readers, RCTD extraction, expression joins, ROI/periphery/density utilities, barcode expansion, enrichment and interaction plotting (function map below). | A standalone runnable pipeline or universally bin-size-safe geometry. |
| [Methods/NucleiSegmentation.py][seg] | H&E image plus bin-size directory → full-section StarDist masks/polygons, barcode-to-nucleus CSV; optional image/ROI crop (lines 25–117). | Cell-boundary segmentation, expression-based cell typing or count aggregation. |
| [Methods/environment_nucleisegmentation.yml][env] | Conda package/build snapshot for segmentation. | R environment, portable cross-platform lock or proof of successful installation. |
| [Figures/Figure_2d.R][f2] | HD/v2 raw probe matrices, probe-filter flags, downloaded v2 probe panel → per-probe totals and log10(UMI+1) scatter/correlation plots (lines 13–129). | The paper's manual matched-area selection itself; explicit `method="spearman"`. |
| [Figures/Figure_3.R][f3] | Three 8 µm matrices plus deconvolution CSVs → merged sketch/manual L1/L2 analysis and projected labels; spatial and expression plots (lines 25–288). | A clean standalone script: unresolved variables and missing BPCells import. |
| [Figures/Figure_4.R][f4] | RCTD plus spatial counts/coordinates → 50 µm periphery, saved barcode RDS, proportions, per-sample macrophage clustering/density, combined marker dotplot (lines 24–356). | A complete three-sample manifest in this file; execution-safe first periphery call. |
| [Figures/Figure_5.R][f5] | Explicit three-sample manifest → macrophage/tumor marker and Hallmark analysis, pooled goblet clustering, per-patient LIANA (lines 26–483). | Batch-corrected integration or a donor-aware differential-expression model. |
| [Figures/Figure_6.R][f6] | RCTD classes/periphery → proportion plots; 8→2 µm mapping plus segmentation CSV → gene-by-nucleus counts, normalized CD4/CD8A overlays (lines 26–229). | Segmentation execution or whole-cell labels; its CSV field expectations need repair. |
| [Figures/Figure_7.R][f7] | P5CRC 2 µm counts and segmentation output → nucleus-level expression overlays for CEACAM5, SELENOP, C1QC, JCHAIN, TRAC, CXCL9 (lines 28–121). | Full Xenium/TCR/clonotype analysis: this script addresses the Visium HD validation region. |
| [Figures/SupplementalFigure_1.R][s1] | HD/v2 P2/P5 probe sensitivity comparisons, similar to Figure_2d (lines 14–173). | Matched-area extraction; explicit Spearman setting; internally consistent P2 cancer/NAT naming. |
| [Figures/SupplementalFigure_3.R][s3] | Supplied `SingleCell_MetaData.csv.gz`, QCFilter=Keep → reference-atlas counts and UMAP plots by annotation/patient/condition (lines 24–81). | Rebuilding the Flex atlas. |
| [Figures/SupplementalFigure_4.R][s4] | Three RCTD outputs plus tissue positions → proportions of singlet bins by first label (lines 24–56). | Cell-count proportions corrected for cell size or multiple bins per cell. |
| [Figures/SupplementalFigure_5.R][s5] | Saved Flex object, tumor Level2 labels and CRC condition → tumor UMAP/clustering (20 PCs, resolution 0.4), marker dot/feature plots (lines 24–86). | Spatial tumor clustering; final bare `gg` is undefined (line 87). |
| [Figures/SupplementalFigure_6.R][s6] | Repeats merged spatial sketch/manual workflow; compares singlet RCTD first label with unsupervised L2 using row-percentage confusion heatmap (lines 25–241). | An independent corrected implementation; inherits Figure_3 portability gaps. |
| [Figures/SupplementalFigure_7.R][s7] | All singlet macrophage bins across three sections → merged clustering (15 PCs, resolution 0.2), markers, periphery/patient proportions and spatial plot (lines 29–181). | Ready-to-run code: `library(ggnetwork` lacks `)`; disk-matrix source is underspecified. |
| [Figures/SupplementalFigure_8.R][s8] | First-label CD4/CD8 bins → class proportions inside/outside periphery (lines 24–72). | Reliable manifest without reconciling swapped tumor labels and accumulation errors. |
| [Figures/SupplementalFigure_9.R][s9] | Macrophage/T-cell colocalization and 2 µm nucleus overlays of eight markers (lines 24–219). | General multi-sample execution: latter code passes whole path vectors where one path is required. |
| [Figures/SupplementalFigure_10.R][s10] | Xenium/HD positions, images, alignment cell-info CSVs and count H5s → per-gene sensitivity plots (lines 10–234). | A working matched-area subset: filtered Xenium coordinates are not used to subset the matrix in `get_per_feature_umis`. |

No supplied `Figure_1.R`, `SupplementalFigure_2.R` or exact mask-distance implementation for the paper's Fig. 2e/Extended Data Fig. 2 was present in the reviewed script set. `SpatialAccuracy` in AuxFunctions.R lines 1042–1128 makes square zoom-in expression plots; it does **not** implement source-mask/adjacent-mask transcript assignment and nearest-mask-edge distances from paper Methods “Spatial accuracy.” Figure scripts mostly create in-memory plot objects; they do not save publication figure files with `ggsave` or equivalent.

## Three-sample analysis sequence

### 1. Establish raw inputs and separate reproduction from reanalysis

**Code-observed inputs:** for each P1/P2/P5 section, use `outs/binned_outputs/square_008um/filtered_feature_bc_matrix.h5`, `spatial/tissue_positions.parquet`, `spatial/scalefactors_json.json`, root low-resolution image, and optional Space Ranger graph-cluster/UMAP CSVs. Nuclei work additionally needs the corresponding high-resolution H&E image and `square_002um` matrix/coordinates. Flex inputs are aggregation H5, aggregation CSV and UMAP CSV. Existing published per-bin annotations are documented by [README lines 111–146][readme]: barcode, tissue, X/Y, three deconvolution columns, periphery, `UnsupervisedL1`, `UnsupervisedL2`, `MacrophageSubtype`, `GobletSubcluster`.

**Recommended adaptation:** create a single explicit sample manifest mapping canonical IDs to actual paths, tumor label, image and periphery/segmentation outputs; validate matching barcodes and gene identities before merging. Use supplied metadata for publication-label reproduction when appropriate. For a new analysis, rebuild labels and inspect marker/morphology evidence; do not reuse hardcoded cluster-number labels. Metadata are described/published externally; this static review did not download or validate their contents.

### 2. Build or reuse the Flex reference

**Paper-described:** Cell Ranger 8.0.0, Seurat v5, remove upper/lower 2.5% UMI and detected-gene tails, leverage-score sketching, 25 PCs/resolution 0.6 for L1, 25 PCs/resolution 0.1 for L2, manual markers, projection to all retained cells. [Methods “Chromium Single Cell Gene Expression Flex,” Sec15][paper]

**Code-observed:** `FlexSingleCell.R` uses BPCells; additionally requires mitochondrial percentage `<25`; quantile filters use strict `>`/`<`; sketches **37,000** cells; L1 marker thresholds `min.diff.pct=0.2`, `logfc.threshold=0.2`, positive markers, adjusted P<0.05; L2 uses the same thresholds. It encodes 26 cluster-to-L1 labels and a fixed L2 label vector. `Seurat:::ProjectData(..., dims=1:50)` transfers labels. Outputs are the two RDS files above. [Lines 38–150][flex]

**Caution:** the 37,000 count is a fixed approximation to the stated 15%, not a dynamic fraction. Imported Cell Ranger UMAP coordinates are created as a dimension reduction, but no `RunUMAP(..., return.model=TRUE)` is present before `ProjectData(..., umap.model="umap")`; model compatibility is unresolved. Fix path assembly and metadata fields before any run.

### 3. Spatial unsupervised clustering and manual annotation are present

**Paper-described:** merge three 8 µm count matrices, sketch 15% by leverage score; 20 PCs/resolution 0.8; manual L1 labels; recluster L1 groups with 25 PCs/resolution 0.1; project to full data. [Methods “Visium HD Spatial Gene Expression,” Sec11][paper]

**Code-observed:** Figure_3.R and SupplementalFigure_6.R explicitly implement this outline with a **240,000-bin** sketch; `CreateSeuratObject(counts=Matrices)` and `JoinLayers`; normalization/variable genes/scaling/PCA; 20-PC neighbors, resolution 0.8, UMAP with saved model; fixed 23-cluster L1 mapping; per-L1 25-PC/resolution 0.1 reclustering and marker analysis; fixed allowed L2 subcluster IDs; 50-PC `ProjectData` label transfer. L1 labels include nine named broad cell types plus Unknown. [Figure_3.R lines 25–162][f3]

Thus **do not describe the spatial manual clustering workflow as absent or only supplied metadata**. Both source code and metadata schemas exist. However, code encodes publication-specific manual decisions and is incomplete as a standalone executable; exact published `UnsupervisedL1/L2` metadata are a distinct reproduction input.

**Batch/integration evidence:** code combines layers/count matrices and performs common preprocessing. No `IntegrateData`, `IntegrateLayers`, anchor workflow, Harmony or explicit batch correction appears anywhere in reviewed R scripts. Figure_4/5 combine macrophages using `merge`→`JoinLayers`→`NormalizeData`; SupplementalFigure_7 uses merged matrices. The paper's word “integrated” does not establish a batch-corrected latent representation. A donor-aware model, pseudobulk comparison, or additional integration is a **recommended new analysis**, not a reproduced paper step.

### 4. RCTD per spatial section

**Code-observed:** reference Level2 populations with **>25** cells are retained (not ≥25); labels have `/` replaced by `_`; reference counts and column sums are passed to `Reference`. Each spatial section uses 8 µm filtered counts and tissue-position columns **3:4** (array coordinates); `SpatialRNA`; `create.RCTD(..., max_cores=12)`; `run.RCTD(..., doublet_mode="doublet")`; save complete RCTD RDS. The file is a P1 template to parameterize for P2 and P5. [Deconvolution.R lines 19–47][deconv]

**Paper-described:** minimum **100 UMIs per bin**; doublet mode; classes `singlet`, `doublet_certain`, `doublet_uncertain`, `reject`; performance modification linked as [spacexr PR 206](https://github.com/dmcable/spacexr/pull/206). [Methods “Spot deconvolution,” Sec16][paper]

**Unresolved default dependence:** the source supplies no `UMI_min` and no manual 100-UMI prefilter, so it delegates threshold behavior to the installed spacexr build. Omission alone does **not** prove that the run used another threshold. The article's reporting summary (main PDF page 26, Data analysis) reports **“spacrxr v2.2.1”**; the package spelling is preserved here and interpreted as a typo for spacexr, consistent with Methods and the code. The exact modified PR commit/build is still not pinned. For reproduction, inspect the installed `create.RCTD` defaults/configuration and explicitly record or set the 100-UMI threshold supported by that version. Do not conflate the spatial UMI cutoff with reference-population >25-cell filtering, periphery 25-label support or downstream singlet selection.

`readRCTD` extracts `results_df` and doublet weights; `AddDeconvolutionInfo` joins by barcode. **Repair required:** line 151 reads `scond_type`, while the corresponding RCTD field elsewhere is `second_type`; weight reconstruction line 130 does not pair row and column indices. Verify these fields and weights against the original RCTD object before using imported labels or `AddWeights=TRUE`. [AuxFunctions.R lines 106–169][aux]

### 5. Define 50 µm periphery and macrophage subpopulations

`SelectPeripheryDiscrete` selects first-label tumor bins, calls `GetSlice` for each seed, unions neighbors, and removes tumor-labeled bins from the result. `GetSlice` rejects seeds with fewer than **25 same-label bins within strict radius <50 µm**; its count includes the seed itself. Singlet/tissue restriction is a caller responsibility, not built into the helper. Figure_5 filters `tissue==1 & DeconvolutionClass=="singlet"` before computing/reusing periphery. Save a barcode vector and mark each bin `"50 micron"`, `"Tumor"` or `"Tissue"`. [AuxFunctions.R lines 304–380][aux]; [Figure_5.R lines 59–81][f5]

Per patient, select singlet macrophage bins in the 50 µm region, normalize, find variable genes, scale, PCA, neighbors 1:10, resolution 0.2. Positive markers use logFC/min.diff.pct=0.1 and adjusted P<0.05 in the main macrophage loop. With >1 clusters, code picks the first marker-table occurrence of SPP1 to identify one cluster and labels **all other clusters** SELENOP+. With one cluster, it labels all SELENOP+ (comment anticipates P5CRC). This is an assumption requiring marker review, not a general two-state classifier. [Figure_4.R lines 216–308][f4]; [Figure_5.R lines 89–166][f5]

The broader macrophage branch includes all singlet macrophage bins irrespective of periphery, merges three samples, uses 15 PCs/resolution 0.2 and reports patient/periphery composition. It is located in SupplementalFigure_7.R, with the syntax/path defects listed below. Do not interpret this as every macrophage being reducible to the two boundary populations. [Lines 54–124][s7]

### 6. Density, ROI, tumor neighbors, enrichment and goblet cells

`PlotDensity` draws `geom_density_2d(..., contour_var="ndensity")` contours normalized to a maximum of 1; `nBins` controls contour levels, **not spatial bin size**. Singlet filtering happens upstream. `SelectEnrichedRegion` computes `MASS::kde2d` on full-resolution coordinates (`n=200` grid), detects strict local maxima using eight neighbors, sorts peaks and selects up to `N`. It finds the nearest observed barcode to each peak, then selects a circular region using `GetSlice`. `SelectTumor` finds nearby tumor bins with strict distance `<DistVal` (typically 50 µm), after limiting the search around a region center using a hardcoded 350 µm radius. [AuxFunctions.R lines 425–623][aux]

**Paper/code discrepancy:** Methods “Distance, local and regional analysis” describes the top **three** macrophage-density regions plus a **cold** region and 350 µm-radius ROIs. Main Figure_4/5 code calls `SelectEnrichedRegion(..., N=1, Area=350)` separately for each macrophage subtype; no cold-region branch was found. Do not silently replace one definition with the other. [Figure_5.R lines 125–166][f5]; [paper Sec18][paper]

Combined macrophage/tumor comparisons use merged normalized bins and `FindAllMarkers`; no patient covariate, replicate-level pseudobulk or paired statistical test is specified. `EnrichRBarPlot` sends two marker-gene lists to `enrichr`, here `MSigDB_Hallmark_2020`; it is gene-list overrepresentation, not a ranked-list GSEA implementation. It filters raw P<0.001, then `slice_max(P.value)` selects the largest P values within retained terms, and uses signed **natural log** adjusted P for the display. The paper's ranked-logFC enrichment description is not fully implemented by this helper. [Figure_5.R lines 173–235][f5]; [AuxFunctions.R lines 385–418][aux]

Goblet branch: select singlet first-label Goblet bins from all three sections; append sample IDs; column-bind raw 8 µm matrices; normalize/variable genes/scale/PCA; 12 PCs/resolution 0.2; markers with logFC/min.diff.pct=0.1 and adjusted P<0.05; map clusters back to sections. [Figure_5.R lines 240–335][f5]

### 7. LIANA per patient

**Paper-described:** LIANA **0.1.12**, tumor periphery within 50 µm, separate Seurat object per patient, retain `aggregate_rank <= 0.01`. [Methods “Ligand–receptor analysis,” Sec19][paper]

**Code-observed:** rederive macrophage subtype labels; start with singlet periphery and tumor bins; include tumor bins with **at least five** periphery bins within **≤50 µm**; build/normalize a Seurat object containing these tumor neighbors plus periphery singlets; use first-label/subtype `CellType` identities; run `liana_wrap(object) %>% liana_aggregate() %>% filter(aggregate_rank <= 0.01)`. Methods/resource and most other LIANA settings are defaults, not explicit. Network helpers count retained ligand–receptor rows by source/target; they are not independently measured communication flux or proof of signaling. [Figure_5.R lines 349–456][f5]; [AuxFunctions.R lines 771–851, 916–1011][aux]

### 8. Nuclear segmentation and custom 2 µm aggregation

**Code-observed Python:** read full H&E image; load StarDist pretrained `2D_versatile_he`; normalize percentiles 5–95; `predict_instances_big(axes="YXC", block_size=4096, prob_thresh=0.01, nms_thresh=0.001, min_overlap=128, context=128, normalizer=None, n_tiles=(4,4,1))`; save full label/polygon pickles; optionally crop image and export ImageJ ROI ZIP. Convert polygon row/column coordinates to x/y; make points from full-resolution bin coordinates; `geopandas.sjoin(..., predicate="within")`; flag duplicated barcode assignments as overlaps; export `Nuclei_Barcode_Map.csv` with columns **`index`, `id`, `is_within_polygon`, `is_overlap`** plus the CSV index. [NucleiSegmentation.py lines 27–117][seg]

The spatial join uses the full tissue-position table, not the previously merged filtered-count `adata.obs`. Therefore retain only relevant count barcodes/tissue downstream. `within` uses bin-center geometry; the script does not assign by fractional square overlap with a polygon. Boundary points and overlapping polygons need explicit handling. The model segments **nuclei**, not cell membranes; aggregated counts are gene-by-nucleus, not certified whole-cell profiles.

**Critical crop hazard:** `polys2 = polys` aliases the same dictionary. When a crop is requested, lines 60–61 subtract crop offsets from selected coordinates before lines 72–76 build the full-section polygons. This mixes cropped and full-image coordinates in the subsequent barcode mapping. The full-section pickle was saved before mutation. **Recommended repair:** preserve immutable full-image polygons and deep-copy only crop-export coordinates, or perform full-section barcode assignment before any crop transformation. Validate nucleus/barcode overlays on the matching image.

**R aggregation:** `TransformBarcodes(8,2)` expands one 8 µm bin into 16 names assuming the repository barcode format and suffix `-1`. Figure_6/7 remove overlap assignments, link 2 µm bins to nuclei, build `sparse.model.matrix(~0+Group)`, multiply gene×bin counts by bin×nucleus indicator matrix, create/normalize Seurat and plot markers. [AuxFunctions.R lines 695–730][aux]; [Figure_6.R lines 163–229][f6]; [Figure_7.R lines 61–121][f7]

The observed nucleus-aggregation branches plot normalized marker expression; they do **not rerun RCTD on nuclei**. Applying RCTD or another cell-typing method to the nucleus-level matrix would be a proposed adaptation requiring its own validation, not an implemented step established by these paper/code sources.

**Interface repairs:** `NucleiSegmentationScript` prints `-x`, but Python accepts **`-s/--srdir`**. Python CSV names barcode field **`index`**, while R figure scripts expect **`barcode`**. Crop filenames produced by Python are generic, whereas figures expect sample-suffixed names; output directories are not created by Python. These mismatches must be resolved before a run. [AuxFunctions.R lines 735–745][aux]; [NucleiSegmentation.py lines 117–130][seg]; [Figure_6.R lines 95–97, 170–177][f6]

## Function lookup

All below are in [Methods/AuxFunctions.R][aux]; line numbers refer to the pinned commit.

| Function | Lines | Input → output / important behavior |
|---|---:|---|
| `GenerateSampleData`, `make_images_tibble`, `get_spatial_files` | 6–88 | Space Ranger directory/bin size → coordinate metadata and image grob. |
| `readRCTD`, `get_doublet_weights_modified`, `AddDeconvolutionInfo` | 106–169 | RCTD RDS → result table/weights → joined metadata; defects above. |
| `AddExpression`, `PlotExpression` | 174–249 | `FetchData` expression joined by barcode; normalized expression depends on current Seurat assay/layer. |
| `GetSquare`, `GetSlice`, `SelectPeripheryDiscrete` | 190–205, 304–380 | Barcode-centered square or radius union; periphery excludes same-label bins and imposes 25-label support. |
| `PlotDensity`, `SelectEnrichedRegion`, `findPeaks3D` | 425–550 | Density contours, top local maxima, circular ROI barcode sets; helpers do not enforce singlets. |
| `GetDistance`, `SelectTumor` | 553–623 | µm distance / nearby tumor barcodes; 8 µm conversion assumption and 350 µm search window. |
| `PlotColocalization` | 629–690 | First-label cell-type overlay plus normalized KDE; not a formal colocalization statistic. |
| `TransformBarcodes`, `NucleiSegmentationScript` | 695–745 | Parent→child bin names and printed segmentation command; not count rebinning/segmentation execution. |
| `geom_spatial`, `%!in%` | 749–768 | Image grob overlay and negated membership. |
| `EnrichRBarPlot`, `EnrichRDotPlot` | 385–418, 874–909 | Enrichr marker-list analysis and visualization; remote resource/version provenance needed. |
| `PlotInteraction`, `PlotInteractionGraph` | 771–851, 916–1011 | Chord/network plots of retained interaction counts; graph helper derives from CellChat visualization but does not run CellChat. |
| `ColorPalette`, `ColorsClusters`, `ColorsExtra`, `color_distance`, `most_different_colors` | 92–103, 252–301, 854–872, 1014–1039 | Publication palettes and color selection, no biological inference. |
| `SpatialAccuracy` | 1042–1128 | 500 µm square zooms with marker/UMI expression; not the paper's quantitative mask-distance assay. |

## Software evidence and execution gates

**Paper versions:** Space Ranger **3.0**; Cell Ranger **8.0.0**; Seurat **v5** (minor version not specified here); QuPath **0.4.4**; Loupe Browser **8.0**; LIANA **0.1.12**; Xenium Onboard Analysis **2.0.0**. The reporting summary (main PDF page 26, Data analysis) additionally specifies **“spacrxr v2.2.1”** and **StarDist v0.9.0**, alongside Seurat v5 and LIANA v0.1.12. “spacrxr” is the source spelling; interpreting it as spacexr is supported by Methods and `library(spacexr)` in Deconvolution.R. These are historical study versions, not recommended current defaults. [Methods Sec11–24 and reporting summary][paper]

**YAML pins:** Python **3.11.9** (line 327), StarDist **0.9.0** (372), TensorFlow CPU **2.15.0** (380–382), csbdeep **0.8.0** (73), GeoPandas **0.14.3** (109–110), Shapely **2.0.4** (362), Scanpy **1.10.1** (353), AnnData **0.10.7** (11), NumPy **1.26.4** (281), pandas **2.2.2** (290), PyArrow **15.0.0** (316), SciPy **1.13.0** (356), tifffile **2024.4.18** (387). It contains Linux-specific build strings and a user-home prefix (441); adapt deliberately for another platform. [Environment YAML][env]

**No reviewed R lockfile or complete R/package-version manifest exists.** The reporting summary supplies selected downstream package versions, including the reported spacexr version above; it does not pin the modified PR commit or all transitive dependencies. README's library list is incomplete for all scripts (for example BPCells, Azimuth, spacexr, LIANA, enrichR and plotting helpers vary by file). Internal calls `Seurat:::ProjectData` and `ggplot2:::ggname` add compatibility risk. Record package versions, exact spacexr source/defaults, LIANA method/resource settings and session information in any actual run.

Static portability findings to resolve before executing:

1. **Paths and hidden session state.** `FlexOutPath` lacks trailing slash where concatenated with `aggregation.csv` (Flex line 22) and `filtered_feature_bc_matrix.h5` (Deconvolution lines 12/15); Flex expects `/count/filtered...` while deconvolution does not. Source paths alternate `~/Sections/AuxFunctions.R`, `~/Methods/AuxFunctions.R`, and README's repository path. Figure_6/7 use absolute `/Outputs/...` for CSVs. Replace with validated manifest paths and `file.path`, create output directories, and avoid overwriting input matrix stores.
2. **Merged workflow incomplete state.** Figure_3/SupplementalFigure_6 call BPCells without loading it, write every sample to `getwd()` with `overwrite=TRUE`, reopen undefined `PathX`, supply an unfilled metadata list, and later use undefined `MetaData.merged`. Figure_3 expression zooms switch from `DF` to undefined `bcsHD` and use P2 centers while loading P1 (lines 239–260). Verify unique disk stores and sample barcode mapping rather than executing sequentially as written.
3. **Periphery/manifests.** Figure_4 line 65 uses undefined `bcDF`; later its macrophage loop expects `BarcodeDF`, `Tumor` and `PathPeriphery` absent from the initial manifest. Its saved `PatientCRC1_TME_Barcodes.rds` naming differs from Figure_5's expected `P1CRC_TME_Barcodes.rds`. Figure_6/SupplementalFigure_8 fallback periphery branches likewise use undefined `bcDF`. Repair and check tumor/periphery visualization.
4. **Downstream joins and defaults.** Fix the RCTD second-label/weight defects, segmentation CSV/CLI/crop defects, and avoid blanket `na.omit()` removing bins because an unrelated or intentionally missing field is NA. Figure_5 LIANA plotting references undefined `SampleInfo` although its manifest is `SampleData` (lines 452, 466–468). Marker-derived macrophage labels require explicit behavior when SPP1 is missing or >2 clusters occur.
5. **Other figure blockers.** SupplementalFigure_7 line 20 fails parsing; its per-sample `open_matrix_dir(getwd())` is underspecified. Figure_6/SupplementalFigure_4/8 initialize a list then `rbind` data frames instead of assigning list elements and binding once; SupplementalFigure_8 derives all periphery labels from only final-loop `Ix`. SupplementalFigure_9 passes three path values in its later single-sample branch. These require correction and small fixture checks before large data execution.
6. **Benchmark scope.** Figure_2d/SupplementalFigure_1 describe matched-area comparisons but contain no ROI subsetting and omit explicit Spearman mode, unlike SupplementalFigure_10. The latter computes filtered aligned Xenium coordinates but sums the whole matrix, has a faulty lower-y filter (line 126), assigns a data-frame object to coordinate maxima (lines 78/100), and reuses stale `im_dims` in the column loop. Reproduce matched spatial domains explicitly before claiming paper-comparable sensitivity.

**Recommended validation for a future run:** barcode/gene alignment and sample IDs; count/coordinate/image units; class and UMI-filter attrition tables; annotated tumor/periphery overlays; immutable full-image nuclei masks and known 2 µm mappings; macrophage marker checks; comparison with published metadata; patient-stratified summaries; explicit figure export and provenance. These are recommendations, not steps executed during this review. Do not claim full numerical reproduction, runtime performance or repaired scripts on the basis of static inspection.

[paper]: https://www.nature.com/articles/s41588-025-02193-3
[readme]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/README.md
[aux]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Methods/AuxFunctions.R
[flex]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Methods/FlexSingleCell.R
[deconv]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Methods/Deconvolution.R
[seg]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Methods/NucleiSegmentation.py
[env]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Methods/environment_nucleisegmentation.yml
[f2]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/Figure_2d.R
[f3]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/Figure_3.R
[f4]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/Figure_4.R
[f5]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/Figure_5.R
[f6]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/Figure_6.R
[f7]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/Figure_7.R
[s1]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/SupplementalFigure_1.R
[s3]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/SupplementalFigure_3.R
[s4]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/SupplementalFigure_4.R
[s5]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/SupplementalFigure_5.R
[s6]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/SupplementalFigure_6.R
[s7]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/SupplementalFigure_7.R
[s8]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/SupplementalFigure_8.R
[s9]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/SupplementalFigure_9.R
[s10]: https://github.com/10XGenomics/HumanColonCancer_VisiumHD/blob/df5801cf5e681b33b5026626989a7635fdf26b99/Figures/SupplementalFigure_10.R
