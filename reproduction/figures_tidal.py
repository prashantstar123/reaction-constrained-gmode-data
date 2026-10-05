"""Published tidal display from saved overlaps and the documented curve-frequency lookup."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import ScalarFormatter
from .processing import PAPER
from .data import record
from .graphics import save_figure
VALID=[]
OUT=None
def save(fig,name):
    save_figure(fig,OUT,"FIG8_tidal_dphi",dpi=200)
    plt.close(fig)
def fig8():
    VALID.append("FIG8 tidal (resolved data unchanged):")
    records=record("published_tidal_points.json")["points"]
    rows=[(r["tag"],r["M"],r["phase_rad"]) for r in records]

    # Published point frequencies are retained at their archived precision.
    def freq_for(tag, M, method):
        return next(r["frequency_Hz"] for r in records if r["tag"]==tag and r["M"]==M)

    TAGS = [("npemu", r"$npe\mu$", "k"), ("ndelta", r"$npe\mu+\Delta$", "#4C72B0"),
            ("ny", r"$npe\mu+Y$", "#C44E52"), ("nydelta", r"$npe\mu+Y+\Delta$", "#55A868"),
            ("ka_UK160", r"$npe\mu+K^-$", "#DA8BC3")]
    methods={}

    fig, ax = plt.subplots(figsize=(10.4, 7.2))
    pts_log = []
    for tag, lab, col in TAGS:
        for (rtag, M, D) in rows:
            if rtag != tag:
                continue
            meth = methods.get((rtag, round(M, 1)), "")
            f = freq_for(tag, M, meth)
            b = min([1.4, 1.8, 2.0], key=lambda x: abs(x - M))
            if abs(b - 1.4) < 0.11:
                ax.plot(f, D, "o", ms=16, color=col, mec="k", mew=1.2, zorder=5)
            elif abs(b - 1.8) < 0.11:
                ax.plot(f, D, "o", ms=16, mfc="white", mec=col, mew=3.2, zorder=5)
            else:
                ax.plot(f, D, "s", ms=14, mfc="white", mec=col, mew=3.2, zorder=5)
            pts_log.append(f"    {tag:10s} M={M:.3f} f={f:6.1f}Hz |dPhi|={D:.3e}")
    VALID.extend(sorted(set(pts_log)))
    handles = [Line2D([], [], marker="o", ls="", ms=13, color=c, mec="k", mew=0.8, label=l)
               for _, l, c in TAGS]
    ax.legend(handles=handles, fontsize=15, loc="upper center",
              bbox_to_anchor=(0.44, 0.86), framealpha=1.0, edgecolor="0.3", fancybox=True)
    ax.axhline(0.03, color="0.2", lw=2.0, ls="--", zorder=2)
    ax.text(900, 0.036, "ET favorable-event scale", fontsize=17, color="0.2", ha="right")
    ax.text(104, 0.055, "$\\bullet$ 1.4 $M_\\odot$      $\\circ$ 1.8 $M_\\odot$      □ 2.0 $M_\\odot$",
            fontsize=19, color="k")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(100, 950); ax.set_ylim(5e-6, 0.1)
    ax.set_xticks([100, 150, 200, 300, 400, 600, 900])
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.set_xlabel(r"$g_1$ resonance frequency $f$ [Hz]", fontsize=23)
    ax.set_ylabel(r"$|\Delta\Phi_{g_1}|$ [rad]", fontsize=23)
    ax.grid(ls=":", color="0.88", lw=0.9, which="both", zorder=0)
    fig.tight_layout()
    save(fig, "FIG8")
def render(out):
    global OUT
    OUT=out
    plt.rcParams.update(PAPER)
    fig8()
