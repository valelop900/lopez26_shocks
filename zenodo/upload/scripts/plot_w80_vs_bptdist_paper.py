import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

LARGE_COLOR = 'black'
SMALL_COLOR = '#5B2C6F'
LABELS = {'seyfert': 'Seyfert', 'liner': 'LINER'}

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

# perpendicular distance to Seyfert/LINER line y = 1.18x + 1.30, positive = Seyfert side
m['bpt_dist'] = (m['log_oiii_hb'] - 1.18 * m['log_oi_ha'] - 1.30) / np.sqrt(1.18**2 + 1)

print('n =', len(m))
for s in ['all', 'small', 'large']:
    sub = m if s == 'all' else m[m['sample'] == s]
    r, p = spearmanr(sub['bpt_dist'], sub['w80'])
    print('Spearman %s: r = %.3f  p = %.3f' % (s, r, p))

fig, ax = plt.subplots(figsize=(7, 5))
for s, cl, mk in [('large', 'seyfert', 'o'), ('large', 'liner', '*'),
                  ('small', 'seyfert', 'o'), ('small', 'liner', '*')]:
    sub = m[(m['sample'] == s) & (m['bpt_class'] == cl)]
    if s == 'large':
        ax.scatter(sub['bpt_dist'], sub['w80'], marker=mk, color=LARGE_COLOR,
                   s=40 if mk == 'o' else 80, label='large %s' % LABELS[cl])
    else:
        ax.scatter(sub['bpt_dist'], sub['w80'], marker=mk, facecolors='none',
                   edgecolors=SMALL_COLOR, s=40 if mk == 'o' else 80,
                   linewidths=1.3, label='small %s' % LABELS[cl])
ax.axvline(0, color='gray', ls=':', lw=1)
ax.set_xlabel('distance from Seyfert/LINER line', fontsize=14)
ax.set_ylabel(r'[O III] W80 (km s$^{-1}$)', fontsize=14)
ax.tick_params(labelsize=12)
ax.legend(fontsize=10, loc='upper left')
plt.tight_layout()
plt.savefig('plots/fig_w80_bptdist.pdf')
plt.savefig('plots/2026-08-27_w80_bptdist_v2.png', dpi=150)
print('saved plots/fig_w80_bptdist.pdf')