import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 18})

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
cat = pd.concat([c1[nev_cols], c2[nev_cols], c3[nev_cols], c4[nev_cols]],
                ignore_index=True).drop_duplicates('TARGETID')

m = w.merge(bpt[['TARGETID', 'bpt_class', 'sample']], on='TARGETID', suffixes=('_w', ''))
m = m.merge(size, on='TARGETID')
m = m[m['log_L_radio'] > 24]
m = m[(m['sample'] == 'small') | (m['Physical_Size'] > 25)]
m = m.merge(cat, on='TARGETID', how='left')
m['nev_det'] = m['NEV_3426_FLUX'] * np.sqrt(m['NEV_3426_FLUX_IVAR']) > 3

small = m[m['sample'] == 'small']
det = small[small['nev_det']]['w80']
nod = small[~small['nev_det']]['w80']
print('detected n =', len(det), 'median', round(np.median(det)))
print('undetected n =', len(nod), 'median', round(np.median(nod)))

bins = np.arange(300, 2500, 150)
plt.figure(figsize=(9, 5.5))
plt.hist(nod, bins=bins, histtype='stepfilled', facecolor='0.8',
         edgecolor='dimgray', lw=1.5, label='[NeV] not detected (n=%d)' % len(nod))
plt.hist(det, bins=bins, histtype='stepfilled', facecolor='none',
         edgecolor='#5B2C6F', hatch='\\\\\\\\', lw=1.5, label='[NeV] detected (n=%d)' % len(det))
plt.axvline(600, color='k', ls='--', lw=1.2)
plt.text(620, plt.ylim()[1]*0.9, 'shocks can make [NeV]\nabove ~600 km/s', fontsize=14)
plt.xlabel('gas speed, W80 (km/s)')
plt.ylabel('number of confined galaxies')
plt.legend()
plt.tight_layout()
plt.savefig('plots/talk_w80_nev.png', dpi=200)
print('saved plots/talk_w80_nev.png')
