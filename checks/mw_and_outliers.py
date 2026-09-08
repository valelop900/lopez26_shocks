import pandas as pd
from scipy.stats import mannwhitneyu, ks_2samp

df = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
cut = df[df['log_L_radio'] > 24]

lg = cut[cut['sample'] == 'large']
sm = cut[cut['sample'] == 'small']

print('KS p = %.4f' % ks_2samp(lg['w80'], sm['w80']).pvalue)
print('MW p = %.4f' % mannwhitneyu(lg['w80'], sm['w80']).pvalue)
print()

broad = lg[lg['w80'] > 900].sort_values('w80', ascending=False)
print('large sources with w80 > 900:')
print(broad[['TARGETID', 'w80', 'Physical_Size', 'log_L_radio']].to_string(index=False))
print()
print('median size of broad large: %.1f kpc' % broad['Physical_Size'].median())
print('median size of all large:   %.1f kpc' % lg['Physical_Size'].median())

for c in [25, 30]:
    lg2 = lg[lg['Physical_Size'] > c]
    print('size cut %d kpc: n large %d, MW p = %.4f' % (c, len(lg2), mannwhitneyu(lg2['w80'], sm['w80']).pvalue))
