import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 18})

fig, ax = plt.subplots(figsize=(7, 5))
ax.bar(["escaped", "confined"], [60, 30], color=["dimgray", "plum"], width=0.55)
ax.set_ylabel("galaxies with [NeV] detected (%)")
ax.set_ylim(0, 100)
for x, v in zip([0, 1], [60, 30]):
    ax.text(x, v + 3, f"{v}%", ha="center")
plt.tight_layout()
plt.savefig("plots/talk_nev_bars.png", dpi=200)