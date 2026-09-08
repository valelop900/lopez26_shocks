import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 18})

tid = "39627974818924181"

spec = pd.read_csv(f"data/spectra/{tid}_desispec.csv")
print(spec.columns.tolist())

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(spec["Lambda"], spec["FLambda17"], color="k", lw=0.6)
ax.set_xlabel("wavelength")
ax.set_yticks([])
ax.set_ylabel("brightness")
plt.tight_layout()
plt.savefig("plots/talk_one_spectrum.png", dpi=200)
print("saved plots/talk_one_spectrum.png")