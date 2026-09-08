import numpy as np
import pandas as pd
from astropy.cosmology import FlatLambdaCDM

cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
old = pd.read_csv("data/OI_sample_small.csv")
dl = cosmo.luminosity_distance(old["Z"]).value * 3.09e22
old["log_L_radio"] = np.log10(4*np.pi*dl**2 * old["Flux"]*1e-29 * (1+old["Z"])**(-0.3))
print(len(old), "total")
print((old["log_L_radio"] > 24).sum(), "above cut")
