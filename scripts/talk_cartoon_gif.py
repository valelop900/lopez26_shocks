import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
from PIL import Image
import glob, os

plt.rcParams.update({"font.size": 18, "font.family": "sans-serif"})

os.makedirs("plots/gif_frames", exist_ok=True)
n_frames = 60
rng = np.random.default_rng(3)

for i in range(n_frames):
    t = i / (n_frames - 1)
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.patch.set_facecolor("white")

    for ax, label, sub, max_len, color, lobe in [
        (axes[0], "CONFINED", "10–15 kpc jets", 1.0, "plum", 0.45),
        (axes[1], "ESCAPED", ">25 kpc jets", 2.4, "purple", 0.6),
    ]:
        gal = Ellipse((0, 0), width=3, height=1.7, facecolor="lightgray",
                      edgecolor="dimgray", lw=2, zorder=2)
        ax.add_patch(gal)

        length = max_len * np.sqrt(t) if t > 0 else 0.001

        for sign in [1, -1]:
            cone = Polygon(
                [[0, 0],
                 [sign * length, 0.30],
                 [sign * length, -0.30]],
                closed=True, facecolor=color, edgecolor="none",
                alpha=0.85, zorder=3)
            ax.add_patch(cone)
            lobe_now = lobe * (0.3 + 0.7 * t)
            lb = Ellipse((sign * length, 0), width=lobe_now,
                         height=lobe_now * 1.5, facecolor=color,
                         edgecolor="none", alpha=0.85, zorder=3)
            ax.add_patch(lb)

        if label == "CONFINED" and t > 0.4:
            n_dots = 25
            xs = rng.uniform(-1.3, 1.3, n_dots)
            ys = rng.uniform(-0.7, 0.7, n_dots)
            jitter = 0.05 * np.sin(10 * t * 2 * np.pi + np.arange(n_dots))
            ax.scatter(xs, ys + jitter, s=12, color="mediumorchid",
                       alpha=0.5, zorder=4)

        ax.plot(0, 0, marker="o", ms=9, color="black", zorder=5)
        ax.text(0, -1.6, label, ha="center", fontsize=26, fontweight="bold")
        ax.text(0, -2.0, sub, ha="center", fontsize=14, color="dimgray")
        ax.set_xlim(-3.1, 3.1)
        ax.set_ylim(-2.4, 1.8)
        ax.set_aspect("equal")
        ax.axis("off")

    plt.tight_layout()
    plt.savefig(f"plots/gif_frames/frame_{i:03d}.png", dpi=100)
    plt.close(fig)

# stitch frames into the gif
frames = [Image.open(f) for f in sorted(glob.glob("plots/gif_frames/frame_*.png"))]
frames[0].save("plots/talk_cartoon_jets.gif", save_all=True,
               append_images=frames[1:], duration=80, loop=0)
print("saved plots/talk_cartoon_jets.gif")