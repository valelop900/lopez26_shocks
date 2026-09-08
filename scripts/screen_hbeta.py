import pandas as pd
import numpy as np

f = pd.read_csv("notes/2026-07-15_hbeta_fits.csv")
zt = f["Z"]

c = 299792.458
hb_obs = 4861.3 * (1 + zt)
floor_kms = c * 30.0 / hb_obs
ceil_kms = c * 150.0 / hb_obs

pinned_low = np.isclose(f["hb_vbroad_sigma_kms"], floor_kms, rtol=0.02)
pinned_high = np.isclose(f["hb_vbroad_sigma_kms"], ceil_kms, rtol=0.02)
detected = f["hb_vbroad_amp"] > 3 * f["hb_vbroad_amp_err"]

real = detected & ~pinned_low & ~pinned_high
print("very broad detected (3x err, not pinned):", real.sum(), "of", len(f))
print("pinned at 30 A floor:", pinned_low.sum())
print("pinned at 150 A ceiling:", pinned_high.sum())
print()
print("objects with a real very broad component:")
print(f[real][["TARGETID", "hb_vbroad_amp", "hb_vbroad_sigma_kms"]].to_string(index=False))
print()

bd = f["hb_broad_amp"] > 3 * f["hb_broad_amp_err"]
print("broad detected:", bd.sum(), "of", len(f))
print("narrow amp median:", round(f["hb_narrow_amp"].median(), 2))