import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 20, "font.family": "sans-serif"})

narrow_id = "39627842677376414"
broad_id = "39627974818924181"
narrow_z = 0.158628
broad_z = 0.455077
narrow_w80 = 363
broad_w80 = 1172

c = 299792.458
rest = 5006.84

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), sharey=True)

panels = [
    (axes[0], narrow_id, narrow_z, "calm gas", narrow_w80, "dimgray"),
    (axes[1], broad_id, broad_z, "disturbed gas", broad_w80, "purple"),
]

for ax, tid, z, label, w80, color in panels:
    spec = pd.read_csv(f"data/spectra/{tid}_desispec.csv")
    wave = spec["Lambda"] / (1 + z)
    vel = (wave - rest) / rest * c
    flux = spec["FLambda17"]

    keep = (vel > -2500) & (vel < 2500)
    flux = flux / np.nanmax(flux[keep])

    ax.fill_between(vel, 0, flux, where=(np.abs(vel) < w80 / 2),
                    color=color, alpha=0.25, zorder=1)
    ax.plot(vel, flux, color="black", lw=2, zorder=2)
    ax.axvline(0, color="gray", ls=":", lw=1, zorder=0)

    ax.set_xlim(-2500, 2500)
    ax.set_ylim(-0.15, 1.3)
    ax.set_xlabel("gas velocity (km/s)")
    ax.set_title(label, fontsize=24, pad=12)
    ax.set_yticks([])
    ax.set_xticks([-2000, -1000, 0, 1000, 2000])
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)

    ax.annotate("", xy=(-w80/2, 1.15), xytext=(w80/2, 1.15),
                arrowprops=dict(arrowstyle="<->", color=color, lw=2.5))
    ax.text(0, 1.19, f"{w80} km/s", ha="center", fontsize=19,
            color=color, fontweight="bold")

axes[0].set_ylabel("brightness")

plt.tight_layout()
plt.savefig("plots/talk_spectrum_compare.png", dpi=200, facecolor="white")