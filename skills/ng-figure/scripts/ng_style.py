"""Reusable Nature Genetics style/export helpers; Python 3 + Matplotlib."""
from pathlib import Path
import warnings
import matplotlib as mpl
from matplotlib import font_manager

COLORS = {"blue": "#386C8C", "teal": "#378578", "rust": "#B3634A",
          "purple": "#806591", "gray": "#777777", "ink": "#222222"}


def configure(font=None):
    """Configure before constructing a figure; disclose actual font."""
    candidates = [font] if font else ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"]
    chosen = None
    for candidate in candidates:
        try:
            font_manager.findfont(font_manager.FontProperties(family=candidate), fallback_to_default=False)
            chosen = candidate
            break
        except ValueError:
            continue
    if chosen is None:
        raise ValueError(f"Requested font unavailable: {candidates}")
    if chosen not in ("Arial", "Helvetica"):
        warnings.warn(f"Using fallback {chosen}; verify production suitability.")
    mpl.rcParams.update({
        "font.family": chosen, "font.size": 7, "axes.labelsize": 7,
        "axes.titlesize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
        "legend.fontsize": 7, "legend.title_fontsize": 7,
        "figure.titlesize": 7, "figure.labelsize": 7,
        "pdf.fonttype": 42, "ps.fonttype": 42, "pdf.use14corefonts": False,
        "text.usetex": False, "svg.fonttype": "none",
        "text.color": COLORS["ink"], "axes.labelcolor": COLORS["ink"],
        "xtick.color": COLORS["ink"], "ytick.color": COLORS["ink"],
        "axes.edgecolor": COLORS["ink"], "axes.linewidth": 0.6,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "xtick.direction": "out", "ytick.direction": "out",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": False, "legend.frameon": False,
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "savefig.bbox": None,
    })
    print(f"[style] Font: {chosen}; labels: 7 pt; PDF fonttype: 42")
    return chosen


def save_pdf(fig, path, *, width_mm, height_mm, dpi=600):
    """Preserve exact page size; dpi only affects raster artists."""
    if not (0 < width_mm <= 180 and height_mm > 0):
        raise ValueError("Use positive dimensions and NG width <= 180 mm.")
    target = Path(path)
    if target.suffix.lower() != ".pdf":
        raise ValueError("Master export must have a .pdf suffix.")
    target.parent.mkdir(parents=True, exist_ok=True)
    fig.set_size_inches(width_mm / 25.4, height_mm / 25.4, forward=True)
    with mpl.rc_context({"savefig.bbox": None, "pdf.fonttype": 42, "pdf.use14corefonts": False}):
        fig.savefig(target, format="pdf", dpi=dpi, bbox_inches=None, facecolor="white", transparent=False)
    print(f"[export] {target}: {width_mm} x {height_mm} mm")
    return target
