import pandas as pd
import matplotlib.pyplot as plt

tid = 39628016040543831   # object 

spec = pd.read_csv("/Users/valeria/Desktop/nrao_project/data/spectra/" + str(tid) + "_desispec.csv")
zt = pd.read_csv("/Users/valeria/Desktop/nrao_project/notes/targetid_redshift.csv")
z = zt.loc[zt["TARGETID"] == tid, "Z"].values[0]

# rest wavelengths
oiii_4959 = 4958.9 * (1 + z)
oiii_5007 = 5006.8 * (1 + z)
oi_6300 = 6300.3 * (1 + z)

plt.figure(figsize=(14, 5))
plt.plot(spec["Lambda"], spec["FLambda17"], color="maroon", lw=0.7)
plt.axvline(oiii_4959, color="blue", ls="--")
plt.axvline(oiii_5007, color="green", ls="--")
plt.axvline(oi_6300, color="orange", ls="--")
plt.xlabel("observed wavelength (Angstrom)")
plt.ylabel("flux")
plt.title("z = " + str(round(z, 4)) + "   OIII green, OI orange")
plt.show()