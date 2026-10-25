# Upstream SpaCET workflow

## Version and inputs

Inspected SpaCET 1.4.0 at `eed9666a0d76507d46e70e5a168da2504086db0e`. Its README recommends R >=4.2, while DESCRIPTION allows >=3.5; use the recommended modern R environment and check dependency compatibility. Installation can require Bioconductor packages and compiled dependencies. H5 and segmented-output readers call Seurat even though it is not in the inspected Imports list; check Seurat explicitly when using those paths. MEX reading avoids that particular H5-reader dependency. Arrow is used for HD parquet coordinates.

```r
# Run in the intended R environment if installation is required.
# install.packages("remotes")
remotes::install_github("data2intelligence/SpaCET",
                       ref="eed9666a0d76507d46e70e5a168da2504086db0e",
                       upgrade="never")
library(SpaCET)
packageVersion("SpaCET")
formals(create.SpaCET.object.10X)
formals(SpaCET.deconvolution)
```

Standard Visium expects one matrix (MEX or H5), spatial positions (`tissue_positions.csv` or headerless `tissue_positions_list.csv`), scalefactors and a tissue image. Pass a single `binned_outputs/square_*um` directory for HD bins. Current source also routes segmented HD outputs through Seurat's segmentation reader. Support in code is not a benchmark of every HD resolution; choose binning from coverage and validate empirically. A 2 µm bin is not a cell.

For a custom input use `create.SpaCET.object(counts=..., spotCoordinates=..., metaData=..., imagePath=NA, platform=..., organism="human")`. Counts are genes × spots; coordinates and metadata must be in exactly the column order of counts. Explicitly reorder before construction.

## Analysis recipe

```r
library(SpaCET)
set.seed(2024)
sample_id <- "sample01"
input_dir <- "/path/to/one/sample/outs"
output_dir <- "/path/to/new/output/sample01"
stopifnot(!dir.exists(output_dir))
dir.create(output_dir, recursive=TRUE)
message("[1/4] Read one tissue section")
obj <- create.SpaCET.object.10X(dataPath=input_dir,
                              platform="Visium", organism="human")
before_qc <- ncol(obj@input$counts)

# Select and document a threshold appropriate for this sample/platform.
min_genes <- 100L # illustrative, not a universal recommendation
message("[2/4] QC")
obj <- SpaCET.quality.control(obj, min.genes=min_genes)
stopifnot(ncol(obj@input$counts)>0)

# Verify the installed cancer dictionary. Do not infer compatibility from TCGA alone.
dict <- new.env(parent=emptyenv())
load(system.file("extdata","cancerDictionary.rda",package="SpaCET"), envir=dict)
keys <- unique(c(names(dict$cancerDictionary$CNA), names(dict$cancerDictionary$expr)))
codes <- vapply(strsplit(keys,"_",fixed=TRUE), function(x) x[2], character(1))
cancer_type <- "SKCM"
stopifnot(cancer_type %in% codes)
message("[3/4] Tumor deconvolution")
obj <- SpaCET.deconvolution(obj, cancerType=cancer_type, coreNo=1)
# coreNo=1 is conservative; set it to the job's allocated cores when appropriate.
used_signature <- obj@results$deconvolution$malRes$sig
message("Selected signature: ", paste(used_signature, collapse=" / "))
message("[4/4] Save results and provenance")
saveRDS(obj, file.path(output_dir,"spacet.rds"))
saveRDS(list(sample_id=sample_id, min_genes=min_genes, before_qc=before_qc,
             after_qc=ncol(obj@input$counts), cancer_type=cancer_type,
             selected_signature=used_signature,
             version=as.character(packageVersion("SpaCET"))),
        file.path(output_dir,"settings.rds"))
capture.output(sessionInfo(),file=file.path(output_dir,"sessionInfo.txt"))
SpaCET.visualize.spatialFeature(obj, spatialType="CellFraction",
  spatialFeatures=c("Malignant","CAF","Macrophage"),
  sameScaleForFraction=TRUE)
```

Confirm requested plot categories exist in `rownames(obj@results$deconvolution$propMat)`. Perform QC before deconvolution; changing the spot set afterward requires synchronized results and a documented rerun. Preserve the object's full input counts for gsMap, not only SpaCET reference-marker genes. Native automatic signature selection can try tumor-specific CNA, tumor-specific expression and then PANCAN expression. Record `malRes$sig` and any alternate large-dataset branch actually used; a requested SKCM code does not prove an SKCM-specific signature was used. Do not force a signature just to hide a fallback.

## Optional analyses

- Custom reference: inspect `SpaCET.deconvolution.matched.scRNAseq` formals and the official oldST_PDAC tutorial. Validate genes, raw scRNA counts, per-cell annotation and parent/child tree. Decide explicitly whether malignant cells are included in that reference.
- Malignant substates: inspect `SpaCET.deconvolution.malignant`; do not conflate states with independent malignant cell types.
- Interaction: follow official `visium_BC` tutorial calls for `SpaCET.CCI.colocalization`, `SpaCET.CCI.LRNetworkScore` and `SpaCET.CCI.cellTypePair`. Optional interface and distance functions depend on upstream results and appropriate geometry.
- Major/sublineage descriptive labels: `SpaCET.calculate.mostAbundantCellType` writes `Estimated_MajorLineage` and `Estimated_SubLineage` in input metadata. These unqualified maxima are not the bridge's filtered modelling labels.

Use the current tutorials linked in [sources](sources.md), not guessed argument names.
