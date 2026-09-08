import pandas as pd

fits = pd.read_csv("notes/2026-07-08_oiii_fits.csv")
large = pd.read_csv("data/OI_sample_large.csv")
small = pd.read_csv("data/OI_sample_small.csv")

fits["broad_det"] = fits["oiii_broad_amp"] > 3 * fits["oiii_broad_amp_err"]

bad_err = (fits["oiii_broad_amp_err"] <= 0) | (fits["oiii_broad_amp_err"].isna())
print("objects with unusable broad error:", bad_err.sum())
print(fits[bad_err]["TARGETID"].to_string(index=False))

ok = fits[~bad_err]

in_l = ok["TARGETID"].isin(set(large["TARGETID"]))
in_s = ok["TARGETID"].isin(set(small["TARGETID"]))

nb_l = (~ok["broad_det"] & in_l).sum()
nb_s = (~ok["broad_det"] & in_s).sum()
print("large: ", nb_l, "of", in_l.sum(), "have no broad OIII component")
print("small: ", nb_s, "of", in_s.sum(), "have no broad OIII component")