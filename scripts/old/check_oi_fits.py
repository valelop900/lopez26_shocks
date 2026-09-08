import pandas as pd

df = pd.read_csv("notes/2026-07-09_oi_fits.csv")

swapped = df[df["oi_narrow_sigma_kms"] > df["oi_broad_sigma_kms"]]
print("swapped:", len(swapped))
print(swapped[["TARGETID", "oi_narrow_sigma_kms", "oi_broad_sigma_kms"]].to_string(index=False))

pinned = df[df["oi_broad_sigma_kms"] > 1200]
print("possibly pinned broad:", len(pinned))
print(pinned[["TARGETID", "oi_broad_sigma_kms"]].to_string(index=False))

weak = df[df["oi_broad_amp"] < 1]
print("weak broad:", len(weak))
print(weak[["TARGETID", "oi_broad_amp"]].to_string(index=False))

# oi is faint, also check for objects where even the narrow line is basically nothing
weak_narrow = df[df["oi_narrow_amp"] < 1]
print("weak narrow (line barely detected):", len(weak_narrow))
print(weak_narrow[["TARGETID", "oi_narrow_amp"]].to_string(index=False))