import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp, mannwhitneyu, anderson_ksamp

LARGE_COLOR = 'black'
SMALL_COLOR = '#5B2C6F'

b = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
lum = pd.read_csv('notes/2026-07-28_luminosity_check.csv')[['TARGETID', 'Physical_Size', 'log_L_radio']]
df = b.merge(lum, on='TARGETID')

df = df[df['log_L_radio'] > 24]
df = df[(df['sample'] == 'small') | (df['Physical_Size'] > 25)]

# perpendicular distance to Seyfert/LINER line y = 1.18x + 1.30
# positive = Seyfert side
m, c = 1.18, 1.30
df['d'] = (df['log_oiii_hb'] - m*df['log_oi_ha'] - c) * np.cos(np.arctan(m))

lg = df[df['sample'] == 'large']['d']
sm = df[df['sample'] == 'small']['d']

print('n large %d  small %d' % (len(lg), len(sm)))
print('median d large %.3f  small %.3f' % (lg.median(), sm.median()))
print('KS p = %.4f' % ks_2samp(lg, sm).pvalue)
print('MW p = %.4f' % mannwhitneyu(lg, sm).pvalue)
print('AD p = %.4f' % anderson_ksamp([lg.values, sm.values], variant='midrank').pvalue)

bins = np.arange(-1.0, 1.4, 0.15)
plt.figure(figsize=(7, 5))
plt.hist(lg, bins=bins, weights=np.ones(len(lg))/len(lg), histtype='step',
         hatch='///', edgecolor=LARGE_COLOR, linewidth=1.4,
         label='large (>25 kpc), n=%d' % len(lg))
plt.hist(sm, bins=bins, weights=np.ones(len(sm))/len(sm), histtype='step',
         hatch='\\\\\\', edgecolor=SMALL_COLOR, linewidth=1.4,
         label='small (10-15 kpc), n=%d' % len(sm))
plt.axvline(0, color='k', ls='--')
plt.xlabel('distance from Seyfert/LINER line')
plt.ylabel('fraction of sample')
plt.legend()
plt.tight_layout()
plt.savefig('plots/fig_bpt_distance.pdf')
plt.savefig('plots/2026-08-21_bpt_distance.png', dpi=150)
print('saved plots/fig_bpt_distance.pdf')