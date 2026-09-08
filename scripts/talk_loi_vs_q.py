import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 18})

oi = pd.concat([pd.read_csv("notes/2026-07-09_oi_fits.csv"),
                pd.read_csv("notes/2026-07-22_oi_fits_new_large.csv"),
                pd.read_csv("notes/2026-07-31_oi_fits_new_small24.csv")], ignore_index=True)

bpt = pd.read_csv("notes/2026-07-31_bpt_class_lumcut_v2.csv")
size = pd.read_csv("notes/2026-07-28_luminosity_check.csv")[["TARGETID", "Physical_Size", "log_L_radio"]]

cols = ["TARGETID", "Z", "Flux", "Alpha", "D_L"]
c1 = pd.read_csv("data/OI_sample_large.csv")[cols]
c2 = pd.read_csv("data/OI_sample_small.csv")[cols]
c3 = pd.read_csv("data/VLASS3_2_OI_large.csv").rename(columns={"TARGETID_1": "TARGETID"})[cols]
c4 = pd.read_csv("data/VLASS3_2_OI_small.csv").rename(columns={"TARGETID_1": "TARGETID"})[cols]
cat = pd.concat([c1, c2, c3, c4], ignore_index=True).drop_duplicates("TARGETID")

m = oi.merge(bpt[["TARGETID", "sample"]], on="TARGETID")
m = m.merge(size, on="TARGETID")
catm = cat.rename(columns={"Z": "Z_cat", "Flux": "Flux_cat",
                           "Alpha": "Alpha_cat", "D_L": "DL_cat"})
m = m.merge(catm, on="TARGETID")
m = m[m["log_L_radio"] > 24]
m = m[(m["sample"] == "small") | (m["Physical_Size"] > 25)]
print("n =", len(m))

# jet power: Willott 1999, f=1
dl_m = m["DL_cat"] * 3.086e22
L3 = 4 * np.pi * dl_m**2 * m["Flux_cat"] * 1e-29 * (1 + m["Z_cat"])**(-(1 + m["Alpha_cat"]))
L151 = L3 * (0.151 / 3.0)**(m["Alpha_cat"]) / (4 * np.pi)
logQ = np.log10(3e38 * (L151 / 1e28)**(6.0 / 7.0))

# [OI] luminosity from the fits
c_kms = 2.998e5
f_oi = np.sqrt(2 * np.pi) * 6300.3 / c_kms * (
    m["oi_narrow_amp"] * m["oi_narrow_sigma_kms"]
    + m["oi_broad_amp"] * m["oi_broad_sigma_kms"])

ok = f_oi > 0
logQ, logLoi, samp = logQ[ok], logLoi[ok], m["sample"][ok].values

print("median logQ large:", round(np.median(logQ[samp == "large"]), 2))
print("median logQ small:", round(np.median(logQ[samp == "small"]), 2))

fig, ax = plt.subplots(figsize=(8, 6.5))
ax.scatter(logQ[samp == "large"], logLoi[samp == "large"],
           marker="s", color="dimgray", s=60, label="escaped")
ax.scatter(logQ[samp == "small"], logLoi[samp == "small"],
           marker="o", facecolors="none", edgecolors="plum",
           s=60, linewidths=1.8, label="confined")

lims = np.array([min(logQ.min(), logLoi.min()) - 0.3, max(logQ.max(), logLoi.max()) + 0.3])
ax.plot(lims, lims, "k--", lw=1)
ax.plot(lims, lims - 2, "k:", lw=1)
ax.text(lims[1] - 0.1, lims[1] - 0.5, "all of the jet power", ha="right", fontsize=14)
ax.text(lims[1] - 0.1, lims[1] - 2.5, "1% of the jet power", ha="right", fontsize=14)

ax.set_xlim(lims)
ax.set_xlabel("jet power  log Q (W)")
ax.set_ylabel("[OI] line power  log L (W)")
ax.legend(loc="upper left")
plt.tight_layout()
plt.savefig("plots/talk_loi_vs_q.png", dpi=200)
print("saved plots/talk_loi_vs_q.png")