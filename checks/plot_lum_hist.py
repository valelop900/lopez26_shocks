import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
df = df.replace([np.inf, -np.inf], np.nan)

lg = df[df['sample'] == 'large']
sm = df[df['sample'] == 'small']

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
for a, c, lab in zip(ax, ['log_L_radio', 'log_L_oiii'],
                     ['log L(1.4 GHz) [W/Hz]', 'log L([OIII]) [erg/s]']):
    bins = np.linspace(df[c].min(), df[c].max(), 16)
    a.hist(lg[c].dropna(), bins=bins, alpha=0.5, label='large (>20 kpc)')
    a.hist(sm[c].dropna(), bins=bins, alpha=0.5, label='small (10-15 kpc)')
    a.axvline(lg[c].median(), ls='--')
    a.axvline(sm[c].median(), ls='--', color='C1')
    a.set_xlabel(lab)
    a.set_ylabel('N')
    a.legend()
plt.tight_layout()
plt.savefig('plots/2026-07-28_luminosity_hist.png', dpi=150)
