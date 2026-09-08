import pandas as pd

def flux(amp, sig_kms, lam0):
    return amp * sig_kms * lam0

oi_all = pd.concat([pd.read_csv("notes/2026-07-09_oi_fits.csv"),
                     pd.read_csv("notes/2026-07-22_oi_fits_new_large.csv")], ignore_index=True)

row = oi_all[oi_all["TARGETID"] == 39633248430590790]
print(row[["oi_narrow_amp", "oi_narrow_sigma_kms", "oi_broad_amp", "oi_broad_sigma_kms"]])

f_narrow = flux(row["oi_narrow_amp"], row["oi_narrow_sigma_kms"], 6300.3)
f_broad = flux(row["oi_broad_amp"], row["oi_broad_sigma_kms"], 6300.3)
print("narrow flux:", f_narrow.values)
print("broad flux:", f_broad.values)
print("total flux:", (f_narrow + f_broad).values)
