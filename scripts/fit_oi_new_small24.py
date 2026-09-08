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

        oi = 6300.3 * (1 + z)
        oi_6364 = 6363.8 * (1 + z)

        sp = pyspeckit.Spectrum(data=flam, xarr=lam, xarrkwargs={'unit':'Angstrom'})
        sp.plotter(xmin=oi-80, xmax=oi+80)
        sp.baseline(xmin=oi-80, xmax=oi+80,
                    exclude=[oi-25, oi+25, oi_6364-15, oi_6364+15],
                    subtract=True, order=1)

        guesses = [5, oi, 2.5, 2, oi, 10.0]
        limits = [(0, 0), (oi-10, oi+10), (0.5, 4.5),
                  (0, 0), (oi-5, oi+5), (4.5, 30.0)]
        limited = [(True, False), (True, True), (True, True),
                   (True, False), (True, True), (True, True)]

        sp.specfit(fittype='gaussian', guesses=guesses, limits=limits, limited=limited)

        v = sp.specfit.parinfo.values
        e = sp.specfit.parinfo.errors
        narrow_kms = c * abs(v[2]) / v[1]
        broad_kms = c * abs(v[5]) / v[4]
        results.append([tid, z, v[0], e[0], narrow_kms, v[3], e[3], broad_kms])

        sp.plotter.savefig("plots/oi_double_" + str(tid) + ".png")
        plt.close('all')
        print(n, tid, round(narrow_kms, 1), round(broad_kms, 1))
    except Exception as e:
        failed.append(tid)
        print(n, tid, "FAILED", e)

df = pd.DataFrame(results, columns=["TARGETID", "Z", "oi_narrow_amp", "oi_narrow_amp_err", "oi_narrow_sigma_kms", "oi_broad_amp", "oi_broad_amp_err", "oi_broad_sigma_kms"])
df.to_csv("notes/2026-07-31_oi_fits_new_small24.csv", index=False)
print("fit", len(results), "failed", len(failed))
print(failed)