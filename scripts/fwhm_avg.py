import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

fits = pd.read_csv("notes/2026-07-08_oiii_fits.csv")
large = pd.read_csv("data/OI_sample_large.csv")

# exclude the two unmeasurable objects
exclude = [39627802344950353, 39627701220278777]
fits = fits[~fits["TARGETID"].isin(exclude)].copy()

# fwhm = 2.3548 sigma, flux of each gaussian goes as amp x sigma
fwhm_n = 2.3548 * fits["oiii_narrow_sigma_kms"]
fwhm_b = 2.3548 * fits["oiii_broad_sigma_kms"]
flux_n = fits["oiii_narrow_amp"] * fits["oiii_narrow_sigma_kms"]
flux_b = fits["oiii_broad_amp"] * fits["oiii_broad_sigma_kms"]
ftot = flux_n + flux_b
fn = flux_n / ftot
fb = flux_b / ftot

fits["fwhm_avg"] = np.sqrt((fwhm_n * fn)**2 + (fwhm_b * fb)**2)

fits["sample"] = ["large" if t in set(large["TARGETID"]) else "small" for t in fits["TARGETID"]]

l = fits[fits["sample"] == "large"]["fwhm_avg"]
s = fits[fits["sample"] == "small"]["fwhm_avg"]

print("large:", len(l), "objects, median fwhm_avg", round(l.median(), 1), "km/s")
print("small:", len(s), "objects, median fwhm_avg", round(s.median(), 1), "km/s")

stat, p = ks_2samp(l, s)
print("KS test p-value:", round(p, 4))

fits[["TARGETID", "Z", "sample", "fwhm_avg"]].to_csv("notes/2026-07-13_fwhm_avg.csv", index=False)
print("saved notes/2026-07-13_fwhm_avg.csv")