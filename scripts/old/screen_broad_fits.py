import pandas as pd

fits = pd.read_csv("notes/2026-07-08_oiii_fits.csv")

det = fits[fits["oiii_broad_amp"] > 3 * fits["oiii_broad_amp_err"]].copy()

# broad flux relative to narrow flux, roughly amp x sigma each
det["broad_share"] = (det["oiii_broad_amp"] * det["oiii_broad_sigma_kms"]) / \
                     (det["oiii_narrow_amp"] * det["oiii_narrow_sigma_kms"] + 1e-9)

print("broad-detected objects:", len(det))
print()
print("check these: widest broad components (possible noise-sculpting or pinned)")
top_wide = det.sort_values("oiii_broad_sigma_kms", ascending=False).head(5)
print(top_wide[["TARGETID", "oiii_broad_sigma_kms", "oiii_broad_amp", "oiii_broad_amp_err"]].to_string(index=False))
print()
print("check these: broad flux dominates narrow (most influence on the average)")
top_share = det.sort_values("broad_share", ascending=False).head(5)
print(top_share[["TARGETID", "broad_share", "oiii_broad_sigma_kms"]].to_string(index=False))