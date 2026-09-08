import numpy as np
import pandas as pd
import pyspeckit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

zt = pd.read_csv("notes/targetid_redshift.csv")
good = [int(line.strip()) for line in open("notes/2026-07-22_new_large_targetids.txt")]

c = 299792.458
ratio = 4958.9 / 5006.8
results = []
failed = []

for n, tid in enumerate(good, 1):
    try:
        spec = pd.read_csv("data/spectra/" + str(tid) + "_desispec.csv")
        lam = spec["Lambda"].values
        flam = spec["FLambda17"].values
        z = zt.loc[zt["TARGETID"] == tid, "Z"].values[0]

        o5007 = 5006.8 * (1 + z)
        o4959 = 4958.9 * (1 + z)

        sp = pyspeckit.Spectrum(data=flam, xarr=lam, xarrkwargs={'unit':'Angstrom'})
        sp.plotter(xmin=o4959-60, xmax=o5007+80)
        sp.baseline(xmin=o4959-60, xmax=o5007+80,
                    exclude=[o4959-25, o5007+25],
                    subtract=True, order=1)

        # fit 4959 and 5007 together, 4959 tied to 5007 with 1/3 flux
        # params: narrow5007, broad5007, narrow4959, broad4959
        guesses = [10, o5007, 2.5, 4, o5007, 10.0,
                   3.3, o4959, 2.5, 1.3, o4959, 10.0]
        limits = [(0, 0), (o5007-10, o5007+10), (0.5, 4.5),
                  (0, 0), (o5007-5, o5007+5), (4.5, 30.0),
                  (0, 0), (0, 0), (0, 0),
                  (0, 0), (0, 0), (0, 0)]
        limited = [(True, False), (True, True), (True, True),
                   (True, False), (True, True), (True, True),
                   (False, False), (False, False), (False, False),
                   (False, False), (False, False), (False, False)]
        tied = ['', '', '', '', '', '',
                'p[0]/3.0', 'p[1]*' + str(ratio), 'p[2]*' + str(ratio),
                'p[3]/3.0', 'p[4]*' + str(ratio), 'p[5]*' + str(ratio)]

        sp.specfit(fittype='gaussian', guesses=guesses,
                   limits=limits, limited=limited, tied=tied)

        v = sp.specfit.parinfo.values
        errs = sp.specfit.parinfo.errors
        narrow_kms = c * abs(v[2]) / v[1]
        broad_kms = c * abs(v[5]) / v[4]
        results.append([tid, z, v[0], errs[0], narrow_kms, v[3], errs[3], broad_kms])

        sp.plotter.savefig("plots/oiii_double_" + str(tid) + ".png")
        plt.close('all')
        print(n, tid, round(narrow_kms, 1), round(broad_kms, 1))
    except Exception as e:
        failed.append(tid)
        print(n, tid, "FAILED", e)

df = pd.DataFrame(results, columns=["TARGETID", "Z", "oiii_narrow_amp", "oiii_narrow_amp_err", "oiii_narrow_sigma_kms", "oiii_broad_amp", "oiii_broad_amp_err", "oiii_broad_sigma_kms"])
df.to_csv("notes/2026-07-22_oiii_fits_new_large.csv", index=False)
print("fit", len(results), "failed", len(failed))
print(failed)