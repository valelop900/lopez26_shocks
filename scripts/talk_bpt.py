import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 18})

oiii = pd.concat([pd.read_csv("notes/2026-07-08_oiii_fits.csv"),
                  pd.read_csv("notes/2026-07-22_oiii_fits_new_large.csv"),
                  pd.read_csv("notes/2026-07-31_oiii_fits_new_small24.csv")], ignore_index=True)
oi = pd.concat([pd.read_csv("notes/2026-07-09_oi_fits.csv"),
                pd.read_csv("notes/2026-07-22_oi_fits_new_large.csv"),
                pd.read_csv("notes/2026-07-31_oi_fits_new_small24.csv")], ignore_index=True)
hb = pd.concat([pd.read_csv("notes/2026-07-15_hbeta_fits.csv"),
                pd.read_csv("notes/2026-07-22_hbeta_fits_new_large.csv"),
                pd.read_csv("notes/2026-07-31_hbeta_fits_new_small24.csv")], ignore_index=True)
ha = pd.concat([pd.read_csv("notes/2026-07-16_halpha_fits.csv"),
                pd.read_csv("notes/2026-07-22_halpha_fits_new_large.csv"),
                pd.read_csv("notes/2026-07-31_halpha_fits_new_small24.csv")], ignore_index=True)

large = pd.read_csv("data/OI_sample_large.csv")
new_large = [int(l) for l in open("notes/2026-07-22_new_large_targetids.txt")]
large_ids = set(large["TARGETID"]) | set(new_large)

def flux(amp, sig_kms, lam0):
    return amp * sig_kms * lam0

m = oiii.merge(oi, on="TARGETID", suffixes=("", "_oi"))
m = m.merge(hb, on="TARGETID", suffixes=("", "_hb"))
m = m.merge(ha, on="TARGETID", suffixes=("", "_ha"))

cols = ["TARGETID", "Z", "Flux", "Alpha"]
c1 = pd.read_csv("data/OI_sample_large.csv")[cols + ["D_L"]]
c2 = pd.read_csv("data/OI_sample_small.csv")[cols + ["D_L"]]
c3 = pd.read_csv("data/VLASS3_2_OI_large.csv").rename(columns={"TARGETID_1": "TARGETID"})[cols + ["D_L"]]
c4 = pd.read_csv("data/VLASS3_2_OI_small.csv").rename(columns={"TARGETID_1": "TARGETID"})[cols + ["D_L"]]
cat = pd.concat([c1, c2, c3, c4], ignore_index=True)

dl_m = cat["D_L"] * 3.086e22
cat["log_L_radio"] = np.log10(4 * np.pi * dl_m**2 * cat["Flux"] * 1e-29 * (1 + cat["Z"])**(-0.3))

m = m.merge(cat[["TARGETID", "log_L_radio"]], on="TARGETID", how="left")
m = m[m["log_L_radio"] > 24]

f_oiii = flux(m["oiii_narrow_amp"], m["oiii_narrow_sigma_kms"], 5006.8) \
       + flux(m["oiii_broad_amp"], m["oiii_broad_sigma_kms"], 5006.8)
f_oi = flux(m["oi_narrow_amp"], m["oi_narrow_sigma_kms"], 6300.3) \
     + flux(m["oi_broad_amp"], m["oi_broad_sigma_kms"], 6300.3)
f_hb = flux(m["hb_narrow_amp"], m["hb_narrow_sigma_kms"], 4861.3) \
     + flux(m["hb_broad_amp"], m["hb_broad_sigma_kms"], 4861.3)
f_ha = flux(m["ha_narrow_amp"], m["ha_narrow_sigma_kms"], 6562.8) \
     + flux(m["ha_broad_amp"], m["ha_broad_sigma_kms"], 6562.8)

ok = (f_oiii > 0) & (f_oi > 0) & (f_hb > 0) & (f_ha > 0)

x = np.log10(f_oi[ok] / f_ha[ok])
y = np.log10(f_oiii[ok] / f_hb[ok])
tid = m["TARGETID"][ok]
samp = np.array(["large" if t in large_ids else "small" for t in tid])

def kewley(xv):
    return 0.73 / (xv + 0.59) + 1.33

def syliner(xv):
    return 1.18 * xv + 1.30

plt.figure(figsize=(8, 7))
for s, mk, c, lab in [("large", "s", "dimgray", "escaped"), ("small", "o", "plum", "confined")]:
    sel = samp == s
    plt.scatter(x[sel], y[sel], marker=mk, color=c, s=60, label=lab, alpha=0.9)
xk = np.linspace(-2.5, -0.63, 100)
plt.plot(xk, kewley(xk), 'k-', lw=1)
xs = np.linspace(-1.12, 0.4, 50)
plt.plot(xs, syliner(xs), 'k--', lw=1)
plt.text(-2.4, 1.6, "lit by the black hole\n(Seyfert)")
plt.text(-0.55, -0.6, "lit by shocks\n(LINER)")
plt.text(-2.4, -1.1, "star forming")
plt.xlabel("log [OI]6300 / Ha")
plt.ylabel("log [OIII]5007 / Hb")
plt.xlim(-2.5, 0.5)
plt.ylim(-1.5, 2.2)
plt.legend()
plt.tight_layout()
plt.savefig("plots/talk_bpt.png", dpi=200)
print("saved plots/talk_bpt.png")