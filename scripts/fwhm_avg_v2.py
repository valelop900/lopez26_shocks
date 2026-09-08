import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, ks_2samp

f1 = pd.read_csv("notes/2026-07-13_resolution_w80.csv")
f2 = pd.read_csv("notes/2026-07-22_w80_new_large.csv")
f3 = pd.read_csv("notes/2026-07-31_w80_new_small24.csv")
fits = pd.concat([f1, f2, f3], ignore_index=True)

fwhm_n = 2.3548 * fits["oiii_narrow_sigma_kms"]
fwhm_b = 2.3548 * fits["oiii_broad_sigma_kms"]
flux_n = fits["oiii_narrow_amp"] * fits["oiii_narrow_sigma_kms"]
flux_b = (fits["oiii_broad_amp"] * fits["oiii_broad_sigma_kms"]).fillna(0)
fwhm_b = fwhm_b.fillna(0)
ftot = flux_n + flux_b

# flux weighted mean, not quadrature (bug in v1)
fits["fwhm_avg"] = (fwhm_n * flux_n + fwhm_b * flux_b) / ftot

lum = pd.read_csv("notes/2026-07-28_luminosity_check.csv")[["TARGETID", "log_L_radio"]]
fits = fits.merge(lum, on="TARGETID")
cut = fits[fits["log_L_radio"] > 24]

l = cut[cut["sample"] == "large"]["fwhm_avg"]
s = cut[cut["sample"] == "small"]["fwhm_avg"]
print("after cut: large", len(l), "small", len(s))
print("median fwhm_avg large %.1f  small %.1f" % (l.median(), s.median()))
print("KS p = %.4f  MW p = %.4f" % (ks_2samp(l, s).pvalue, mannwhitneyu(l, s).pvalue))

fits[["TARGETID", "Z", "sample", "fwhm_avg", "w80", "log_L_radio"]].to_csv("notes/2026-07-31_fwhm_avg_v2.csv", index=False)
