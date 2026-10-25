#!/usr/bin/env python3
"""Validate a SpaCET export and write sparse gsMap AnnData; no scientific re-estimation."""
from __future__ import annotations
import argparse
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path
import tempfile
import inspect
import anndata as ad
import numpy as np
import pandas as pd
from scipy import io, sparse


def table(path):
    with open(path, newline='', encoding='utf-8') as f:
        header = next(csv.reader(f, delimiter='\t'), [])
    if not header or len(set(header)) != len(header):
        raise ValueError(f'Empty or duplicate table headers: {path}')
    return pd.read_csv(path, sep='\t', dtype=str, keep_default_na=False)


def unique(values, what):
    values = pd.Index(values.astype(str) if hasattr(values, 'astype') else values)
    if len(values) == 0 or values.has_duplicates or any(not str(x).strip() for x in values):
        raise ValueError(f'{what} must be nonempty, unique and contain no blank IDs')
    if any(str(x)!=str(x).strip() for x in values):
        raise ValueError(f'{what} contain leading/trailing whitespace; resolve explicitly')
    return values


def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def indexed(frame, id_col, target, what):
    if id_col not in frame:
        raise ValueError(f'{what}: missing {id_col}')
    idx = unique(frame[id_col], what)
    if set(idx) != set(target):
        raise ValueError(f'{what}: spot IDs differ; missing={len(set(target)-set(idx))}, extra={len(set(idx)-set(target))}')
    return frame.set_index(id_col).loc[target]


def build(bundle, output, label_mode='none', min_fraction=None, min_margin=None,
          max_unidentifiable=None, reviewed_labels=None):
    bundle, output = Path(bundle), Path(output)
    audit_path = output.with_suffix('.audit.json')
    if output.exists() or audit_path.exists():
        raise ValueError('Output or audit exists; use a fresh path')
    required = ['counts.mtx','genes.tsv','spots.tsv','fractions.tsv','lineage.tsv','metadata.json']
    for name in required:
        if not (bundle/name).is_file():
            raise ValueError(f'Missing export file: {name}')
    meta = json.loads((bundle/'metadata.json').read_text())
    for key in ['sample_id','organism','platform','observation_unit','coordinate_units','coordinate_convention']:
        if not isinstance(meta.get(key),str) or not meta[key].strip():
            raise ValueError(f'metadata.json requires nonblank string {key}')
    if meta['organism'].lower() != 'human':
        raise ValueError('This bridge targets human ST; prepare explicit homolog mapping for other species')
    if meta['observation_unit'] not in ['spot','bin','cell']:
        raise ValueError('observation_unit must be spot, bin or cell')
    if meta['observation_unit']=='bin':
        size=meta.get('bin_size_um')
        if not isinstance(size,(float,int)) or not np.isfinite(size) or size<=0:
            raise ValueError('Binned data require a positive numeric bin_size_um')
    genes=table(bundle/'genes.tsv')
    if 'gene_symbol' not in genes:
        raise ValueError('genes.tsv requires gene_symbol')
    gene_ids=unique(genes.gene_symbol,'Gene symbols')
    if gene_ids.str.match(r'^ENS[A-Z]*G[0-9]+(?:\.[0-9]+)?$').any():
        raise ValueError('Ensembl gene IDs detected: explicitly map to reference-compatible symbols first')
    spots=table(bundle/'spots.tsv')
    for col in ['spot_id','source_id','source_id_kind','x','y']:
        if col not in spots:
            raise ValueError(f'spots.tsv requires {col}')
    spot_ids=unique(spots.spot_id,'SpaCET spot IDs')
    source_ids=unique(spots.source_id,'Source IDs')
    if '::' in meta['sample_id'] or any('::' in s for s in source_ids):
        raise ValueError('The namespace delimiter :: is reserved; choose unambiguous sample/source IDs')
    if not spots.source_id_kind.isin(['barcode','spacet_id','cell_id']).all():
        raise ValueError('Unsupported source_id_kind')
    coords=spots[['x','y']].apply(pd.to_numeric,errors='raise').to_numpy(dtype=float)
    if not np.isfinite(coords).all():
        raise ValueError('Coordinates must be finite')
    # New SciPy versions expose spmatrix; avoid a changing-default warning.
    mm_options={'spmatrix':False} if 'spmatrix' in inspect.signature(io.mmread).parameters else {}
    counts=sparse.csr_matrix(io.mmread(bundle/'counts.mtx',**mm_options).T)
    counts.sum_duplicates()
    counts.eliminate_zeros()
    if counts.shape!=(len(spot_ids),len(gene_ids)):
        raise ValueError('counts.mtx must be genes by spots in genes.tsv/spots.tsv order')
    if not np.isfinite(counts.data).all() or (counts.data<0).any() or not np.allclose(counts.data,np.rint(counts.data),rtol=0,atol=1e-6):
        raise ValueError('Counts must be finite, nonnegative, unnormalized integer counts')
    if np.any(np.asarray(counts.sum(axis=1)).ravel()==0):
        raise ValueError('Zero-count spots detected; perform explicit QC before export')
    counts=counts.astype(np.float64)
    frac=indexed(table(bundle/'fractions.tsv'),'spot_id',spot_ids,'Fractions')
    if frac.shape[1]==0:
        raise ValueError('No fraction columns')
    frac=frac.apply(pd.to_numeric,errors='raise').astype(float)
    if not np.isfinite(frac.to_numpy()).all() or ((frac.to_numpy()<0)|(frac.to_numpy()>1)).any():
        raise ValueError('Fractions must be finite and within [0,1]')
    tree=table(bundle/'lineage.tsv')
    if not {'parent','child'}.issubset(tree.columns) or tree.empty:
        raise ValueError('lineage.tsv requires parent and child rows from Ref$lineageTree')
    if tree[['parent','child']].apply(lambda c:c.str.strip().eq('')).any().any() or tree.duplicated(['parent','child']).any():
        raise ValueError('Lineage tree contains blank or duplicate entries')
    parents=list(dict.fromkeys(tree.parent))
    children=set(tree.loc[tree.parent!=tree.child,'child'])
    if set(parents)&children:
        raise ValueError('Parent/sublineage overlap in the proposed major lineage set')
    if 'Unidentifiable' in parents:
        raise ValueError('Unidentifiable must not be a major cell lineage')
    if 'Malignant' in frac and 'Malignant' not in parents:
        parents.insert(0,'Malignant')
    if set(parents)-set(frac.columns):
        raise ValueError('Some major lineages are missing from the fraction matrix')
    if set(tree.child)-set(frac.columns):
        raise ValueError('Some reference sublineages are missing from the fraction matrix')
    if tree.groupby('child').parent.nunique().gt(1).any():
        raise ValueError('A child belongs to more than one parent in lineage.tsv')
    major=frac[parents].to_numpy()
    major_total=major.sum(axis=1)
    if 'Unidentifiable' in frac:
        major_total=major_total+frac.Unidentifiable.to_numpy()
    if np.any(major_total>1+1e-5):
        raise ValueError('Major-lineage fractions plus Unidentifiable exceed one; check hierarchy and export')
    order=np.argsort(-major,axis=1,kind='stable')
    top=major[np.arange(len(spots)),order[:,0]]
    second=major[np.arange(len(spots)),order[:,1]] if len(parents)>1 else np.zeros(len(spots))
    margin=top-second
    tie=np.isclose(margin,0,atol=1e-12,rtol=0) if len(parents)>1 else top==0
    dominant=np.array(parents,dtype=object)[order[:,0]]
    dominant[(top<=0)|tie]=None
    obs_names=pd.Index([meta['sample_id']+'::'+s for s in source_ids],name='spot')
    obs=pd.DataFrame(index=obs_names)
    obs['spacet_spot_id']=spot_ids.to_numpy()
    obs['source_id']=source_ids.to_numpy()
    obs['source_id_kind']=spots.source_id_kind.to_numpy()
    for key in ['sample_id','patient_id','section_id','organism','platform','observation_unit','donor_ancestry']:
        value=meta.get(key)
        obs[key]='unknown' if value is None or value=='' else str(value)
    obs['spacet_major_dominant']=pd.Categorical(dominant)
    obs['spacet_major_top_fraction']=top
    obs['spacet_major_margin']=margin
    obs['spacet_major_tie']=tie
    obs['spacet_unidentifiable']=frac['Unidentifiable'].to_numpy() if 'Unidentifiable' in frac else np.nan
    expected_drop=[]
    label_counts={}
    if label_mode=='dominant-major':
        for value,name in [(min_fraction,'min_fraction'),(min_margin,'min_margin'),(max_unidentifiable,'max_unidentifiable')]:
            if value is None or not np.isfinite(value) or not 0<=value<=1:
                raise ValueError(f'{name} must be explicitly set within [0,1]')
        if 'Unidentifiable' not in frac:
            raise ValueError('Unidentifiable is required for this policy; use reviewed labels for custom references')
        labels=dominant.copy()
        keep=(top>=min_fraction)&(margin>=min_margin)&~tie&(top>0)&(frac.Unidentifiable.to_numpy()<=max_unidentifiable)
        labels[~keep]=None
    elif label_mode=='reviewed':
        if reviewed_labels is None:
            raise ValueError('reviewed mode requires --reviewed-labels')
        reviewed=indexed(table(reviewed_labels),'spot_id',spot_ids,'Reviewed labels')
        if 'annotation' not in reviewed:
            raise ValueError('Reviewed labels require annotation column')
        labels=reviewed.annotation.str.strip().to_numpy(dtype=object)
        labels[labels=='']=None
    elif label_mode!='none':
        raise ValueError('Unsupported label mode')
    if label_mode!='none':
        obs['gsmap_annotation']=pd.Categorical(labels)
        label_counts={str(k):int(v) for k,v in obs.gsmap_annotation.value_counts().items()}
        eligible=obs.gsmap_annotation.notna() & obs.gsmap_annotation.map(label_counts).astype(float).ge(30)
        obs['gsmap_annotation_eligible_at_inspected_commit']=eligible.to_numpy()
        expected_drop=obs.index[~eligible].tolist()
    frac.index=obs_names
    var=genes.set_index('gene_symbol')
    var.index=gene_ids
    result=ad.AnnData(X=counts,obs=obs,var=var)
    result.layers['count']=counts.copy()
    result.obsm['spatial']=coords
    result.obsm['spacet_fractions']=frac
    hashes={n:digest(bundle/n) for n in required}
    if reviewed_labels:
        hashes['reviewed_labels']=digest(Path(reviewed_labels))
    audit={'sample_id':meta['sample_id'],'n_spots':len(spots),'n_genes':len(gene_ids),
           'n_fraction_columns':frac.shape[1],'major_lineages':parents,
           'coordinate_units':meta['coordinate_units'],'coordinate_convention':meta['coordinate_convention'],
           'duplicate_coordinate_rows':int(pd.DataFrame(coords).duplicated().sum()),
           'major_plus_unknown_total_range':[float(major_total.min()),float(major_total.max())],
           'label_policy':{'mode':label_mode,'min_fraction':min_fraction,'min_margin':min_margin,'max_unidentifiable':max_unidentifiable},
           'label_counts':label_counts,'expected_gsmap_annotation_drop_ids':expected_drop,
           'expected_gsmap_annotation_drop_n':len(expected_drop),
           'gsmap_filter_source_commit':'ffb561db3e5a92ddabf7dc7b8f203c25e4d9f627',
           'input_sha256':hashes,'versions':{p:importlib.metadata.version(p) for p in ['anndata','numpy','pandas','scipy','h5py']},
           'scope':'Format and identity checks only; no biological validation or gsMap execution.'}
    result.uns['spacet_bridge']={'metadata_json':json.dumps(meta),'audit_json':json.dumps(audit),'lineage':tree}
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        temp=Path(tmp)/'result.h5ad'
        result.write_h5ad(temp,compression='gzip')
        check=ad.read_h5ad(temp)
        if not check.obs_names.equals(obs_names) or check.shape!=result.shape:
            raise RuntimeError('h5ad round-trip identity check failed')
        temp.rename(output)
    audit_path.write_text(json.dumps(audit,indent=2)+'\n')
    return audit


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--label-mode',choices=['none','dominant-major','reviewed'],default='none')
    p.add_argument('--min-fraction',type=float)
    p.add_argument('--min-margin',type=float)
    p.add_argument('--max-unidentifiable',type=float)
    p.add_argument('--reviewed-labels')
    args=p.parse_args()
    print('[1/2] Validating SpaCET export and building sparse AnnData',flush=True)
    audit=build(**vars(args))
    print(f"[2/2] Saved {args.output}: {audit['n_spots']} spots × {audit['n_genes']} genes",flush=True)
    if args.label_mode!='none':
        print(f"Annotated gsMap would exclude {audit['expected_gsmap_annotation_drop_n']} spots at the inspected commit. Review the audit before running.",flush=True)


if __name__=='__main__':
    main()
