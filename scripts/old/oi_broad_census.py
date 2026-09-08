import pandas as pd

fits = pd.read_csv("notes/2026-07-09_oi_fits.csv")
large = pd.read_csv("data/OI_sample_large.csv")
small = pd.read_csv("data/OI_sample_small.csv")

# broad component is real if amp > 3x its own fit error
fits["broad_det"] = fits["oi_broad_amp"] > 3 * fits["oi_broad_amp_err"]

# flag unreliable errors (0 or missing), those cannot be judged
bad_err = (fits["oi_broad_amp_err"] <= 0) | (fits["oi_broad_amp_err"].isna())
print("objects with unusable broad error:", bad_err.sum())
print(fits[bad_err]["TARGETID"].to_string(index=False))

ok = fits[~bad_err]

in_l = ok["TARGETID"].isin(set(large["TARGETID"]))
in_s = ok["TARGETID"].isin(set(small["TARGETID"]))

nb_l = (~ok["broad_det"] & in_l).sum()
nb_s = (~ok["broad_det"] & in_s).sum()
print("large: ", nb_l, "of", in_l.sum(), "have no broad OI component")
print("small: ", nb_s, "of", in_s.sum(), "have no broad OI component")