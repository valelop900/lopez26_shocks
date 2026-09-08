import numpy as np
import pandas as pd
from astropy.cosmology import FlatLambdaCDM

cosmo = FlatLambdaCDM(H0=70, Om0=0.3)

df = pd.read_csv("data/VLASS3_2_OI_small.csv")

dl = cosmo.luminosity_distance(df["Z"]).value * 3.09e22   # Mpc to m
L = 4*np.pi*dl**2 * df["Flux"]*1e-29 * (1+df["Z"])**(-0.3)
df["log_L_radio"] = np.log10(L)

out = df[["Name", "TARGETID_1", "Z", "Flux", "Physical_size", "log_L_radio"]]
out.to_csv("notes/2026-07-31_luminosity_small_new.csv", index=False)

print(len(out), "objects")
print(out["log_L_radio"].round(2).describe())
print((out["log_L_radio"] > 24).sum(), "above log L = 24")
