"""Publication plotting recipes for buoyancy, composition, and mass-radius figures."""
import os
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator
from .data import array
from .graphics import save_figure
EOS="eos";TOV="mr";BUO="reaction";INT="composition"

def L(path):
    kind,name=path.split("/",1)
    for prefix in ("eos5_can_","MR_can_","fractions_can_"):
        if name.startswith(prefix):name=name[len(prefix):]
    return array(kind,name.removesuffix(".dat"))

def draw_obs(ax):
    def cx(n):return array("",n,"observational_display.h5")
    for name,color,alpha in (("Miller_68_3_J0030_0451","c",.35),("Riley_68_3_J0030_0451","goldenrod",.4),
            ("GW170817_90","steelblue",.30),("GW170817_50","steelblue",.45),("Riley_68_J0740_6620","#b45ec6",.40)):
        a=cx(name);ax.fill(a[:,0],a[:,1],color=color,alpha=alpha,lw=0,zorder=1)
    ax.errorbar(12.39,2.072,xerr=[[.98],[1.30]],yerr=[[.066],[.067]],color="purple",lw=2.2,capsize=4,zorder=2)
    ax.errorbar(13.02,1.44,xerr=[[1.06],[1.24]],yerr=[[.14],[.15]],color="magenta",lw=2.2,capsize=4,zorder=2)
    ax.errorbar(12.71,1.34,xerr=[[1.19],[1.14]],yerr=[[.16],[.15]],color="#C44E52",lw=2.2,capsize=4,zorder=2)

PAPER = {
    "font.family": "STIXGeneral", "mathtext.fontset": "stix",
    "axes.linewidth": 1.8,
    "xtick.direction": "in", "ytick.direction": "in",
    "xtick.top": True, "ytick.right": True,
    "xtick.major.size": 7, "ytick.major.size": 7,
    "xtick.minor.size": 3.5, "ytick.minor.size": 3.5,
    "xtick.major.width": 1.6, "ytick.major.width": 1.6,
    "xtick.minor.width": 1.1, "ytick.minor.width": 1.1,
    "xtick.labelsize": 20, "ytick.labelsize": 20,
    "xtick.minor.visible": True, "ytick.minor.visible": True,
}

UK_TAB10 = {0: "#1f77b4", 100: "#2ca02c", 120: "#ff7f0e",
            140: "#d62728", 160: "#9467bd"}

UK_MR = {0: "k", 100: "#4C72B0", 120: "#55A868", 140: "#DD8452", 160: "#C44E52"}

def mr_stable(path):
    """MR_can cols: M R eps_c nB_c.  Sort by eps_c, cut at max mass.
    Returns (stable_rows, k_index, is_turnover)."""
    d = L(path)
    d = d[np.argsort(d[:, 2])]
    k = int(np.argmax(d[:, 0]))
    return d[:k + 1], k, (k < len(d) - 1)

def mr_marker(ax, row, col, turnover):
    """Star at a genuine turnover (physical max mass); filled square at a
    validity-truncated sequence endpoint (terminal marker)."""
    if turnover:
        ax.plot(row[1], row[0], "*", color=col, ms=18, mec="k", mew=0.6, zorder=4)
    else:
        ax.plot(row[1], row[0], "s", color=col, ms=10, mec="k", mew=0.9, zorder=4)

def panel1_left(ax):
    UKS = [(0, r"$U_K = 0$ (no condensate)"), (100, r"$U_K = -100$ MeV"),
           (120, r"$U_K = -120$ MeV"), (140, r"$U_K = -140$ MeV"),
           (160, r"$U_K = -160$ MeV")]
    for uk, lab in UKS:
        e = L(os.path.join(EOS, f"eos5_can_ka_UK{uk}.dat"))
        nB, dc2 = e[:, 0], e[:, 3] - e[:, 4]
        m = nB > 0.0
        ax.plot(nB[m], dc2[m], "-", color=UK_TAB10[uk], lw=2.4, label=lab)
        if uk != 0:
            k = L(os.path.join(BUO, f"eos5_can_ka_UK{uk}_Keq.dat"))
            nBk, dck = k[:, 0], k[:, 3] - k[:, 4]
            mk = nBk > 0.04
            ax.plot(nBk[mk], dck[mk], "--", color=UK_TAB10[uk], lw=2.0,
                    dashes=(5, 2.5))
    ax.set_xlim(0.0, 1.05)
    ax.set_ylim(-0.008, 0.46)
    ax.set_xlabel(r"$n_B$ [fm$^{-3}$]", fontsize=23)
    ax.set_ylabel(r"$c_s^2 - c_e^2$", fontsize=23)
    ax.grid(ls=":", color="0.8", lw=0.8)
    leg1 = ax.legend(fontsize=12.5, loc="upper right", framealpha=0.95,
                     handlelength=1.8, borderpad=0.5)
    ax.add_artist(leg1)
    style = [Line2D([], [], color="0.25", lw=2.4, ls="-", label="frozen"),
             Line2D([], [], color="0.25", lw=2.0, ls="--", dashes=(5, 2.5),
                    label="fast-$K$ equilibrated")]
    ax.legend(handles=style, fontsize=12, loc="center right", framealpha=0.95,
              handlelength=2.2)

def panel1_right(ax):
    nB, Yn, Yp, Ye, Ymu, YK = L(os.path.join(
        INT, "fractions_can_ka_UK120.dat")).T
    SPEC = [(Yn, "n", "C0"), (Yp, "p", "C3"), (Ye, r"e$^-$", "C2"),
            (Ymu, r"$\mu^-$", "C1"), (YK, r"K$^-$", "k")]
    for y, lab, col in SPEC:
        y = y.copy()
        y[y <= 0] = np.nan
        ax.plot(nB, y, "-", color=col, lw=2.6, label=lab)
    ax.set_yscale("log")
    ax.set_ylim(1e-3, 1.2)
    ax.set_xlim(nB.min(), nB.max())
    ax.set_xlabel(r"$n_B$ [fm$^{-3}$]", fontsize=23)
    ax.set_ylabel("particle fraction", fontsize=23)
    ax.grid(alpha=0.25, which="both")
    ax.legend(fontsize=15, ncol=5, loc="lower right", columnspacing=1.0,
              framealpha=0.95, handlelength=1.4)

def fig1():
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(15.2, 6.0))
    panel1_left(axL)
    panel1_right(axR)
    fig.tight_layout(pad=1.4, w_pad=3.0)
    save(fig, "FIG1")

def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 7.4))
    draw_obs(ax)
    UKS = [(0, r"$U_K = 0$"), (100, r"$U_K = -100$ MeV"),
           (120, r"$U_K = -120$ MeV"), (140, r"$U_K = -140$ MeV"),
           (160, r"$U_K = -160$ MeV")]
    for uk, lab in UKS:
        d, k, turn = mr_stable(os.path.join(TOV, f"MR_can_ka_UK{uk}.dat"))
        ax.plot(d[:, 1], d[:, 0], "-", color=UK_MR[uk], lw=2.8,
                solid_capstyle="round", label=lab, zorder=3)
        mr_marker(ax, d[k], UK_MR[uk], turn)
    ax.set_xlabel(r"$R$ [km]", fontsize=26)
    ax.set_ylabel(r"$M\,[M_\odot]$", fontsize=26)
    ax.set_xlim(10, 16)
    ax.set_ylim(0.2, 2.75)
    ax.xaxis.set_major_locator(MultipleLocator(1.0))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.grid(ls=":", color="0.85", lw=0.8, zorder=0)
    ax.legend(fontsize=16, loc="lower left", framealpha=1.0, edgecolor="0.3",
              fancybox=True)
    fig.tight_layout()
    save(fig, "FIG2")

def panel4_buoyancy(ax):
    SETS = [("npemu", C_NPEMU, r"$npe\mu$"),
            ("ndelta", C_NDEL, r"$npe\mu+\Delta$"),
            ("ny", C_NY, r"$npe\mu+Y$"),
            ("nydelta", C_NYDEL, r"$npe\mu+Y+\Delta$")]
    for tag, col, lab in SETS:
        e = L(os.path.join(EOS, f"eos5_can_{tag}.dat"))
        nB, dc2 = e[:, 0], e[:, 3] - e[:, 4]
        m = nB > 0.04
        ax.plot(nB[m], dc2[m], "-", color=col, lw=4.0, solid_capstyle="round",
                label=lab, zorder=3)
    ax.set_xlim(0.0, 0.95)
    ax.set_ylim(-0.012, 0.43)
    ax.set_xlabel(r"$n_B$ [fm$^{-3}$]", fontsize=25)
    ax.set_ylabel(r"$c_s^2 - c_e^2$", fontsize=25)
    ax.xaxis.set_major_locator(MultipleLocator(0.1))
    ax.yaxis.set_major_locator(MultipleLocator(0.05))
    ax.grid(ls=":", color="0.75", lw=0.9, zorder=0)
    ax.legend(fontsize=16, loc="upper left", framealpha=1.0, edgecolor="0.3",
              fancybox=True)

def panel4_fractions(ax):
    d = L(os.path.join(INT, "fractions_can_nydelta.dat"))
    nB = d[:, 0]
    IDX = {"n": 1, "p": 2, "e": 3, "mu": 4, "L": 5, "Dm": 11, "D0": 12, "Dp": 13}
    SPECIES = [("n", "#4C72B0", "-", r"n"), ("p", "#C44E52", "-", r"p"),
               ("e", "#55A868", "-", r"e$^-$"), ("mu", "#DD8452", "-", r"$\mu^-$"),
               ("Dm", "k", "--", r"$\Delta^-$"), ("D0", "#8172B2", "--", r"$\Delta^0$"),
               ("Dp", "#64B5CD", "--", r"$\Delta^+$"), ("L", "#937860", "--", r"$\Lambda$")]
    for key, col, ls, lab in SPECIES:
        y = d[:, IDX[key]].copy()
        if y.max() <= 1e-3:
            continue
        y[y <= 1e-5] = np.nan
        ax.plot(nB, y, ls, color=col, lw=4.0, solid_capstyle="round",
                label=lab, zorder=3)
    ax.set_yscale("log")
    ax.set_ylim(1e-4, 1.4)
    ax.set_xlim(0.05, 0.58)
    ax.xaxis.set_major_locator(MultipleLocator(0.1))
    ax.set_xlabel(r"$n_B$ [fm$^{-3}$]", fontsize=25)
    ax.set_ylabel("particle fraction", fontsize=25)
    ax.grid(ls=":", color="0.85", lw=0.8, zorder=0)
    ax.legend(fontsize=15, loc="center left", bbox_to_anchor=(1.01, 0.5),
              framealpha=1.0, edgecolor="0.3", fancybox=True)

def fig4():
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(16.8, 6.6))
    panel4_buoyancy(axL)
    panel4_fractions(axR)
    fig.subplots_adjust(left=0.055, right=0.88, bottom=0.13, top=0.96, wspace=0.30)
    save(fig, "FIG4", tight=False)

def fig5():
    fig, ax = plt.subplots(figsize=(9.6, 7.4))
    draw_obs(ax)
    SETS = [("npemu", C_NPEMU, r"$npe\mu$"),
            ("ndelta", C_NDEL, r"$npe\mu+\Delta$"),
            ("ny", C_NY, r"$npe\mu+Y$"),
            ("nydelta", C_NYDEL, r"$npe\mu+Y+\Delta$")]
    for tag, col, lab in SETS:
        d, k, turn = mr_stable(os.path.join(TOV, f"MR_can_{tag}.dat"))
        ax.plot(d[:, 1], d[:, 0], "-", color=col, lw=2.8, solid_capstyle="round",
                label=lab, zorder=3)
        mr_marker(ax, d[k], col, turn)
    ax.set_xlabel(r"$R$ [km]", fontsize=26)
    ax.set_ylabel(r"$M\,[M_\odot]$", fontsize=26)
    ax.set_xlim(10, 16)
    ax.set_ylim(0.2, 2.75)
    ax.xaxis.set_major_locator(MultipleLocator(1.0))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.grid(ls=":", color="0.85", lw=0.8, zorder=0)
    ax.legend(fontsize=16, loc="lower left", framealpha=1.0, edgecolor="0.3",
              fancybox=True)
    fig.tight_layout()
    save(fig, "FIG5")
C_NPEMU,C_NDEL,C_NY,C_NYDEL="k","#4C72B0","#C44E52","#55A868"
NAMES={"FIG1":"FIG1_kaon_buoyancy_fractions","FIG2":"FIG2_kaon_MR",
       "FIG4":"FIG4_hypdelta_buoyancy_fractions","FIG5":"FIG5_hypdelta_MR"}
OUT=None
def save(fig,name,tight=True):
    save_figure(fig,OUT,NAMES[name],dpi=200)
    plt.close(fig)
def render(out):
    global OUT
    OUT=out
    plt.rcParams.update(PAPER)
    for function in (fig1,fig2,fig4,fig5):function()
