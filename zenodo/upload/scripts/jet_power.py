import numpy as np
import pandas as pd

# Willott et al. 1999, Q = 3e38 (L151/1e28)^(6/7) W
# I go from 3 GHz to 151 MHz with alpha = -0.7 and use the catalog Alpha only for the K-correction

mpc_to_m = 3.086e22
mjy_to_si = 1e-29   # W/m^2/Hz
alpha_151 = -0.7

for name in ['large', 'small']:
    df = pd.read_csv('data/catalog_%s.csv' % name)
    S = df['Flux'] * mjy_to_si
    dL = df['D_L'] * mpc_to_m
    alpha = df['Alpha'].fillna(-0.7)
    L3 = 4*np.pi * dL**2 * S * (1+df['Z'])**(-1-alpha)   # W/Hz at rest 3 GHz
    L151 = L3 * (151/3000.)**alpha_151
    L151_sr = L151 / (4*np.pi)
    Q = 3e38 * (L151_sr / 1e28)**(6./7)
    df['logL3'] = np.log10(L3)
    df['logQ'] = np.log10(Q)
    df[['TARGETID', 'logL3', 'logQ']].to_csv('data/catalog_%s_Q.csv' % name, index=False)
    print(name, len(df), round(df['logL3'].median(), 2), round(df['logQ'].median(), 2))