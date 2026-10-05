"""Archived display selections and interpolation; not a stellar solver."""
import numpy as np
from scipy.signal import savgol_filter
from .data import array,attributes
from .figures_basic import PAPER
N_CUT={}

def g1_stable(tag):
    g=array("g1",tag)
    g=g[np.argsort(g[:,0])]
    g=g[:int(np.argmax(g[:,1]))+1]
    order=np.argsort(g[:,1]);mass,frequency=g[order,1],g[order,4]
    keep=np.concatenate([[True],np.diff(mass)>1e-4])
    return mass[keep],frequency[keep]

def g1_cowl(tag):
    if attributes("g1",tag)["cowling_same_record"]:
        g=array("g1",tag);a=g[np.isfinite(g[:,3]),:][:,[1,3]]
    else:a=array("cowling",tag)
    if a.ndim==1:a=a[None,:]
    a=a[np.argsort(a[:,0])]
    keep=np.concatenate([[True],np.diff(a[:,0])>1e-4])
    mass,frequency=a[keep,0],a[keep,1]
    mg,fg=g1_stable(tag);reference=np.interp(mass,mg,fg)
    keep=(frequency>.72*reference)&(frequency<1.03*reference)
    return mass[keep],frequency[keep]

def tau_pts(tag):
    a=array("tau",tag)
    if a.ndim==1:a=a[None,:]
    a=a[np.argsort(a[:,0])]
    keep=np.concatenate([np.diff(a[:,0])>1e-4,[True]])
    a=a[keep];reliable=np.abs(a[:,2])>=1e-16
    N_CUT[tag]=int((~reliable).sum())
    return a[reliable]

def onset_mass(tag, baseline, thr=12.0):
    """First mass (>1.0) where own fGR exceeds the baseline fGR by >thr Hz and
    stays above thr/2 afterwards -> the physical onset / splice point."""
    oM, oF = g1_stable(tag)
    bM, bF = g1_stable(baseline)
    bFi = np.interp(oM, bM, bF)
    diff = oF - bFi
    for i in range(len(oM)):
        if oM[i] > 1.0 and diff[i] > thr and np.all(diff[i:] > thr / 3):
            return oM[i]
    return oM.max() + 1.0

def spliced_freq(tag, baseline):
    oM, oF = g1_stable(tag)
    bM, bF = g1_stable(baseline)
    on = onset_mass(tag, baseline)
    M = np.concatenate([bM[bM < on], oM[oM >= on]])
    F = np.concatenate([bF[bM < on], oF[oM >= on]])
    o = np.argsort(M)
    return M[o], F[o], on

def spliced_cowl(tag, baseline):
    """Cowling analogue of spliced_freq: below the full-GR onset the exotic
    family IS the baseline star, so its Cowling curve is the baseline's there."""
    oc = g1_cowl(tag)
    bc = g1_cowl(baseline)
    if oc is None or bc is None:
        return None
    (oM, oF), (bM, bF) = oc, bc
    on = onset_mass(tag, baseline)
    M = np.concatenate([bM[bM < on], oM[oM >= on]])
    F = np.concatenate([bF[bM < on], oF[oM >= on]])
    o = np.argsort(M)
    return M[o], F[o]

def tau_onset(tag, baseline):
    """Mass where the family's own damping first diverges from the baseline by
    >20% (the physical onset).  Below it own==baseline (identical star), so the
    splice is seamless AND the full onset feature stays inside the own data."""
    ow = tau_pts(tag)
    ba = tau_pts(baseline)
    bi = np.interp(ow[:, 0], ba[:, 0], ba[:, 1])
    for i in range(len(ow)):
        if ow[i, 0] > 1.0 and abs(np.log(ow[i, 1] / bi[i])) > 0.20:
            return ow[i, 0]
    return ow[:, 0].max() + 1.0

def spliced_tau(tag, baseline, on):
    """Below onset use baseline damping points; above use own."""
    own = tau_pts(tag)
    base = tau_pts(baseline)
    M = np.concatenate([base[base[:, 0] < on, 0], own[own[:, 0] >= on, 0]])
    T = np.concatenate([base[base[:, 0] < on, 1], own[own[:, 0] >= on, 1]])
    conv = np.concatenate([base[base[:, 0] < on, 4], own[own[:, 0] >= on, 4]])
    o = np.argsort(M)
    return M[o], T[o], conv[o]

def despike_tau(M, T, cv, up=0.30):
    """Drop onset GW-decoupling UP-spikes -- tau points sitting >10^up (~2x)
    above the log-interpolation of their neighbours.  These are the near-
    decoupling tips that read as a jagged spike; removing them leaves the smooth
    weak->strong damping transition.  Repeated to peel multi-point spikes."""
    for _ in range(4):
        if len(M) < 3:
            break
        lt = np.log10(T)
        keep = np.ones(len(M), bool)
        for i in range(1, len(M) - 1):
            it = np.interp(M[i], [M[i - 1], M[i + 1]], [lt[i - 1], lt[i + 1]])
            if lt[i] - it > up:
                keep[i] = False
        if keep.all():
            break
        M, T, cv = M[keep], T[keep], cv[keep]
    return M, T, cv

def smooth_logtau(M, T, cv, win=7, order=2):
    """Light shape-preserving smooth of log(tau): removes the damping_quad
    mode-ID point-to-point jitter.  Small window so the steep onset drop and the
    high-mass rise are preserved (only the sub-feature scatter is removed)."""
    n = len(T)
    if n >= 5:
        w = min(win, n if n % 2 else n - 1)
        if w >= 5:
            T = 10.0 ** savgol_filter(np.log10(T), w, order)
    return M, T, cv
