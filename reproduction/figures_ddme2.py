"""DD-ME2 appendix figure from the saved EOS and mode sequences."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from .data import array
from .graphics import save_figure
def eos(tag):
    a=array("eos",tag,"ddme2.h5")
    return a[:,0],a[:,3]-a[:,4]
def g1(tag):
    a=array("g1",tag,"ddme2.h5");k=int(np.argmax(a[:,1]))
    return a[:k+1,1],a[:k+1,4]
def render(out):
    matplotlib.use('Agg')
    plt.rcParams.update({'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix', 'axes.linewidth': 1.2, 'xtick.direction': 'in', 'ytick.direction': 'in', 'xtick.top': True, 'ytick.right': True, 'xtick.labelsize': 12, 'ytick.labelsize': 12, 'xtick.minor.visible': True, 'ytick.minor.visible': True})
    DASH = (5, 2.3)
    CK = '#2ca02c'
    CN = '#1f77b4'
    CY = '#d62728'
    CYD = '#9467bd'
    CNP = '0.25'
    NEU = '0.35'
    fig, ax = plt.subplots(2, 2, figsize=(13.2, 10.0))
    nB, dcf = eos('kaon')
    _, dck = eos('kaon_fastK')
    m = nB > 0.35
    ax[0, 0].plot(nB[m], dcf[m], '-', color=CK, lw=2.3)
    ax[0, 0].plot(nB[m], dck[m], '--', color=CK, lw=2.0, dashes=DASH)
    ax[0, 0].set_xlabel('$n_B$ (fm$^{-3}$)', fontsize=14)
    ax[0, 0].set_ylabel('$c_s^2 - c_e^2$', fontsize=14)
    ax[0, 0].set_title('(a) $K^-$ local buoyancy ($U_K=-120$ MeV)', fontsize=13)
    ax[0, 0].legend(handles=[Line2D([], [], color=CK, lw=2.3, ls='-', label='frozen'), Line2D([], [], color=CK, lw=2.0, ls='--', dashes=DASH, label='fast-$K$')], fontsize=11, frameon=True)
    ax[0, 0].grid(ls=':', color='0.85')
    ax[0, 0].set_xlim(0.3, 1.15)
    Mn, fn = g1('npemu')
    Mf, ff = g1('kaon')
    Mk, fk = g1('kaon_fastK')
    ax[0, 1].plot(Mn, fn, '-', color=CNP, lw=2.0)
    ax[0, 1].plot(Mf, ff, '-', color=CK, lw=2.3)
    ax[0, 1].plot(Mk, fk, '--', color=CK, lw=2.0, dashes=DASH)
    ax[0, 1].set_xlabel('$M\\,(M_\\odot)$', fontsize=14)
    ax[0, 1].set_ylabel('$f_{g_1}\\,(\\mathrm{Hz})$', fontsize=14)
    ax[0, 1].set_title('(b) $K^-$ $g_1$-mode frequency', fontsize=13)
    ax[0, 1].legend(handles=[Line2D([], [], color=CNP, lw=2.0, label='npe$\\mu$'), Line2D([], [], color=CK, lw=2.3, label='$K^-$'), Line2D([], [], color=CK, lw=2.0, ls='--', dashes=DASH, label='fast-$K$')], fontsize=11, frameon=True, loc='upper left')
    ax[0, 1].grid(ls=':', color='0.85')
    ax[0, 1].set_xlim(1.0, 2.55)
    nBd, dcdf = eos('ndelta')
    _, dcds = eos('ndelta_strongD')
    nBy, dcyd = eos('nydelta')
    _, dcyds = eos('nydelta_strongD')
    nBny, dcny = eos('ny')
    md = nBd > 0.3
    myd = nBy > 0.3
    mny = nBny > 0.3
    ax[1, 0].plot(nBd[md], dcdf[md], '-', color=CN, lw=2.2)
    ax[1, 0].plot(nBd[md], dcds[md], '--', color=CN, lw=1.9, dashes=DASH)
    ax[1, 0].plot(nBy[myd], dcyd[myd], '-', color=CYD, lw=2.2)
    ax[1, 0].plot(nBy[myd], dcyds[myd], '--', color=CYD, lw=1.9, dashes=DASH)
    ax[1, 0].plot(nBny[mny], dcny[mny], ':', color=CY, lw=2.0)
    ax[1, 0].set_xlabel('$n_B$ (fm$^{-3}$)', fontsize=14)
    ax[1, 0].set_ylabel('$c_s^2 - c_e^2$', fontsize=14)
    ax[1, 0].set_title('(c) $\\Delta$ and hyperon local buoyancy', fontsize=13)
    ax[1, 0].legend(handles=[Line2D([], [], color=CN, lw=2.2, label='$N\\Delta$'), Line2D([], [], color=CYD, lw=2.2, label='$NY\\Delta$'), Line2D([], [], color=CY, lw=2.0, ls=':', label='$NY$'), Line2D([], [], color=NEU, lw=1.9, ls='--', dashes=DASH, label='strong-$\\Delta$')], fontsize=10.5, frameon=True)
    ax[1, 0].grid(ls=':', color='0.85')
    ax[1, 0].set_xlim(0.3, 1.1)
    ax[1, 1].plot(Mn, fn, '-', color=CNP, lw=2.0)
    Mny_, fny_ = g1('ny')
    ax[1, 1].plot(Mny_, fny_, ':', color=CY, lw=2.0)
    Mdf, fdf = g1('ndelta')
    Mds, fds = g1('ndelta_strongD')
    ax[1, 1].plot(Mdf, fdf, '-', color=CN, lw=2.2)
    ax[1, 1].plot(Mds, fds, '--', color=CN, lw=1.9, dashes=DASH)
    Mydf, fydf = g1('nydelta')
    Myds, fyds = g1('nydelta_strongD')
    ax[1, 1].plot(Mydf, fydf, '-', color=CYD, lw=2.2)
    ax[1, 1].plot(Myds, fyds, '--', color=CYD, lw=1.9, dashes=DASH)
    ax[1, 1].set_xlabel('$M\\,(M_\\odot)$', fontsize=14)
    ax[1, 1].set_ylabel('$f_{g_1}\\,(\\mathrm{Hz})$', fontsize=14)
    ax[1, 1].set_title('(d) $\\Delta$ and hyperon $g_1$-mode frequencies', fontsize=13)
    ax[1, 1].legend(handles=[Line2D([], [], color=CNP, lw=2.0, label='npe$\\mu$'), Line2D([], [], color=CY, lw=2.0, ls=':', label='$NY$'), Line2D([], [], color=CN, lw=2.2, label='$N\\Delta$'), Line2D([], [], color=CYD, lw=2.2, label='$NY\\Delta$'), Line2D([], [], color=NEU, lw=1.9, ls='--', dashes=DASH, label='strong-$\\Delta$')], fontsize=10, frameon=True, loc='upper left', ncol=2)
    ax[1, 1].grid(ls=':', color='0.85')
    ax[1, 1].set_xlim(1.0, 2.45)
    fig.tight_layout()
    save_figure(fig, out, 'ddme2_appendix_robustness', dpi=300)
    plt.close("all")
