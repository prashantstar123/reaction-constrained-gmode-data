"""Reproduce the accepted article's figures and tables from saved data."""
import argparse,importlib.metadata,json,platform,time
from pathlib import Path
import matplotlib.pyplot as plt
from .data import ROOT
from . import tables,verify,figures_basic,figures_modes,figures_tidal,figures_ddme2

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'output')
    parser.add_argument('--verify-only',action='store_true')
    args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    started=time.monotonic()
    print('Checking input hashes and published table values...',flush=True)
    count=verify.check_inputs();checks=verify.check_numbers()
    if not args.verify_only:
        tables.write(out/'tables')
        for name,function in (('Figures 1, 2, 4, 5',figures_basic.render),('Figure 3',figures_modes.render_kaon),
                ('Figure 6',figures_modes.render_baryonic),('Figure 7',figures_modes.render_reaction),
                ('Figure 8',figures_tidal.render),('Figure 9',figures_ddme2.render)):
            print('Rendering '+name+'...',flush=True)
            with plt.rc_context(plt.rcParamsDefault):function(out/'figures')
    outputs=verify.check_outputs(out)
    if args.verify_only:
        previous=json.loads((out/'verification.json').read_text())
        if previous['outputs']!=outputs:raise ValueError('Output hash mismatch relative to completed run')
    report={'status':'PASS','scope':'Saved-data reproduction, not a new solver calculation',
            'input_manifest_entries':count,'checks':checks,'outputs':outputs,
            'python':platform.python_version(),'platform':platform.system(),
            'packages':{line.split('==')[0]:importlib.metadata.version(line.split('==')[0])
                        for line in (ROOT/'requirements.lock').read_text().splitlines() if '==' in line},
            'elapsed_seconds':round(time.monotonic()-started,3)}
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 9 numbered figures (11 PNG/PDF assets), 8 tables, and all reference checks.',flush=True)

if __name__=='__main__':main()
