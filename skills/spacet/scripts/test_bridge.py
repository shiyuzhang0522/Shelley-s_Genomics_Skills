#!/usr/bin/env python3
"""Synthetic regression tests for identities, hierarchy, labels and sparse export."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import anndata as ad
import numpy as np
import pandas as pd
from scipy import io, sparse
from spacet_to_gsmap import build


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.bundle=self.root/'bundle'
        self.bundle.mkdir()
        self.ids=[f'{i}x0' for i in range(34)]
        self.counts=sparse.csr_matrix(np.array([[1,2,0],[0,3,4],[2,0,1]]*11+[[1,1,1]]))
        io.mmwrite(self.bundle/'counts.mtx',self.counts.T)
        self.save('genes',pd.DataFrame({'gene_symbol':['CD3D','COL1A1','MLANA']}))
        self.save('spots',pd.DataFrame({'spot_id':self.ids,'source_id':[f'BC{i}-1' for i in range(34)],
                                      'source_id_kind':'barcode','x':range(34),'y':np.zeros(34)}))
        # All parent and child columns survive; parent+child sums can exceed one.
        f=pd.DataFrame({'spot_id':self.ids,'Malignant':0.8,'T cell':0.1,'CAF':0.05,
                        'T CD4':0.07,'T CD8':0.03,'Unidentifiable':0.05})
        f.loc[30:,['Malignant','T cell','CAF','T CD4','T CD8','Unidentifiable']]=[
            [0.2,0.6,0.1,0.4,0.2,0.1], # T group <30
            [0.2,0.6,0.1,0.4,0.2,0.1],
            [0.45,0.45,0.05,0.3,0.15,0.05], # tie
            [0.2,0.1,0.1,0.08,0.02,0.6]] # unknown dominates
        self.save('fractions',f.iloc[::-1]) # deliberate row shuffle
        self.save('lineage',pd.DataFrame({'parent':['T cell','T cell','CAF'],
                                         'child':['T CD4','T CD8','CAF']}))
        self.meta={'sample_id':'S1','patient_id':'P1','section_id':'A','organism':'human',
                   'platform':'Visium','observation_unit':'spot','coordinate_units':'um',
                   'coordinate_convention':'x/y as exported'}
        self.save_meta()

    def tearDown(self):
        self.temp.cleanup()

    def save(self,name,frame):
        frame.to_csv(self.bundle/(name+'.tsv'),sep='\t',index=False)

    def read(self,name):
        return pd.read_csv(self.bundle/(name+'.tsv'),sep='\t',keep_default_na=False)

    def save_meta(self):
        (self.bundle/'metadata.json').write_text(json.dumps(self.meta))

    def run_build(self,**kw):
        return build(self.bundle,self.root/'result.h5ad',**kw)

    def test_sparse_roundtrip_and_join(self):
        audit=self.run_build()
        a=ad.read_h5ad(self.root/'result.h5ad')
        self.assertTrue(sparse.issparse(a.layers['count']))
        np.testing.assert_array_equal(a.layers['count'].toarray(),self.counts.toarray())
        self.assertEqual(a.obs_names[0],'S1::BC0-1')
        self.assertEqual(a.obs_names[-1],'S1::BC33-1')
        self.assertEqual(a.obs.spacet_spot_id.iloc[0],'0x0')
        self.assertAlmostEqual(a.obsm['spacet_fractions'].iloc[0]['Malignant'],0.8)
        self.assertAlmostEqual(a.obsm['spacet_fractions'].iloc[-1]['Unidentifiable'],0.6)
        self.assertNotIn('gsmap_annotation',a.obs)
        self.assertNotIn('T CD4',audit['major_lineages'])
        self.assertEqual(a.obsm['spacet_fractions'].shape,(34,6))
        np.testing.assert_array_equal(a.obsm['spatial'][:,0],np.arange(34))

    def test_annotation_audit_and_ties(self):
        audit=self.run_build(label_mode='dominant-major',min_fraction=0.5,min_margin=0.1,max_unidentifiable=0.3)
        a=ad.read_h5ad(self.root/'result.h5ad')
        self.assertEqual(audit['label_counts'],{'Malignant':30,'T cell':2})
        self.assertEqual(audit['expected_gsmap_annotation_drop_n'],4)
        self.assertEqual(a.n_obs,34) # report only, never silently filter
        self.assertTrue(pd.isna(a.obs.gsmap_annotation.iloc[32]))
        self.assertTrue(a.obs.spacet_major_tie.iloc[32])
        self.assertTrue(pd.isna(a.obs.gsmap_annotation.iloc[33]))

    def test_reviewed_labels_shuffled_and_missing(self):
        p=self.root/'labels.tsv'
        pd.DataFrame({'spot_id':self.ids[::-1],'annotation':['']+['region']*33}).to_csv(p,sep='\t',index=False)
        audit=self.run_build(label_mode='reviewed',reviewed_labels=p)
        self.assertEqual(audit['expected_gsmap_annotation_drop_n'],1)
        self.assertEqual(audit['expected_gsmap_annotation_drop_ids'],['S1::BC33-1'])

    def test_cli(self):
        r=subprocess.run([sys.executable,str(Path(__file__).with_name('spacet_to_gsmap.py')),
                          '--bundle',str(self.bundle),'--output',str(self.root/'cli.h5ad')],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertIn('[2/2]',r.stdout)

    def test_mismatched_fraction_ids(self):
        f=self.read('fractions'); f.loc[0,'spot_id']='OTHER'; self.save('fractions',f)
        with self.assertRaisesRegex(ValueError,'spot IDs differ'): self.run_build()

    def test_duplicate_barcodes(self):
        f=self.read('spots'); f.loc[0,'source_id']=f.loc[1,'source_id']; self.save('spots',f)
        with self.assertRaisesRegex(ValueError,'Source IDs'): self.run_build()

    def test_duplicate_genes(self):
        f=self.read('genes'); f.loc[0,'gene_symbol']=f.loc[1,'gene_symbol']; self.save('genes',f)
        with self.assertRaisesRegex(ValueError,'Gene symbols'): self.run_build()

    def test_nonfinite_fraction(self):
        f=self.read('fractions'); f.loc[0,'Malignant']=np.inf; self.save('fractions',f)
        with self.assertRaisesRegex(ValueError,'Fractions must'): self.run_build()

    def test_log_normalized_counts(self):
        io.mmwrite(self.bundle/'counts.mtx',self.counts.T*0.5)
        with self.assertRaisesRegex(ValueError,'integer counts'): self.run_build()

    def test_zero_spot(self):
        c=self.counts.toarray(); c[0,:]=0; io.mmwrite(self.bundle/'counts.mtx',sparse.csr_matrix(c.T))
        with self.assertRaisesRegex(ValueError,'Zero-count'): self.run_build()

    def test_overlapping_parent_sublineage(self):
        f=self.read('lineage'); f.loc[len(f)]=['T CD4','T CD4']; self.save('lineage',f)
        with self.assertRaisesRegex(ValueError,'Parent/sublineage'): self.run_build()

    def test_thresholds_must_be_explicit(self):
        with self.assertRaisesRegex(ValueError,'explicitly set'): self.run_build(label_mode='dominant-major')

    def test_hd_bin_metadata(self):
        self.meta['observation_unit']='bin'; self.save_meta()
        with self.assertRaisesRegex(ValueError,'bin_size_um'): self.run_build()

    def test_no_overwrite(self):
        self.run_build()
        with self.assertRaisesRegex(ValueError,'exists'): self.run_build()

    def test_missing_child(self):
        f=self.read('fractions').drop(columns='T CD4'); self.save('fractions',f)
        with self.assertRaisesRegex(ValueError,'sublineages are missing'): self.run_build()

    def test_major_total_over_one(self):
        f=self.read('fractions'); f.loc[0,'Malignant']=0.9; self.save('fractions',f)
        with self.assertRaisesRegex(ValueError,'exceed one'): self.run_build()

    def test_all_missing_reviewed_annotations(self):
        p=self.root/'blank.tsv'
        pd.DataFrame({'spot_id':self.ids,'annotation':['']*34}).to_csv(p,sep='\t',index=False)
        audit=self.run_build(label_mode='reviewed',reviewed_labels=p)
        self.assertEqual(audit['expected_gsmap_annotation_drop_n'],34)


if __name__=='__main__':
    unittest.main(verbosity=2)
