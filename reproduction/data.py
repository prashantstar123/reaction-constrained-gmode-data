"""Portable read-only access to losslessly stored published numerical records."""
from functools import lru_cache
from pathlib import Path
import json
import h5py
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

@lru_cache(None)
def _array(file,key):
    with h5py.File(DATA/file,'r') as f:return f[key][:]

def array(kind,tag,file='bigapple.h5'):
    return _array(file,f'{kind}/{tag}').copy()

def attributes(kind,tag,file='bigapple.h5'):
    with h5py.File(DATA/file,'r') as f:return dict(f[f'{kind}/{tag}'].attrs)

def record(name):
    return json.loads((DATA/name).read_text())
