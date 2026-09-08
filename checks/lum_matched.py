import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

df = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
df = df[np.isfinite(df['log_L_oiii'])]

lg = df[df['sample'] == 'large']
sm = df[df['sample'] == 'small']
print('after dropping bad OIII:', len(lg), 'large', len(sm), 'small')
print()

for c in ['log_L_radio', 'log_L_oiii']:
    lo = max(lg[c].min(), sm[c].min())
    hi = min(lg[c].max(), sm[c].max())
    m = df[(df[c] >= lo) & (df[c] <= hi)]
    ml = m[m['sample'] == 'large']
    ms = m[m['sample'] == 'small']
    print(c, 'overlap', round(lo, 2), 'to', round(hi, 2))
    print('  n', len(ml), 'large', len(ms), 'small')
    print('  median lum', round(ml[c].median(), 3), round(ms[c].median(), 3),
          'KS p', round(ks_2samp(ml[c], ms[c]).pvalue, 4))
    print('  median w80', round(ml['w80'].median(), 1), round(ms['w80'].median(), 1),
          'KS p', round(ks_2samp(ml['w80'], ms['w80']).pvalue, 4))
    print()

print('sizes: large', round(lg['Physical_Size'].min(), 1), 'to', round(lg['Physical_Size'].max(), 1))
print('sizes: small', round(sm['Physical_Size'].min(), 1), 'to', round(sm['Physical_Size'].max(), 1))
print()
print('zero OIII objects:')
print(pd.read_csv('notes/2026-07-28_luminosity_check.csv').query('OIII_5007_FLUX == 0')[['TARGETID', 'sample']])
