import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp

df = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
cut = df[df['log_L_radio'] > 24]

for name, d in [('before cut', df), ('after cut', cut)]:
    lg = d[d['sample'] == 'large']['w80']
    sm = d[d['sample'] == 'small']['w80']
    print(name, ': n large', len(lg), 'n small', len(sm))
    print('   median w80 large %.1f  small %.1f' % (lg.median(), sm.median()))
    print('   KS p = %.4f' % ks_2samp(lg, sm).pvalue)
    print()

lg = cut[cut['sample'] == 'large']['w80']
sm = cut[cut['sample'] == 'small']['w80']
bins = np.linspace(0, 2200, 15)
plt.figure(figsize=(7, 5))
plt.hist(sm, bins=bins, alpha=0.6, label='small (10-15 kpc), n=%d' % len(sm))
plt.hist(lg, bins=bins, alpha=0.6, label='large (>20 kpc), n=%d' % len(lg))
plt.axvline(sm.median(), ls='--')
plt.axvline(lg.median(), ls='--', color='C1')
plt.xlabel('W80 (km/s)')
plt.ylabel('number of objects')
plt.legend()
plt.tight_layout()
plt.savefig('plots/2026-07-29_w80_by_sample_cut24.png', dpi=150)
