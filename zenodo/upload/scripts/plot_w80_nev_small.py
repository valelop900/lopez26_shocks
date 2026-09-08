import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

DET_COLOR = 'black'
NONDET_COLOR = '#5B2C6F'

w1 = pd.read_csv('notes/2026-07-13_resolution_w80.csv')
w2 = pd.read_csv('notes/2026-07-22_w80_new_large.csv')
w3 = pd.read_csv('notes/2026-07-31_w80_new_small24.csv')
w = pd.concat([w1, w2, w3], ignore_index=True)

bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
lum = pd.read_csv('notes/2026-07-28_luminosity_check.csv')[['TARGETID', 'Physical_Size', 'log_L_radio']]

c1 = pd.read_csv('data/OI_sample_small.csv')
c2 = pd.read_csv('data/OI_sample_large.csv')
c3 = pd.read_csv('data/VLASS3_2_OI_small.csv').rename(columns={'TARGETID_1': 'TARGETID'})
c4 = pd.read_csv('data/VLASS3_2_OI_large.csv').rename(columns={'TARGETID_1': 'TARGETID'})
cat = pd.concat([c1, c2, c3, c4], ignore_index=True).drop_duplicates('TARGETID')

m = w.merge(bpt[['TARGETID', 'bpt_class', 'sample']], on='TARGETID', suffixes=('_w', ''))
m = m.merge(lum, on='TARGETID')
m = m.merge(cat[['TARGETID', 'NEV_3426_FLUX', 'NEV_3426_FLUX_IVAR']], on='TARGETID')
m = m[m['log_L_radio'] > 24]
m = m[(m['sample'] == 'small') | (m['Physical_Size'] > 25)]

m['nev_det'] = m['NEV_3426_FLUX'] * np.sqrt(m['NEV_3426_FLUX_IVAR']) > 3

sm = m[m['sample'] == 'small']
det = sm[sm['nev_det']]['w80']
non = sm[~sm['nev_det']]['w80']

print('small sample: NeV detected n=%d, not detected n=%d' % (len(det), len(non)))
print('median W80: detected %.1f, not detected %.1f' % (det.median(), non.median()))
print('MW p =', round(mannwhitneyu(det, non).pvalue, 4))
print('fraction above 600 km/s: detected %.2f, not detected %.2f'
      % ((det > 600).mean(), (non > 600).mean()))

# same check on the large sample for comparison
lg = m[m['sample'] == 'large']
ldet = lg[lg['nev_det']]['w80']
lnon = lg[~lg['nev_det']]['w80']
print()
print('large sample: detected n=%d median %.1f, not detected n=%d median %.1f'
      % (len(ldet), ldet.median(), len(lnon), lnon.median()))
if len(ldet) > 3 and len(lnon) > 3:
    print('MW p =', round(mannwhitneyu(ldet, lnon).pvalue, 4))

bins = np.arange(200, 1800, 125)
plt.figure(figsize=(7, 5))
plt.hist(det, bins=bins, weights=np.ones(len(det))/len(det), color=DET_COLOR,
         alpha=0.7, label='[NeV] detected, n=%d' % len(det))
plt.hist(non, bins=bins, weights=np.ones(len(non))/len(non), histtype='step',
         color=NONDET_COLOR, linewidth=1.8, label='[NeV] not detected, n=%d' % len(non))
plt.axvline(600, color='k', ls='--', lw=0.8)
plt.xlabel('W80 (km/s)')
plt.ylabel('fraction')
plt.title('Small sample: W80 by [NeV] detection')
plt.legend(fontsize=9)
plt.tight_layout()
plt.savefig('plots/2026-08-19_w80_nev_small.png', dpi=150)
plt.savefig('plots/fig_w80_nev_small.pdf')
print('saved')