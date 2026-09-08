import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import matplotlib.pyplot as plt

large_old = pd.read_csv('data/OI_sample_large.csv')
small = pd.read_csv('data/OI_sample_small.csv')
large_new = pd.read_csv('data/VLASS3_2_OI_large.csv')
large_new = large_new.rename(columns={'TARGETID_1': 'TARGETID', 'Physical_size': 'Physical_Size'})
small_new = pd.read_csv('data/VLASS3_2_OI_small.csv')
small_new = small_new.rename(columns={'TARGETID_1': 'TARGETID', 'Physical_size': 'Physical_Size'})

cols = ['TARGETID', 'Z', 'Flux', 'Alpha', 'D_L', 'OIII_5007_FLUX', 'Physical_Size']
cat = pd.concat([large_old[cols], large_new[cols], small[cols], small_new[cols]], ignore_index=True)

for c in ['Z', 'Flux', 'Alpha', 'D_L', 'OIII_5007_FLUX', 'Physical_Size']:
    print(c, round(cat[c].min(), 4), round(cat[c].median(), 4), round(cat[c].max(), 4))
print()

dl_m = cat['D_L'] * 3.086e22
dl_cm = cat['D_L'] * 3.086e24
kcorr = (1 + cat['Z']) ** (-(1 + cat['Alpha']))
cat['log_L_radio'] = np.log10(4 * np.pi * dl_m**2 * cat['Flux'] * 1e-29 * kcorr)
cat['log_L_oiii'] = np.log10(4 * np.pi * dl_cm**2 * cat['OIII_5007_FLUX'] * 1e-17)

w1 = pd.read_csv('notes/2026-07-13_resolution_w80.csv')
w2 = pd.read_csv('notes/2026-07-22_w80_new_large.csv')
w3 = pd.read_csv('notes/2026-07-31_w80_new_small24.csv')
w80 = pd.concat([w1[['TARGETID', 'sample', 'w80']], w2[['TARGETID', 'sample', 'w80']], w3[['TARGETID', 'sample', 'w80']]], ignore_index=True)

df = w80.merge(cat, on='TARGETID', how='inner')
print('merged', len(df))
print(df['sample'].value_counts())
print()

lg = df[df['sample'] == 'large']
sm = df[df['sample'] == 'small']

for c in ['log_L_radio', 'log_L_oiii', 'w80']:
    print(c, 'large', round(lg[c].median(), 3), 'small', round(sm[c].median(), 3),
          'KS p', round(ks_2samp(lg[c].dropna(), sm[c].dropna()).pvalue, 4))
print()

for name, s in [('large', lg), ('small', sm)]:
    for c in ['log_L_radio', 'log_L_oiii']:
        s2 = s[[c, 'w80']].dropna()
        print(name, c, 'corr', round(np.corrcoef(s2[c], s2['w80'])[0, 1], 3))

df.to_csv('notes/2026-07-28_luminosity_check.csv', index=False)

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
for a, c in zip(ax, ['log_L_radio', 'log_L_oiii']):
    a.scatter(lg[c], lg['w80'], label='large', alpha=0.7)
    a.scatter(sm[c], sm['w80'], label='small', alpha=0.7)
    a.set_xlabel(c)
    a.set_ylabel('W80 (km/s)')
    a.legend()
plt.tight_layout()
plt.savefig('plots/2026-07-28_w80_vs_luminosity.png', dpi=150)
