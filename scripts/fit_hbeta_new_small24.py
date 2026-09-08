import numpy as np
import pandas as pd
import pyspeckit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

zt = pd.read_csv("notes/targetid_redshift.csv")
good = [int(line.strip()) for line in open("notes/2026-07-31_new_small24_targetids.txt")]

c = 299792.458
results = []
failed = []

for n, tid in enumerate(good, 1):
    try:
        spec = pd.read_csv("data/spectra/" + str(tid) + "_desispec.csv")
        lam = spec["Lambda"].values
        flam = spec["FLambda17"].values
        z = zt.loc[zt["TARGETID"] == tid, "Z"].values[0]

        hb = 4861.3 * (1 + z)
        o4959 = 4958.9 * (1 + z)
        o5007 = 5006.8 * (1 + z)

        sp = pyspeckit.Spectrum(data=flam, xarr=lam, xarrkwargs={'unit':'Angstrom'})
        sp.plotter(xmin=hb-300, xmax=hb+300)
        sp.baseline(xmin=hb-300, xmax=hb+300,
                    exclude=[hb-60, hb+60, o4959-25, o5007+30],
                    subtract=True, order=1)

        # three components: narrow, broad, very broad
        guesses = [5, hb, 2.5, 2, hb, 10.0, 1, hb, 50.0]
        limits = [(0, 0), (hb-10, hb+10), (0.5, 4.5),
                  (0, 0), (hb-5, hb+5), (4.5, 30.0),
                  (0, 0), (hb-15, hb+15), (30.0, 150.0)]
        limited = [(True, False), (True, True), (True, True),
                   (True, False), (True, True), (True, True),
                   (True, False), (True, True), (True, True)]

        sp.specfit(fittype='gaussian', guesses=guesses,
                   limits=limits, limited=limited,
                   xmin=hb-300, xmax=o4959-30)

        v = sp.specfit.parinfo.values
        errs = sp.specfit.parinfo.errors
        narrow_kms = c * abs(v[2]) / v[1]
        broad_kms = c * abs(v[5]) / v[4]
        vbroad_kms = c * abs(v[8]) / v[7]
        results.append([tid, z, v[0], errs[0], narrow_kms,
                        v[3], errs[3], broad_kms,
                        v[6], errs[6], vbroad_kms])

        sp.plotter.savefig("plots/hbeta_triple_" + str(tid) + ".png")
        plt.close('all')
        print(n, tid, round(narrow_kms, 1), round(broad_kms, 1), round(vbroad_kms, 1))
    except Exception as e:
        failed.append(tid)
        print(n, tid, "FAILED", e)

df = pd.DataFrame(results, columns=["TARGETID", "Z",
    "hb_narrow_amp", "hb_narrow_amp_err", "hb_narrow_sigma_kms",
    "hb_broad_amp", "hb_broad_amp_err", "hb_broad_sigma_kms",
    "hb_vbroad_amp", "hb_vbroad_amp_err", "hb_vbroad_sigma_kms"])
df.to_csv("notes/2026-07-31_hbeta_fits_new_small24.csv", index=False)
print("fit", len(results), "failed", len(failed))
print(failed)