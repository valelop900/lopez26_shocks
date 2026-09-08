import pandas as pd
import numpy as np

zt = pd.read_csv("notes/targetid_redshift.csv")
fits = pd.read_csv("notes/2026-07-09_oi_fits.csv")

dlam = 0.8   # desi pixel size in angstrom

noises = []
for tid in fits["TARGETID"]:
    spec = pd.read_csv("data/spectra/" + str(tid) + "_desispec.csv")
    z = zt.loc[zt["TARGETID"] == tid, "Z"].values[0]
    oi = 6300.3 * (1 + z)
    lam = spec["Lambda"].values
    flam = spec["FLambda17"].values
    m = ((lam > oi-80) & (lam < oi-30)) | ((lam > oi+30) & (lam < oi+80))
    coef = np.polyfit(lam[m], flam[m], 1)
    resid = flam[m] - np.polyval(coef, lam[m])
    noises.append(np.std(resid))

fits["noise"] = noises

# integrated line flux and its uncertainty, per component
sig_n = fits["oi_narrow_sigma_kms"] / 299792.458 * 6300.3 * (1 + fits["Z"])
sig_b = fits["oi_broad_sigma_kms"] / 299792.458 * 6300.3 * (1 + fits["Z"])

flux_n = fits["oi_narrow_amp"] * sig_n * np.sqrt(2*np.pi)
flux_b = fits["oi_broad_amp"] * sig_b * np.sqrt(2*np.pi)

# noise on the integrated flux: pixel noise summed over about 4 sigma of line
err_n = fits["noise"] * np.sqrt(4 * sig_n * dlam)
err_b = fits["noise"] * np.sqrt(4 * sig_b * dlam)

fits["narrow_snr"] = flux_n / err_n
fits["broad_snr"] = flux_b / err_b
fits.to_csv("notes/2026-07-09_oi_fits.csv", index=False)

print("narrow detected (snr>3):", (fits["narrow_snr"] > 3).sum(), "of", len(fits))
print("broad detected (snr>3):", (fits["broad_snr"] > 3).sum(), "of", len(fits))
print()
print("narrow not detected:")
print(fits[fits["narrow_snr"] <= 3]["TARGETID"].to_string(index=False))