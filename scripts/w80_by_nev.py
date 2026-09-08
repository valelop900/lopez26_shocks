import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

w1 = pd.read_csv('notes/2026-07-13_resolution_w80.csv')
w2 = pd.read_csv('notes/2026-07-22_w80_new_large.csv')
w3 = pd.read_csv('notes/2026-07-31_w80_new_small24.csv')
w = pd.concat([w1, w2, w3], ignore_index=True)

bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
size = pd.read_csv('notes/2026-07-28_luminosity_check.csv')[['TARGETID', 'Physical_Size', 'log_L_radio']]

c1 = pd.read_csv('data/OI_sample_large.csv')
c2 = pd.read_csv('data/OI_sample_small.csv')
c3 = pd.read_csv('data/VLASS3_2_OI_large.csv').rename(columns={'TARGETID_1': 'TARGETID'})
c4 = pd.read_csv('data/VLASS3_2_OI_small.csv').rename(columns={'TARGETID_1': 'TARGETID'})
nev_cols = ['TARGETID', 'NEV_3426_FLUX', 'NEV_3426_FLUX_IVAR']
cat = pd.concat([c1[nev_cols], c2[nev_cols], c3[nev_cols], c4[nev_cols]], ignore_index=True)
cat = cat.drop_duplicates('TARGETID')

m = w.merge(bpt[['TARGETID', 'bpt_class', 'sample']], on='TARGETID', suffixes=('_w', ''))
m = m.merge(size, on='TARGETID')
m = m[m['log_L_radio'] > 24]
m = m[(m['sample'] == 'small') | (m['Physical_Size'] > 25)]
m = m.merge(cat, on='TARGETID', how='left')
print('with NeV column:', m['NEV_3426_FLUX'].notna().sum(), 'of', len(m))

m['nev_snr'] = m['NEV_3426_FLUX'] * np.sqrt(m['NEV_3426_FLUX_IVAR'])
m['nev_det'] = m['nev_snr'] > 3

for s in ['small', 'large']:
    sub = m[m['sample'] == s]
    a = sub[sub['nev_det']]['w80']
    b = sub[~sub['nev_det']]['w80']
    print(s, 'NeV det n =', len(a), 'median W80 =', round(np.median(a)))
    print(s, 'NeV nondet n =', len(b), 'median W80 =', round(np.median(b)))
    print(s, 'MW p =', round(mannwhitneyu(a, b).pvalue, 4))
    print()

small = m[m['sample'] == 'small']
bins = np.arange(300, 2500, 150)
plt.figure(figsize=(7, 5))
plt.hist(small[~small['nev_det']]['w80'], bins=bins, histtype='step', lw=1.8,
         color='black', label='[NeV] undetected')
plt.hist(small[small['nev_det']]['w80'], bins=bins, histtype='step', lw=1.8,
         color='#5B2C6F', label='[NeV] detected')
plt.xlabel('[OIII] W80 (km/s)')
plt.ylabel('N')
plt.legend()
plt.tight_layout()
plt.savefig('plots/2026-08-20_w80_by_nev_small.png', dpi=150)
print('saved plots/2026-08-20_w80_by_nev_small.png')