import numpy as np
import pandas as pd
import pyspeckit

tid = 39628016040543831

spec = pd.read_csv("data/spectra/" + str(tid) + "_desispec.csv")
lam = spec["Lambda"].values
flam = spec["FLambda17"].values

zt = pd.read_csv("notes/targetid_redshift.csv")
z = zt.loc[zt["TARGETID"] == tid, "Z"].values[0]
oiii = 5006.8 * (1 + z)

sp = pyspeckit.Spectrum(data=flam, xarr=lam, xarrkwargs={'unit':'Angstrom'})
sp.plotter(xmin=oiii-80, xmax=oiii+80)

# fit and subtract the continuum first, excluding the line region
sp.baseline(xmin=oiii-80, xmax=oiii+80, exclude=[oiii-25, oiii+25], subtract=True, order=1)

# narrow + broad gaussian on the continuum-subtracted line
guesses = [10, oiii, 2.5, 4, oiii, 10.0]
limits = [(0, 0), (oiii-10, oiii+10), (0.5, 6.0),
          (0, 0), (oiii-5, oiii+5), (3.0, 30.0)]
limited = [(True, False), (True, True), (True, True),
           (True, False), (True, True), (True, True)]

sp.specfit(fittype='gaussian', guesses=guesses, limits=limits, limited=limited)

vals = sp.specfit.parinfo.values
c = 299792.458
for k in range(0, len(vals), 3):
    cen = vals[k+1]
    sig = vals[k+2]
    print(vals[k], cen, c*abs(sig)/cen)

sp.plotter.savefig("plots/oiii_double_" + str(tid) + ".png")