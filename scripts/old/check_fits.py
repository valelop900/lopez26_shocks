import pandas as pd

df = pd.read_csv("notes/2026-07-08_oiii_fits.csv")

# swapped: narrow came out wider than broad
swapped = df[df["oiii_narrow_sigma_kms"] > df["oiii_broad_sigma_kms"]]
print("swapped:", len(swapped))
print(swapped[["TARGETID", "oiii_narrow_sigma_kms", "oiii_broad_sigma_kms"]].to_string(index=False))

# pinned: broad sigma at the upper limit (30 A is about 1300-1500 km/s depending on z)
pinned = df[df["oiii_broad_sigma_kms"] > 1200]
print("possibly pinned broad:", len(pinned))
print(pinned[["TARGETID", "oiii_broad_sigma_kms"]].to_string(index=False))

# weak broad: amplitude near zero means no real broad component
weak = df[df["oiii_broad_amp"] < 1]
print("weak broad:", len(weak))
print(weak[["TARGETID", "oiii_broad_amp"]].to_string(index=False))