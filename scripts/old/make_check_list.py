import pandas as pd

fits = pd.read_csv("notes/2026-07-08_oiii_fits.csv")
large = pd.read_csv("data/OI_sample_large.csv")

fits["broad_det"] = fits["oiii_broad_amp"] > 3 * fits["oiii_broad_amp_err"]
fits["sample"] = ["large" if t in set(large["TARGETID"]) else "small" for t in fits["TARGETID"]]

bad_err = (fits["oiii_broad_amp_err"] <= 0) | (fits["oiii_broad_amp_err"].isna())

print("PRIORITY 1: no-broad objects, check these carefully")
nb = fits[~fits["broad_det"] & ~bad_err]
for _, r in nb.iterrows():
    print(r["sample"], r["TARGETID"], "broad_amp", round(r["oiii_broad_amp"], 2), "err", round(r["oiii_broad_amp_err"], 2))

print()
print("PRIORITY 2: unusable error")
for _, r in fits[bad_err].iterrows():
    print(r["sample"], r["TARGETID"])

print()
print("PRIORITY 3: control sample, 5 broad-detected to compare against")
det = fits[fits["broad_det"]].sample(5, random_state=1)
for _, r in det.iterrows():
    print(r["sample"], r["TARGETID"], "broad_amp", round(r["oiii_broad_amp"], 2), "err", round(r["oiii_broad_amp_err"], 2))