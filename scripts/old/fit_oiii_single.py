import numpy as np
import pandas as pd
import pyspeckit

tid = 39628016040543831   # the object we already checked

# load the spectrum
spec = pd.read_csv("/Users/valeria/Desktop/nrao_project/data/spectra/" + str(tid) + "_desispec.csv")
lam = spec["Lambda"].values
flam = spec["FLambda17"].values

# get redshift
zt = pd.read_csv("/Users/valeria/Desktop/nrao_project/notes/targetid_redshift.csv")
z = zt.loc[zt["TARGETID"] == tid, "Z"].values[0]

# where OIII 5007 lands
oiii_5007 = 5006.8 * (1 + z)

# build a pyspeckit spectrum
sp = pyspeckit.Spectrum(data=flam, xarr=lam, xarrkwargs={'unit':'Angstrom'}, unit='flux')

# zoom to the OIII window and fit one gaussian
sp.plotter(xmin=oiii_5007-60, xmax=oiii_5007+60)
sp.specfit(fittype='gaussian', guesses=[10, oiii_5007, 3.0])

amp, cen, sig = sp.specfit.parinfo.values

# convert width (sigma in Angstrom) to velocity in km/s
c = 299792.458
sigma_v = c * sig / cen
fwhm_v = 2.3548 * sigma_v

print("amplitude:", round(amp, 2))
print("center (A):", round(cen, 2))
print("sigma (A):", round(sig, 3))
print("sigma velocity (km/s):", round(sigma_v, 1))
print("FWHM velocity (km/s):", round(fwhm_v, 1))

sp.plotter.savefig("/Users/valeria/Desktop/nrao_project/plots/oiii_fit_" + str(tid) + ".png")
print("saved plot")