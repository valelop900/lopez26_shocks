import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

oiii = pd.read_csv("notes/2026-07-08_oiii_fits.csv")
oi = pd.read_csv("notes/2026-07-09_oi_fits.csv")
hb = pd.read_csv("notes/2026-07-15_hbeta_fits.csv")
ha = pd.read_csv("notes/2026-07-16_halpha_fits.csv")
large = pd.read_csv("data/OI_sample_large.csv")

# flux of a gaussian goes as amp x sigma x rest wavelength


def flux(amp, sig_kms, lam0):
    return amp * sig_kms * lam0

m = oiii.merge(oi, on="TARGETID", suffixes=("", "_oi"))
m = m.merge(hb, on="TARGETID", suffixes=("", "_hb"))
m = m.merge(ha, on="TARGETID", suffixes=("", "_ha"))

f_oiii = flux(m["oiii_narrow_amp"], m["oiii_narrow_sigma_kms"], 5006.8) \
       + flux(m["oiii_broad_amp"], m["oiii_broad_sigma_kms"], 5006.8)
f_oi = flux(m["oi_narrow_amp"], m["oi_narrow_sigma_kms"], 6300.3) \
     + flux(m["oi_broad_amp"], m["oi_broad_sigma_kms"], 6300.3)
f_hb = flux(m["hb_narrow_amp"], m["hb_narrow_sigma_kms"], 4861.3) \
     + flux(m["hb_broad_amp"], m["hb_broad_sigma_kms"], 4861.3)
f_ha = flux(m["ha_narrow_amp"], m["ha_narrow_sigma_kms"], 6562.8) \
     + flux(m["ha_broad_amp"], m["ha_broad_sigma_kms"], 6562.8)

# keep objects where all four lines have positive flux
ok = (f_oiii > 0) & (f_oi > 0) & (f_hb > 0) & (f_ha > 0)
print("objects with all four lines measured:", ok.sum(), "of", len(m))

x = np.log10(f_oi[ok] / f_ha[ok])
y = np.log10(f_oiii[ok] / f_hb[ok])
tid = m["TARGETID"][ok]
samp = ["large" if t in set(large["TARGETID"]) else "small" for t in tid]
samp = np.array(samp)

# kewley 2006 lines for the OI diagram
# starburst boundary: y = 0.73/(x+0.59) + 1.33, for x < -0.59
# seyfert-liner boundary: y = 1.18x + 1.30
def kewley(xv):
    return 0.73 / (xv + 0.59) + 1.33

def syliner(xv):
    return 1.18 * xv + 1.30

above_k = y > kewley(np.where(x < -0.59, x, -0.6))
is_agn = above_k | (x >= -0.59)
is_sy = is_agn & (y > syliner(x))
is_lin = is_agn & ~is_sy

cls = np.where(is_sy, "seyfert", np.where(is_lin, "liner", "sf"))
out = pd.DataFrame({"TARGETID": tid.values, "sample": samp,
                    "log_oi_ha": x.values, "log_oiii_hb": y.values, "bpt_class": cls})
out.to_csv("notes/2026-07-16_bpt_class.csv", index=False)

print()
print(pd.crosstab(out["sample"], out["bpt_class"]))

plt.figure(figsize=(7, 6))
for s, mk in [("large", "s"), ("small", "o")]:
    sel = samp == s
    plt.scatter(x[sel], y[sel], marker=mk, label=s, alpha=0.8)
xk = np.linspace(-2.5, -0.63, 100)
plt.plot(xk, kewley(xk), 'k-', lw=1)
xs = np.linspace(-1.12, 0.4, 50)
plt.plot(xs, syliner(xs), 'k--', lw=1)
plt.text(-2.2, 1.4, "Seyfert")
plt.text(-0.5, 0.0, "LINER")
plt.text(-2.2, -0.5, "star forming")
plt.xlabel("log [OI]6300 / Ha")
plt.ylabel("log [OIII]5007 / Hb")
plt.xlim(-2.5, 0.5)
plt.ylim(-1.5, 2.2)
plt.legend()
plt.tight_layout()
plt.savefig("plots/bpt_oi.png", dpi=150)
print("saved plots/bpt_oi.png and notes/2026-07-16_bpt_class.csv")