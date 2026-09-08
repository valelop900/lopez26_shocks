import numpy as np
import pandas as pd
import pyspeckit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

zt = pd.read_csv("notes/targetid_redshift.csv")
good = [int(line.strip()) for line in open("notes/2026-07-07_good_targetids.txt")]

c = 299792.458
r83 = 6583.5 / 6562.8   # NII 6583 relative to Ha
r48 = 6548.1 / 6583.5   # NII 6548 relative to NII 6583
results = []
failed = []
skipped = []

for n, tid in enumerate(good, 1):
    try:
        z = zt.loc[zt["TARGETID"] == tid, "Z"].values[0]
        nii83 = 6583.5 * (1 + z)
        if nii83 > 9790:
            skipped.append(tid)
            print(n, tid, "SKIPPED, Ha region off detector")
            continue

        spec = pd.read_csv("data/spectra/" + str(tid) + "_desispec.csv")
        lam = spec["Lambda"].values
        flam = spec["FLambda17"].values

        ha = 6562.8 * (1 + z)
        nii48 = 6548.1 * (1 + z)
        sii = 6716.4 * (1 + z)

        sp = pyspeckit.Spectrum(data=flam, xarr=lam, xarrkwargs={'unit':'Angstrom'})
        sp.plotter(xmin=ha-250, xmax=ha+250)
        sp.baseline(xmin=ha-250, xmax=ha+250,
                    exclude=[nii48-30, nii83+30, sii-15, sii+40],
                    subtract=True, order=1)

        # params: 0-2 Ha narrow, 3-5 Ha broad, 6-8 Ha very broad,
        #         9-11 NII6583 narrow, 12-14 NII6583 broad,
        #         15-17 NII6548 narrow, 18-20 NII6548 broad
        guesses = [10, ha, 2.5, 4, ha, 10.0, 1, ha, 50.0,
                   5, nii83, 2.5, 2, nii83, 10.0,
                   1.7, nii48, 2.5, 0.7, nii48, 10.0]
        limits = [(0, 0), (ha-10, ha+10), (0.5, 4.5),
                  (0, 0), (ha-5, ha+5), (4.5, 30.0),
                  (0, 0), (ha-15, ha+15), (30.0, 150.0),
                  (0, 0), (0, 0), (0, 0),
                  (0, 0), (0, 0), (0, 0),
                  (0, 0), (0, 0), (0, 0),
                  (0, 0), (0, 0), (0, 0)]
        limited = [(True, False), (True, True), (True, True),
                   (True, False), (True, True), (True, True),
                   (True, False), (True, True), (True, True),
                   (True, False), (False, False), (False, False),
                   (True, False), (False, False), (False, False),
                   (False, False), (False, False), (False, False),
                   (False, False), (False, False), (False, False)]
        # NII kinematics tied to Ha, NII6548 amp locked to 1/3 of 6583
        tied = ['', '', '', '', '', '', '', '', '',
                '', 'p[1]*' + str(r83), 'p[2]*' + str(r83),
                '', 'p[4]*' + str(r83), 'p[5]*' + str(r83),
                'p[9]/3.0', 'p[10]*' + str(r48), 'p[11]*' + str(r48),
                'p[12]/3.0', 'p[13]*' + str(r48), 'p[14]*' + str(r48)]

        sp.specfit(fittype='gaussian', guesses=guesses,
                   limits=limits, limited=limited, tied=tied,
                   xmin=ha-250, xmax=sii-15)

        v = sp.specfit.parinfo.values
        errs = sp.specfit.parinfo.errors
        narrow_kms = c * abs(v[2]) / v[1]
        broad_kms = c * abs(v[5]) / v[4]
        vbroad_kms = c * abs(v[8]) / v[7]
        results.append([tid, z, v[0], errs[0], narrow_kms,
                        v[3], errs[3], broad_kms,
                        v[6], errs[6], vbroad_kms,
                        v[9], errs[9], v[12], errs[12]])

        sp.plotter.savefig("plots/halpha_triple_" + str(tid) + ".png")
        plt.close('all')
        print(n, tid, round(narrow_kms, 1), round(broad_kms, 1), round(vbroad_kms, 1))
    except Exception as e:
        failed.append(tid)
        print(n, tid, "FAILED", e)

df = pd.DataFrame(results, columns=["TARGETID", "Z",
    "ha_narrow_amp", "ha_narrow_amp_err", "ha_narrow_sigma_kms",
    "ha_broad_amp", "ha_broad_amp_err", "ha_broad_sigma_kms",
    "ha_vbroad_amp", "ha_vbroad_amp_err", "ha_vbroad_sigma_kms",
    "nii_narrow_amp", "nii_narrow_amp_err", "nii_broad_amp", "nii_broad_amp_err"])
df.to_csv("notes/2026-07-16_halpha_fits.csv", index=False)
print("fit", len(results), "skipped", len(skipped), "failed", len(failed))
print("skipped:", skipped)
print("failed:", failed)