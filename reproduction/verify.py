"""Reproduction integrity checks; no stellar solver is called."""
import hashlib,json
from pathlib import Path
import numpy as np
import h5py
from .data import ROOT,DATA,record,array
from .tables import generate,TABLE_NAMES
from .processing import g1_stable,tau_pts,spliced_freq,spliced_cowl

ASSETS=('FIG1_kaon_buoyancy_fractions','FIG2_kaon_MR','FIG3a_kaon_freq','FIG3b_kaon_damping',
        'FIG4_hypdelta_buoyancy_fractions','FIG5_hypdelta_MR','g1_paperstyle_can','tau_paperstyle_can',
        'FIG7_strongD','FIG8_tidal_dphi','ddme2_appendix_robustness')

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def check_inputs():
    manifest=json.loads((ROOT/'reference/input_manifest.json').read_text())
    for relative,expected in manifest.items():
        if digest(ROOT/relative)!=expected:raise ValueError(f'Input hash mismatch: {relative}')
    return len(manifest)

def check_numbers():
    actual=generate();expected=json.loads((ROOT/'reference/table_cells.json').read_text());count=0
    for n,rows in actual.items():
        if rows!=expected[str(n)]['rows']:raise ValueError(f'Published table {n} does not match')
        count+=sum(map(len,rows))
    with h5py.File(DATA/'bigapple.h5') as f:
        for tag in f['g1']:
            mass,frequency=g1_stable(tag)
            assert np.all(np.diff(mass)>0) and np.all(np.isfinite(frequency)) and np.all(frequency>0)
        for tag in f['tau']:
            values=tau_pts(tag)
            assert np.all(values[:,1]>0) and np.all(np.diff(values[:,0])>0)
    exact=record('exact_points.json')['points']
    for tag in ('ka_UK100','ka_UK120','ka_UK140','ka_UK160'):
        a,b=exact[tag+':term'],exact[tag+'_Keq:term']
        assert a['M']==b['M'] and a['R']==b['R']
    assert record('structure.json')['npemu']['terminal_kind']=='physical_TOV_max'
    assert all(record('structure.json')[x]['terminal_kind']=='EOS_validity_endpoint'
               for x in ('ny','ndelta','nydelta','ka_UK140','ka_UK160'))
    tidal=record('published_tidal_points.json')['points']
    assert len(tidal)==14 and max(r['phase_rad'] for r in tidal)==.00141
    assert not any(r['tag']=='nydelta' and r['M']>=2 for r in tidal)
    expected_rows=record('tidal_resolved.json')
    for r in tidal:
        candidates=[x for x in expected_rows if x['tag']==r['tag'] and round(x['M'],1)==round(r['M'],1)]
        assert len(candidates)==1 and candidates[0]['phase_rad']==r['phase_rad']
    return {'tables':len(actual),'display_cells':count,'published_tidal_points':len(tidal),
            'frozen_fastK_background_pairs':4,'published_display_records':len(record('published_display.json'))}

def check_outputs(out):
    products=[]
    for stem in ASSETS:
        for extension in ('png','pdf','curves.json'):
            p=out/'figures'/f'{stem}.{extension}'
            assert p.is_file() and p.stat().st_size>100,p
            products.append(p)
    for n,stem in TABLE_NAMES.items():
        for extension in ('json','tex'):
            p=out/'tables'/f'table{n}_{stem}.{extension}'
            assert p.is_file() and p.stat().st_size>20,p
            products.append(p)
    return {str(p.relative_to(out)):digest(p) for p in products}
