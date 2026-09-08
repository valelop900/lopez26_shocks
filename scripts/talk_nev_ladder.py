import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 18})

lines = ["hydrogen\n(Ha)", "oxygen\n([OIII])", "neon\n([NeV])"]
energy = [13.6, 35.1, 97.1]
colors = ["lightgray", "darkgray", "#5B2C6F"]

fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.bar(lines, energy, color=colors, width=0.55)
for b, e in zip(bars, energy):
    ax.text(b.get_x() + b.get_width() / 2, e + 2, f"{e:.0f} eV", ha="center")

ax.axhspan(0, 25, color="gold", alpha=0.12)
ax.text(0, 25.5, "hot stars can do this", ha="center", fontsize=16, color="darkgoldenrod")
ax.text(1.62, 85, "only the black hole's\nfiercest light", ha="right", fontsize=16, color="#5B2C6F")

ax.set_ylabel("energy needed to light it up (eV)")
ax.set_ylim(0, 115)
plt.tight_layout()
plt.savefig("plots/talk_nev_ladder.png", dpi=200)
print("saved plots/talk_nev_ladder.png")