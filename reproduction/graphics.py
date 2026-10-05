"""Deterministic output files and a compact plot-coordinate audit record."""
import json
from pathlib import Path
import numpy as np
META={'Creator':'Matplotlib','CreationDate':None,'ModDate':None}

def save_figure(fig,out,name,dpi=200,**kwargs):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    fig.savefig(out/f'{name}.png',dpi=dpi,**kwargs)
    fig.savefig(out/f'{name}.pdf',metadata=META,**kwargs)
    curves=[]
    for panel,ax in enumerate(fig.axes):
        for index,line in enumerate(ax.lines):
            x=np.asarray(line.get_xdata(),float);y=np.asarray(line.get_ydata(),float)
            curves.append(dict(panel=panel,index=index,x=x.tolist(),y=y.tolist()))
    # Diagnostic coordinates are in physical plotting units; NaN marks a break.
    clean=lambda a:[float(v) if np.isfinite(v) else None for v in a]
    for curve in curves:
        curve['x']=clean(curve['x']);curve['y']=clean(curve['y'])
    (out/f'{name}.curves.json').write_text(json.dumps(curves,separators=(',',':'),allow_nan=False)+'\n')
