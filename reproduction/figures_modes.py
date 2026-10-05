"""Published frequency and damping panels, reconstructed from saved data."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from . import processing as mf
from .graphics import save_figure
def render_kaon(out):
    matplotlib.use('Agg')
    plt.rcParams.update(mf.PAPER)
    plt.rcParams.update({'axes.linewidth': 1.7, 'xtick.major.width': 1.4, 'ytick.major.width': 1.4, 'xtick.labelsize': 17, 'ytick.labelsize': 17})
    UKS = [(0, '#1f77b4', '$U_K = 0$ (no condensate)'), (100, '#2ca02c', '$U_K = -100$ MeV'), (120, '#ff7f0e', '$U_K = -120$ MeV'), (140, '#d62728', '$U_K = -140$ MeV'), (160, '#9467bd', '$U_K = -160$ MeV')]
    DASH = (5, 2.3)
    XLAB = '$M\\,[M_\\odot]$'
    colorh = [Line2D([], [], color=c, lw=3.0, label=l) for _, c, l in UKS]
    styleh = [Line2D([], [], color='0.25', lw=2.7, ls='-', label='full GR, frozen'), Line2D([], [], color='0.25', lw=2.3, ls='--', dashes=DASH, label='full GR, fast-$K$')]
    figA, ax = plt.subplots(figsize=(7.8, 6.3))
    for UK, col, lab in UKS:
        if UK == 0:
            M, F = mf.g1_stable('ka_UK0')
        else:
            M, F, _ = mf.spliced_freq(f'ka_UK{UK}', 'ka_UK0')
        m = M > 0.25
        ax.plot(M[m], F[m], '-', color=col, lw=2.7, solid_capstyle='round')
        if UK:
            Mk, Fk, _ = mf.spliced_freq(f'ka_UK{UK}_Keq', 'ka_UK0')
            mk = Mk > 0.25
            ax.plot(Mk[mk], Fk[mk], '--', color=col, lw=2.3, dashes=DASH)
    ax.set_xlabel(XLAB, fontsize=23)
    ax.set_ylabel('$f_{g_1}$ [Hz]', fontsize=23)
    ax.set_xlim(0.2, 2.7)
    ax.set_ylim(90, 900)
    ax.xaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax.yaxis.set_major_locator(plt.MultipleLocator(100))
    ax.grid(ls=':', color='0.85', lw=0.8, zorder=0)
    ax.legend(handles=colorh + styleh, fontsize=12.5, loc='upper left', framealpha=1.0, edgecolor='0.3', fancybox=True, handlelength=2.1)
    figA.tight_layout()
    save_figure(figA, out, 'FIG3a_kaon_freq', dpi=175)
    plt.close(figA)
    figB, ax = plt.subplots(figsize=(7.8, 6.3))
    lo, hi = (np.inf, -np.inf)
    
    def tau_curve(tag, base='ka_UK0'):
        if tag == base:
            b = mf.tau_pts(base)
            M, T, cv = (b[:, 0], b[:, 1], b[:, 4])
        else:
            on = mf.tau_onset(tag, base)
            M, T, cv = mf.spliced_tau(tag, base, on)
            pre = T[M < on]
            if len(pre):
                T = np.where(M >= on, np.minimum(T, 1.3 * pre[-1]), T)
        M, T, cv = mf.despike_tau(M, T, cv)
        return mf.smooth_logtau(M, T, cv)
    for UK, col, lab in UKS:
        M, T, cv = tau_curve('ka_UK0' if UK == 0 else f'ka_UK{UK}')
        ax.semilogy(M, T, '-', color=col, lw=2.7)
        lo, hi = (min(lo, T.min()), max(hi, T.max()))
        if UK:
            Mk, Tk, cvk = tau_curve(f'ka_UK{UK}_Keq')
            ax.semilogy(Mk, Tk, '--', color=col, lw=2.3, dashes=DASH)
            lo, hi = (min(lo, Tk.min()), max(hi, Tk.max()))
    ax.set_xlabel(XLAB, fontsize=23)
    ax.set_ylabel('$\\tau_{g_1}^{\\rm GW}$ [yr]', fontsize=23)
    ax.set_xlim(1.0, 2.65)
    ax.set_ylim(10.0 ** np.floor(np.log10(lo)), 10.0 ** np.ceil(np.log10(hi)))
    ax.grid(ls=':', which='both', color='0.85', lw=0.8, zorder=0)
    leg_c = ax.legend(handles=colorh, fontsize=12, loc='lower left', framealpha=1.0, edgecolor='0.3', fancybox=True)
    ax.add_artist(leg_c)
    ax.legend(handles=styleh, fontsize=11.5, loc='upper left', framealpha=1.0, edgecolor='0.3', fancybox=True, handlelength=2.1)
    figB.tight_layout()
    save_figure(figB, out, 'FIG3b_kaon_damping', dpi=175)
    plt.close(figB)
    plt.close("all")

def render_baryonic(out):
    matplotlib.use('Agg')
    plt.rcParams.update(mf.PAPER)
    plt.rcParams.update({'xtick.labelsize': 22, 'ytick.labelsize': 22})
    SETS = [('npemu', 'k', '$npe\\mu$'), ('ndelta', '#4C72B0', '$npe\\mu+\\Delta$'), ('ny', '#C44E52', '$npe\\mu+Y$'), ('nydelta', '#55A868', '$npe\\mu+Y+\\Delta$')]
    fig, ax = plt.subplots(figsize=(9.6, 7.4))
    handles = []
    for tag, col, lab in SETS:
        if tag == 'npemu':
            Mf, Ff = mf.g1_stable(tag)
        else:
            Mf, Ff, _ = mf.spliced_freq(tag, 'npemu')
        m = Mf > 0.25
        ax.plot(Mf[m], Ff[m], '-', color=col, lw=2.8, solid_capstyle='round')
        cw = mf.g1_cowl(tag) if tag == 'npemu' else mf.spliced_cowl(tag, 'npemu')
        if cw is not None:
            Mc, Fc = cw
            mc = Mc > 0.25
            ax.plot(Mc[mc], Fc[mc], '--', color=col, lw=2.4)
        handles.append(Line2D([], [], color=col, lw=3.2, label=lab))
    handles += [Line2D([], [], color='k', lw=2.6, ls='-', label='Full GR'), Line2D([], [], color='k', lw=2.2, ls='--', label='Relativistic Cowling')]
    ax.set_xlabel('$M\\,[M_\\odot]$', fontsize=26)
    ax.set_ylabel('$f_{g_1}$ [Hz]', fontsize=26)
    ax.set_xlim(0.2, 2.7)
    ax.set_ylim(90, 900)
    ax.xaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax.yaxis.set_major_locator(plt.MultipleLocator(100))
    ax.grid(ls=':', color='0.85', lw=0.8, zorder=0)
    ax.legend(handles=handles, fontsize=14, loc='upper left', framealpha=1.0, edgecolor='0.3', fancybox=True)
    fig.tight_layout()
    save_figure(fig, out, 'g1_paperstyle_can', dpi=170)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(9.6, 7.4))
    lo, hi = (np.inf, -np.inf)
    for tag, col, lab in SETS:
        if tag == 'npemu':
            a = mf.tau_pts(tag)
            M, T, cv = (a[:, 0], a[:, 1], a[:, 4])
        else:
            on = mf.tau_onset(tag, 'npemu')
            M, T, cv = mf.spliced_tau(tag, 'npemu', on)
            pre = T[M < on]
            if len(pre):
                T = np.where(M >= on, np.minimum(T, 1.3 * pre[-1]), T)
        M, T, cv = mf.despike_tau(M, T, cv)
        M, T, cv = mf.smooth_logtau(M, T, cv)
        ax.semilogy(M, T, '-', color=col, lw=2.8, solid_capstyle='round', label=lab)
        lo, hi = (min(lo, T.min()), max(hi, T.max()))
    ax.set_ylim(10.0 ** np.floor(np.log10(lo)), 10.0 ** np.ceil(np.log10(hi)))
    ax.set_xlabel('$M\\,[M_\\odot]$', fontsize=26)
    ax.set_ylabel('$\\tau_{g_1}^{\\rm GW}$ [yr]', fontsize=26)
    ax.set_xlim(0.5, 2.7)
    ax.xaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax.grid(ls=':', color='0.85', lw=0.8, which='both', zorder=0)
    ax.legend(fontsize=16, loc='lower left', framealpha=1.0, edgecolor='0.3', fancybox=True)
    fig.tight_layout()
    save_figure(fig, out, 'tau_paperstyle_can', dpi=170)
    plt.close(fig)
    plt.close("all")

def render_reaction(out):
    matplotlib.use('Agg')
    plt.rcParams.update(mf.PAPER)
    plt.rcParams.update({'xtick.labelsize': 20, 'ytick.labelsize': 20})
    fig, ax = plt.subplots(figsize=(9.8, 7.2))
    Mn, Fn = mf.g1_stable('npemu')
    m = Mn > 0.95
    ax.plot(Mn[m], Fn[m], '-', color='0.55', lw=3.0, solid_capstyle='round')
    for tag, col in [('ndelta', '#4C72B0'), ('nydelta', '#55A868')]:
        MF, FF, _ = mf.spliced_freq(tag, 'npemu')
        MS, FS, _ = mf.spliced_freq(f'{tag}_strongD', 'npemu')
        mF, mS = (MF > 0.95, MS > 0.95)
        ax.plot(MF[mF], FF[mF], '-', color=col, lw=3.2, solid_capstyle='round')
        ax.plot(MS[mS], FS[mS], '--', color=col, lw=3.2)
    handles = [Line2D([], [], color='#4C72B0', lw=3.2, label='$npe\\mu+\\Delta$'), Line2D([], [], color='#55A868', lw=3.2, label='$npe\\mu+Y+\\Delta$'), Line2D([], [], color='0.55', lw=3.0, label='$npe\\mu$'), Line2D([], [], color='k', lw=2.6, ls='-', label='frozen composition'), Line2D([], [], color='k', lw=2.6, ls='--', label='strong-equilibrium $\\hspace{0.15235}\\Delta$')]
    ax.legend(handles=handles, fontsize=16, loc='upper left', framealpha=1.0, edgecolor='0.3', fancybox=True)
    ax.set_xlabel('$M\\,[M_\\odot]$', fontsize=23)
    ax.set_ylabel('$f_{g_1}$ [Hz]', fontsize=23)
    ax.set_xlim(0.95, 2.4)
    ax.set_ylim(120, 800)
    ax.xaxis.set_major_locator(plt.MultipleLocator(0.25))
    ax.yaxis.set_major_locator(plt.MultipleLocator(100))
    ax.grid(ls=':', color='0.88', lw=0.9, zorder=0)
    fig.tight_layout()
    save_figure(fig, out, 'FIG7_strongD', dpi=170)
    plt.close("all")
