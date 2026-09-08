import numpy as np
import pandas as pd
from astropy.cosmology import FlatLambdaCDM

cosmo = FlatLambdaCDM(H0=70, Om0=0.3)

df = pd.read_csv("data/VLASS3_2_OI_small.csv")
dl = cosmo.luminosity_distance(df["Z"]).value * 3.09e22
df["log_L_radio"] = np.log10(4*np.pi*dl**2 * df["Flux"]*1e-29 * (1+df["Z"])**(-0.3))

cut = df[df["log_L_radio"] > 24]
print(len(cut), "above cut")

bad = ["J161611.48", "J130749.00", "J072012.49"]
for b in bad:
    hit = cut[cut["Name"].str.contains(b)]
    print(b, "in cut:", len(hit) > 0)

cut.to_csv("data/small_new_cut27.csv", index=False)

clean = cut[~cut["Name"].str.contains("|".join(bad))]
clean.to_csv("data/small_new_cut24.csv", index=False)
print(len(clean), "clean")

old = pd.read_csv("data/OI_sample_small.csv")
oldid = set(old["TARGETID"])
print(len(set(clean["TARGETID_1"]) & oldid), "overlap with existing small sample")
print(len(oldid), "in existing small sample")
