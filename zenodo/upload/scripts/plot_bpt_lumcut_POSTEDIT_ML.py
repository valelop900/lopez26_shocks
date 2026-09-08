import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches

def load(*files):
    return pd.concat([pd.read_csv("notes/" + f) for f in files], ignore_index=True)

oiii = load("2026-07-08_oiii_fits.csv", "2026-07-22_oiii_fits_new_large.csv", "2026-07-31_oiii_fits_new_small24.csv")
oi   = load("2026-07-09_oi_fits.csv", "2026-07-22_oi_fits_new_large.csv", "2026-07-31_oi_fits_new_small24.csv")
hb   = load("2026-07-15_hbeta_fits.csv", "2026-07-22_hbeta_fits_new_large.csv", "2026-07-31_hbeta_fits_new_small24.csv")
ha   = load("2026-07-16_halpha_fits.csv", "2026-07-22_halpha_fits_new_large.csv", "2026-07-31_halpha_fits_new_small24.csv")

def flux(amp, sig_kms, lam0):
    return amp * sig_kms * lam0

m = oiii.merge(oi, on="TARGETID", suffixes=("", "_oi"))
m = m.merge(hb, on="TARGETID", suffixes=("", "_hb"))
m = m.merge(ha, on="TARGETID", suffixes=("", "_ha"))

# cut to the final sample... luminosity and size, no repeats!
lum = pd.read_csv("notes/2026-07-28_luminosity_check.csv").drop_duplicates("TARGETID")
final = lum[lum["log_L_radio"] > 24]
is_large = final["sample"].str.lower().str.contains("large")
final = final[(~is_large) | (final["Physical_Size"] > 25)]
final_ids = set(final["TARGETID"])
sample_of = dict(zip(final["TARGETID"], final["sample"].str.lower()))

m=m[m["TARGETID"].isin(final_ids)].drop_duplicates("TARGETID")
print("in sample and fit:", len(m), "of", len(final_ids))

f_oiii = flux(m["oiii_narrow_amp"], m["oiii_narrow_sigma_kms"], 5006.8) \
       + flux(m["oiii_broad_amp"], m["oiii_broad_sigma_kms"], 5006.8)
f_oi = flux(m["oi_narrow_amp"], m["oi_narrow_sigma_kms"], 6300.3) \
     + flux(m["oi_broad_amp"], m["oi_broad_sigma_kms"], 6300.3)
f_hb = flux(m["hb_narrow_amp"], m["hb_narrow_sigma_kms"], 4861.3) \
     + flux(m["hb_broad_amp"], m["hb_broad_sigma_kms"], 4861.3)
f_ha = flux(m["ha_narrow_amp"], m["ha_narrow_sigma_kms"], 6562.8) \
     + flux(m["ha_broad_amp"], m["ha_broad_sigma_kms"], 6562.8)

ok =(f_oiii > 0) & (f_oi > 0) & (f_hb > 0) & (f_ha > 0)
print("all four lines:", ok.sum(), "of", len(m))

x = np.log10(f_oi[ok] / f_ha[ok])
y = np.log10(f_oiii[ok] / f_hb[ok])
tid = m["TARGETID"][ok]
samp= np.array([sample_of[t] for t in tid])

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
out.to_csv("notes/2026-07-31_bpt_class_lumcut_v2.csv", index=False)

print(pd.crosstab(out["sample"], out["bpt_class"]))

xv =x.values
yv =y.values

#ML - make an axis instance to better control the plotting 
fig=plt.figure(figsize=(6, 6))
ax=fig.add_subplot(111,xlim=(-2.5,0.7),ylim=(-1.2,2.0))
ax.set_aspect=1


styles = {
    ("large", "seyfert"): ("large Seyfert", dict(marker="o", facecolors="black", edgecolors="black")),
    ("large", "liner"):   ("large LINER", dict(marker="*", facecolors="black", edgecolors="black", s=140)),
    ("small", "seyfert"): ("small Seyfert", dict(marker="o", facecolors="none", edgecolors="#5B2C6F")),
    ("small", "liner"):   ("small LINER", dict(marker="*", facecolors="none", edgecolors="#5B2C6F", s=140)),
}
for (s_name, c_name), (lab, st) in styles.items():
    sel = (samp == s_name) & (cls == c_name)
    ax.scatter(xv[sel], yv[sel], label=lab, **st)

sf_sel = (samp == "small") & (cls == "sf")
if sf_sel.any():
    ax.scatter(xv[sf_sel], yv[sf_sel], marker="^", facecolors="none",
                edgecolors="#5B2C6F", label="small SF")

xk = np.linspace(-2.5, -0.63, 100)
ax.plot(xk, kewley(xk), 'k-', lw=1)
xs = np.linspace(-1.12, 0.4, 50)
ax.plot(xs, syliner(xs), 'k--', lw=1)

mslope, b = 1.18, 1.30
# pick the Seyfert-side point with the largest perpendicular distance ABOVE the line
# (ML) pick a point on the line corresponding to x=0.2
xt=0.2
yt=syliner(xt)
# set x position for head to be xh, calculate yh on a line perpendicular to
# the S-L divide
xh=-0.15
m2=-1/1.18
c2=yt-xt*m2
yh=m2*xh+c2

#signed_d = (yv - mslope * xv - b) / np.sqrt(1 + mslope**2)
#cand = (cls == "seyfert") & (signed_d > 0)
#idx = np.where(cand)[0][np.argmax(signed_d[cand])]
#xp, yp = xv[idx], yv[idx]
#xf = (xp + mslope * (yp - b)) / (1 + mslope**2)
#yf =mslope * xf + b
#plt.annotate("", xy=(xp, yp), xytext=(xf, yf),
#             arrowprops=dict(arrowstyle="->", color="tab:red", lw=2), zorder=6)
arrow=mpatches.FancyArrowPatch((xt,yt),(xh,yh),mutation_scale=20,color='r')
ax.add_patch(arrow)
ax.annotate("SL", xy=(xh, yh), xytext=(8, -2),
             textcoords="offset points", color="tab:red", fontweight="bold",
             path_effects=[pe.withStroke(linewidth=3, foreground="white")],fontsize=14)

##########################################################################

ax.text(-2.2, 1.4, "Seyfert",fontsize=14)
ax.text(-0.5, 0.0, "LINER",fontsize=14)
ax.text(-2.2, -0.3, "star forming",fontsize=14)
ax.set_xlabel(r"log [OI]6300 / H$\alpha$",fontsize=14)
ax.set_ylabel(r"log [OIII]5007 / H$\beta$",fontsize=14)
#ax.xlim(-2.5, 0.5)
#ax.ylim(-1.5, 2.2)
ax.legend(loc='lower left')
#ax.tight_layout()
plt.savefig("plots/2026-07-31_bpt_oi_lumcut_v2.png", dpi=150)
plt.savefig("plots/fig_bpt.pdf")
