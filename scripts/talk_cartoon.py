import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon

plt.rcParams.update({"font.size": 18, "font.family": "sans-serif"})

fig, axes = plt.subplots(1, 2, figsize=(13, 6))

gal_face = "lightgray"
gal_edge = "dimgray"


def draw_jets(ax, length, color, lobe_size):
    # tapered cone from the core out to each side, plus a lobe blob at the end
    for sign in [1, -1]:
        cone = Polygon(
            [[0, 0],
             [sign * length, 0.32],
             [sign * length, -0.32]],
            closed=True, facecolor=color, edgecolor="none", alpha=0.85, zorder=3)
        ax.add_patch(cone)
        lobe = Ellipse((sign * length, 0), width=lobe_size, height=lobe_size * 1.5,
                       facecolor=color, edgecolor="none", alpha=0.85, zorder=3)
        ax.add_patch(lobe)


for ax, label, sub, length, color, lobe in [
    (axes[0], "CONFINED", "10–15 kpc jets", 1.0, "plum", 0.45),
    (axes[1], "ESCAPED", ">25 kpc jets", 2.4, "purple", 0.6),
]:
    gal = Ellipse((0, 0), width=3, height=1.7, facecolor=gal_face,
                  edgecolor=gal_edge, lw=2, zorder=2)
    ax.add_patch(gal)
    draw_jets(ax, length, color, lobe)
    # bright core
    ax.plot(0, 0, marker="o", ms=9, color="black", zorder=4)
    ax.text(0, -1.6, label, ha="center", fontsize=26, fontweight="bold")
    ax.text(0, -2.0, sub, ha="center", fontsize=14, color="dimgray")
    ax.set_xlim(-3.1, 3.1)
    ax.set_ylim(-2.4, 1.8)
    ax.set_aspect("equal")
    ax.axis("off")

plt.tight_layout()
plt.savefig("plots/talk_cartoon_confined_vs_escaped.png", dpi=200, facecolor="white")