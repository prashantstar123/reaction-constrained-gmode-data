"""Table summaries from frozen numerical records and adopted model inputs."""
import json
from pathlib import Path
import numpy as np
from .data import array,record

TABLE_NAMES={1:'model_parameters',2:'exotic_couplings',3:'kaon_summary',4:'kaon_channels',
             5:'baryonic_summary',6:'baryonic_channels',7:'tidal_response',8:'eos_comparison'}
LABELS={1:'tab:bigapple',2:'tab:exotic',3:'tab:eos_summary_kaon',4:'tab:kaon_chi',
        5:'tab:eos_summary',6:'tab:hypdelta_chi',7:'tab:tidal',8:'tab:ddme2_comparison'}
COLUMNS={1:['quantity','value','unit'],2:['sector','quantity','value'],
 3:['U_K_MeV','M_term_Msun','R_term_km','R_1p4_km','f_frozen_term_Hz','f_fastK_term_Hz','f_1p4_Hz','tau_frozen_term_yr','tau_fastK_term_yr','tau_1p4_yr'],
 4:['M_Msun','n_Bc_fm-3','frequency_Hz','chi_K','chi_leptons'],
 5:['composition','M_term_Msun','R_term_km','R_1p4_km','f_term_Hz','f_1p4_Hz','tau_term_yr','tau_1p4_yr'],
 6:['composition','M_Msun','frequency_Hz','chi_Delta','chi_hyperons','chi_leptons'],
 7:['composition','f_1p4_Hz','phase_1p4_rad','f_1p8_Hz','phase_1p8_rad','f_2p0_Hz','phase_2p0_rad'],
 8:['composition','EOS','M_comparison_Msun','f_frozen_Hz','f_reaction_Hz','frequency_ratio','local_retention_percent']}
COMPOSITIONS={'npemu':r'npe\mu','ndelta':r'npe\mu+\Delta','ny':r'npe\mu+Y','nydelta':r'npe\mu+Y+\Delta','ka_UK160':r'npe\mu+K^-'}

def model_tables():
    p=record('parameters.json');m=p['meson'];a=record('adopted_parameters.json');sat=a['saturation_targets']
    one=[[r'm_N',f'{a["nucleon_mass_MeV"]:.0f}','MeV']]
    for symbol,key in ((r'\sigma','s'),(r'\omega','w'),(r'\rho','r')):
        one.append([f'm_{symbol}',f'{m[f"m_{key}"]:.3f}','MeV'])
    for symbol,key in ((r'\sigma','s'),(r'\omega','w'),(r'\rho','r')):
        one.append([f'g_{{{symbol} N}}^{{2}}',f'{m[f"g_{key}N"]**2:.4f}','--'])
    one += [[r'\kappa',f'{m["kappa"]:.5f}','MeV'],[r'\lambda',f'{m["lam"]:.6f}','--'],
            [r'\zeta',f'{m["zeta"]:.6f}','--'],[r'\Lambda_v',f'{m["Lambda_v"]:.6f}','--']]
    one += [[label,f'{sat[key]:.3f}',unit] for label,key,unit in ((r'n_0','n0',r'fm^{-3}'),('E/A','EA','MeV'),('K','K','MeV'),('J','J','MeV'),('L','L','MeV'))]
    potentials=','.join(str(x) for x in sorted(map(int,p['kaon_couplings']),reverse=True))
    two=[[r'K^-',r'm_K',f'{a["kaon_mass_MeV"]:.1f}~MeV'],['',r'g_{\omega K}',r'g_{\omega N}/3'],
         ['',r'g_{\rho K}',r'g_{\rho N}'],['',r'U_K(n_0)',potentials+'~MeV']]
    for symbol,key in ((r'\Lambda','Lambda'),(r'\Sigma','Sigma'),(r'\Xi','Xi')):
        v=p['hyperon_U'][key]
        two.append([symbol,'U_'+symbol+'(n_0)',f'{v:+d}~MeV'])
    q=p['delta_ratios']
    two += [[r'\Delta',r'x_{\sigma\Delta}',f'{q["x_s"]:.2f}'],['',r'x_{\omega\Delta}',f'{q["x_w"]:.2f}'],
            ['',r'x_{\rho\Delta}',f'{q["x_r"]:.1f}'],['',r'g_{\phi\Delta}',f'{q["g_phi"]:.0f}'],
            ['',r'U_\Delta^{(N)}(n_0)',f'{p["saturation"]["U_Delta_pred"]:.1f}~MeV']]
    return one,two

def structural(tag,structures):
    s=structures[tag];terminal=s['terminal_kind']=='EOS_validity_endpoint'
    return (f'{s["M_end"] if terminal else s["Mmax"]:.3f}'+(r'^{\dagger}' if terminal else ''),
            f'{s["R_end"] if terminal else s["Rmax"]:.3f}',f'{s["R_1.4"]:.3f}')

def summary_tables():
    p=record('exact_points.json')['points'];structure=record('structure.json');base=p['npemu:1.4']
    tauformats={100:('.2f','.1f'),120:('.3f','.2f'),140:('.3f','.3f'),160:('.4f','.4f')}
    kaon=[]
    for uk in (0,100,120,140,160):
        tag=f'ka_UK{uk}';point=p[('npemu' if uk==0 else tag)+':term']
        if uk:
            reaction=p[tag+'_Keq:term'];ff=f'{reaction["f"]:.2f}'
            tf=format(point['tau'],tauformats[uk][0]);tr=format(reaction['tau'],tauformats[uk][1])
        else:ff=tr='--';tf=rf'{point["tau"]/1e5:.2f}\times10^{{5}}'
        kaon.append([str(-uk),*structural(tag,structure),f'{point["f"]:.2f}',ff,f'{base["f"]:.2f}',tf,tr,f'{base["tau"]:.0f}'])
    baryonic=[]
    for tag,taufmt in (('npemu',None),('ndelta','.3f'),('ny','.4f'),('nydelta','.4f')):
        term=p[tag+':term'];canonical=p[('npemu' if tag=='ny' else tag)+':1.4']
        tau=rf'{term["tau"]/1e5:.2f}\times10^{{5}}' if taufmt is None else format(term['tau'],taufmt)
        baryonic.append([COMPOSITIONS[tag],*structural(tag,structure),f'{term["f"]:.2f}',f'{canonical["f"]:.2f}',tau,
                        f'{canonical["tau"]:.0f}' if tag in ('npemu','ny') else f'{canonical["tau"]:.1f}'])
    return kaon,baryonic

def channel_tables():
    mr=array('mr','ka_UK120');order=np.argsort(mr[:,0])
    kaon=[]
    for row in array('chi','ka_UK120'):
        density=np.interp(row[0],mr[order,0],mr[order,3])
        kaon.append([f'{row[0]:.3f}',f'{density:.3f}',f'{row[1]:.1f}',f'{row[6]:.3f}',f'{row[4]+row[5]:.3f}'])
    baryonic=[]
    for tag,label in (('ndelta',r'N\Delta'),('nydelta',r'NY\Delta')):
        rows=array('chi',tag)
        if tag=='ndelta':rows=rows[:1]
        for row in rows:
            hyperon='--' if tag=='ndelta' else f'{sum(row[10:13]):.3f}'
            baryonic.append([label,f'{row[0]:.3f}',f'{row[1]:.1f}',f'{sum(row[6:10]):.3f}',hyperon,f'{sum(row[4:6]):.3f}'])
    return kaon,baryonic

def tidal_table():
    points=record('published_tidal_points.json')['points']
    lookup={(r['tag'],round(r['M'],1)):r for r in points}
    # Printed mantissa precision is retained from the accepted table.
    formats={'npemu':(2,1,1),'ny':(2,1,2),'ka_UK160':(2,2,2),'ndelta':(2,2,2),'nydelta':(2,3,None)}
    rows=[]
    for tag in ('npemu','ny','ka_UK160','ndelta','nydelta'):
        values=[COMPOSITIONS[tag]]
        for index,mass in enumerate((1.4,1.8,2.0)):
            r=lookup.get((tag,mass))
            if r is None:values.extend(['--','--']);continue
            phase=r['phase_rad'];exponent=int(np.floor(np.log10(phase)))
            text=f'{phase/10**exponent:.{formats[tag][index]}f}'+rf'\times10^{{{exponent}}}'
            if tag=='npemu' and mass==2.:text=r'\lesssim'+text
            values.extend([f'{r["frequency_Hz"]:.1f}',text])
        rows.append(values)
    return rows

def comparison_table():
    points=record('exact_points.json')['points'];meta=record('exact_points.json')['meta']
    reaction=record('reaction_summary.json')['families'];dd=record('ddme2_comparison.json')
    rows=[]
    for i,(label,tag,react,key) in enumerate(((r'K^-','ka_UK120','ka_UK120_Keq','term'),
            (r'N\Delta','ndelta','ndelta_strongD','1.9'),(r'NY\Delta','nydelta','nydelta_strongD','1.9'))):
        frozen=points[tag+':'+key]['f'];equilibrated=points[react+':'+key]['f']
        mass=meta[tag]['M_term'] if key=='term' else 1.9
        rows.append([label,'BigApple',f'{mass:.3f}',f'{frozen:.1f}',f'{equilibrated:.1f}',f'{equilibrated/frozen:.3f}',f'{reaction[react]["retained_pct"]:.1f}'])
        row=dd[i]
        rows.append([label,'DD-ME2',f'{row["M_cmp"]:.3f}',f'{row["frozen"]:.1f}',f'{row["reaction"]:.1f}',f'{row["ratio"]:.3f}',f'{row["local_retention"]:.0f}'])
    return rows

def generate(use_published_display=True):
    one,two=model_tables();three,five=summary_tables();four,six=channel_tables()
    allrows={1:one,2:two,3:three,4:four,5:five,6:six,7:tidal_table(),8:comparison_table()}
    if use_published_display:
        for entry in record('published_display.json'):
            row=allrows[entry['table']][entry['row']]
            assert row[entry['column']]==entry['checkpoint_display']
            row[entry['column']]=entry['published_display']
    return allrows

def tex_cell(s):
    if not s or s in ('BigApple','DD-ME2','MeV','--'):return s
    if s.endswith('~MeV'):return '$'+s[:-4]+'$~MeV'
    if s==r'fm^{-3}':return r'fm$^{-3}$'
    return '$'+s+'$'

def write(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    allrows=generate()
    for number,rows in allrows.items():
        stem=f'table{number}_{TABLE_NAMES[number]}'
        result={'table_number':number,'semantic_label':LABELS[number],'columns':COLUMNS[number],'display_rows':rows}
        (out/(stem+'.json')).write_text(json.dumps(result,indent=2)+'\n')
        (out/(stem+'.tex')).write_text('\n'.join(' & '.join(map(tex_cell,row))+r' \\' for row in rows)+'\n')
    return allrows
