import numpy as np
import pandas as pd
from astropy.cosmology import FlatLambdaCDM

cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
df = pd.read_csv("data/OI_sample_large.csv")
dl = cosmo.luminosity_distance(df["Z"]).value * 3.09e22
df["log_L_radio"] = np.log10(4*np.pi*dl**2 * df["Flux"]*1e-29 * (1+df["Z"])**(-0.3))
print(len(df), "total")
print((df["log_L_radio"] > 24).sum(), "above cut")
