import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

LARGE_COLOR = 'black'
SMALL_COLOR = '#5B2C6F'

w1 = pd.read_csv('notes/2026-07-13_resolution_w80.csv')
w2 = pd.read_csv('notes/2026-07-22_w80_new_large.csv')
w3 = pd.read_csv('notes/2026-07-31_w80_new_small24.csv')
w = pd.concat([w1, w2, w3], ignore_index=True)

bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
size = pd.read_csv('notes/2026-07-28_luminosity_check.csv')[['TARGETID', 'Physical_Size', 'log_L_radio']]

m = w.merge(bpt, on='TARGETID', suffixes=('_w', ''))
m = m.merge(size, on='TARGETID')
m = m[m['log_L_radio'] > 24]
m = m[(m['sample'] == 'small') | (m['Physical_Size'] > 25)]

# perpendicular distance to the Seyfert/LINER line y = 1.18x + 1.30, positive = Seyfert side
m['bpt_dist'] = (m['log_oiii_hb'] - 1.18 * m['log_oi_ha'] - 1.30) / np.sqrt(1.18**2 + 1)

print('n =', len(m))
r, p = spearmanr(m['bpt_dist'], m['w80'])
print('Spearman all: r =', round(r, 3), 'p =', round(p, 4))
for s in ['small', 'large']:
    sub = m[m['sample'] == s]
    r, p = spearmanr(sub['bpt_dist'], sub['w80'])
    print('Spearman', s, ': r =', round(r, 3), 'p =', round(p, 4))

plt.figure(figsize=(7, 6))
for s, cl, mk in [('large', 'seyfert', 'o'), ('large', 'liner', '*'),
                  ('small', 'seyfert', 'o'), ('small', 'liner', '*')]:
    sub = m[(m['sample'] == s) & (m['bpt_class'] == cl)]
    if s == 'large':
        plt.scatter(sub['bpt_dist'], sub['w80'], marker=mk, color=LARGE_COLOR,
                    s=60 if mk == 'o' else 110, label='large %s' % cl)
    else:
        plt.scatter(sub['bpt_dist'], sub['w80'], marker=mk, facecolors='none',
                    edgecolors=SMALL_COLOR, s=60 if mk == 'o' else 110,
                    linewidths=1.5, label='small %s' % cl)
plt.axvline(0, color='gray', ls=':', lw=1)
plt.xlabel('distance from Seyfert-LINER line')
plt.ylabel('[OIII] W80 (km/s)')
plt.legend()
plt.tight_layout()
plt.savefig('plots/2026-08-20_w80_vs_bptdist.png', dpi=150)
print('saved plots/2026-08-20_w80_vs_bptdist.png')