#!/usr/bin/env python3
"""Build the static SVG charts used in README.md / docs/assets/CHARTS.md.

Reproduce:
    python3 scripts/make_charts.py

Writes light+dark SVG pairs into docs/assets/. No network, no new deps
(matplotlib 3.10 only). Numbers are hardcoded below (small, hand-checked
dataset) with the file each one was checked against.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "none"  # real SVG text, not paths
matplotlib.rcParams["font.family"] = "sans-serif"

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

OUT = Path(__file__).resolve().parent.parent / "docs" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# DATA (hardcoded, small, hand-verified against source files below)
# ---------------------------------------------------------------------------

# Chart A: manifest-effect
# Source: ANALYSE.md:30 (61% Treue vor Reparatur, gleiches deepseek-v4.1-flash
# im Produktivlauf) plus Samuels manifest-effect Nachlauf (Dateiliste im
# Prompt statt freier Suche) am 2026-09-23 -- gleiches Modell, gleiche 16
# Repos, gleicher Pruefer (scripts/grounding.py).
MANIFEST_BEFORE_TREUE = 61
MANIFEST_AFTER_TREUE = 100
MANIFEST_BEFORE_INVENTED = 28
MANIFEST_AFTER_INVENTED = 0

# Chart B: blind-vs-metric
# Sources (cross-checked, all 8 points match exactly):
#   <contest-dir>/mappe/AUFLOESUNG.md  (Buchstabe -> Modell)
#   <contest-dir>/mappe/MESSUNG.md    (Treue-%, blind)
#   <contest-dir>/mappe/URTEIL.md     (Blindurteil-Stufe, vor Aufloesung)
# README B (nemotron-3.5-lightning) fehlt: nicht geliefert, faellt aus der Treue-Messung raus.
TIER_ORDER = ["schwach", "mittel", "gut", "Spitze"]
TIER_Y = {name: i for i, name in enumerate(TIER_ORDER)}

BLIND_VS_METRIC = [
    # (model, harness, treue_pct, tier, label_dx, label_dy)
    ("gpt-5.5", "Hermes", 100, "Spitze", 8, 6),
    ("MiniMax-M3", "Hermes", 94, "Spitze", -8, 14),
    ("deepseek-v4.1-flash", "Hermes", 94, "Spitze", -8, -16),
    ("mimo-v2.6-flash", "OpenCode", 94, "gut", 8, 8),
    ("ling-3.0-flash", "OpenCode", 67, "gut", 8, 6),
    ("muse-spark-1.2", "OpenCode", 100, "mittel", -8, 8),
    ("nemotron-3-ultra", "OpenCode", 88, "schwach", -10, 16),
    ("muse-spark-1.3", "OpenCode", 94, "schwach", 8, 16),
]

HARNESS_COLOR = {"Hermes": "series1", "OpenCode": "series2"}

# ---------------------------------------------------------------------------
# PALETTE (validated: node .../dataviz/scripts/validate_palette.js -- PASS
# for both light and dark, see docs/assets/CHARTS.md)
# ---------------------------------------------------------------------------

PALETTES = {
    "light": dict(
        surface="#fcfcfb",
        text_primary="#0b0b0b",
        text_secondary="#52514e",
        grid="#e8e7e3",
        series1="#2a78d6",
        series2="#eb6834",
    ),
    "dark": dict(
        surface="#1a1a19",
        text_primary="#ffffff",
        text_secondary="#c3c2b7",
        grid="#383835",
        series1="#3987e5",
        series2="#d95926",
    ),
}

FIG_W_IN = 9.4  # ~800px wide once bbox_inches='tight' crops the SVG


def style_axes(ax, pal):
    ax.set_facecolor(pal["surface"])
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(pal["grid"])
        ax.spines[spine].set_linewidth(1.0)
    ax.tick_params(colors=pal["text_secondary"], labelsize=9, length=3)
    ax.xaxis.label.set_color(pal["text_secondary"])
    ax.yaxis.label.set_color(pal["text_secondary"])


def save(fig, name, mode):
    path = OUT / f"{name}-{mode}.svg"
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {path}")


# ---------------------------------------------------------------------------
# Chart A: manifest-effect (hero stat tiles)
# ---------------------------------------------------------------------------

def make_manifest_effect(mode):
    pal = PALETTES[mode]
    fig, axes = plt.subplots(1, 2, figsize=(FIG_W_IN, 3.1), facecolor=pal["surface"])
    fig.subplots_adjust(left=0.03, right=0.97, top=0.99, bottom=0.01, wspace=0.05)

    tiles = [
        ("Pfad-Treue", f"{MANIFEST_BEFORE_TREUE} %", f"{MANIFEST_AFTER_TREUE} %", pal["series1"]),
        ("neu erfundene Pfade", str(MANIFEST_BEFORE_INVENTED), str(MANIFEST_AFTER_INVENTED), pal["series2"]),
    ]

    for ax, (label, before, after, color) in zip(axes, tiles):
        ax.set_facecolor(pal["surface"])
        ax.axis("off")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.text(0.5, 0.86, label, ha="center", va="center", fontsize=15,
                 color=pal["text_secondary"])
        ax.text(0.20, 0.5, before, ha="center", va="center", fontsize=30,
                 color=pal["text_secondary"], fontweight="bold")
        ax.annotate("", xy=(0.60, 0.5), xytext=(0.35, 0.5),
                     arrowprops=dict(arrowstyle="-|>", color=pal["text_secondary"], lw=1.8))
        ax.text(0.82, 0.5, after, ha="center", va="center", fontsize=40,
                 color=color, fontweight="bold")

    fig.suptitle("Datei-Manifest im Prompt hebt die Pfad-Treue",
                  color=pal["text_primary"], fontsize=16, y=1.16, fontweight="bold")
    fig.text(0.5, 1.055,
              "Gleiches Modell (deepseek-v4.1-flash), gleiche 16 Repos, gleicher Prüfer — "
              "einzige Änderung: Dateiliste im Prompt",
              ha="center", va="top", fontsize=10, color=pal["text_secondary"])
    fig.text(0.5, -0.07,
              "Vorher-Wert: Reparatur ohne Dateiliste (61 %, 28 neu erfunden). Messung: Anteil der in\n"
              "Backticks genannten Pfade, die im Repo existieren.",
              ha="center", va="top", fontsize=8.5, color=pal["text_secondary"])

    save(fig, "manifest-effect", mode)


# ---------------------------------------------------------------------------
# Chart B: blind-vs-metric (scatter)
# ---------------------------------------------------------------------------

def make_blind_vs_metric(mode):
    pal = PALETTES[mode]
    fig, ax = plt.subplots(figsize=(FIG_W_IN, 5.2), facecolor=pal["surface"])
    style_axes(ax, pal)

    for model, harness, treue, tier, dx, dy in BLIND_VS_METRIC:
        color = pal[HARNESS_COLOR[harness]]
        y = TIER_Y[tier]
        ax.scatter(treue, y, s=90, color=color, zorder=3,
                   edgecolors=pal["surface"], linewidths=2)
        ax.annotate(model, xy=(treue, y), xytext=(dx, dy),
                    textcoords="offset points", fontsize=8.3,
                    color=pal["text_primary"], ha="left" if dx >= 0 else "right",
                    va="bottom" if dy > 0 else ("top" if dy < 0 else "center"))

    ax.set_xlim(60, 101)
    ax.set_xlabel("Pfad-Treue (%, gemessen)")
    ax.set_xticks([60, 70, 80, 90, 100])
    ax.set_yticks(range(len(TIER_ORDER)))
    ax.set_yticklabels(TIER_ORDER)
    ax.set_ylim(-0.6, len(TIER_ORDER) - 0.4)
    ax.set_ylabel("Blindurteil (Stufe)")
    ax.grid(axis="x", color=pal["grid"], linewidth=0.8, zorder=0)
    ax.grid(axis="y", visible=False)
    ax.set_title("Menschliches Urteil und Messung sehen verschiedene Dinge",
                  color=pal["text_primary"], fontsize=13.5, pad=14, fontweight="bold")

    legend_handles = [
        Line2D([0], [0], marker="o", linestyle="", markersize=8,
               markerfacecolor=pal["series1"], markeredgecolor=pal["surface"],
               markeredgewidth=1.5, label="Hermes"),
        Line2D([0], [0], marker="o", linestyle="", markersize=8,
               markerfacecolor=pal["series2"], markeredgecolor=pal["surface"],
               markeredgewidth=1.5, label="OpenCode"),
    ]
    leg = ax.legend(handles=legend_handles, loc="lower left", frameon=False,
                     fontsize=9, labelcolor=pal["text_primary"])

    fig.text(0.02, -0.02,
              "n = 1 Repo, 8 Modelle. Hermes- und OpenCode-Modelle liefen in verschiedenen\n"
              "Harnesses — deshalb der zweite Benchmark in einer Harness.",
              ha="left", va="top", fontsize=7.8, color=pal["text_secondary"])

    save(fig, "blind-vs-metric", mode)


def main():
    for mode in ("light", "dark"):
        make_manifest_effect(mode)
        make_blind_vs_metric(mode)


if __name__ == "__main__":
    main()
