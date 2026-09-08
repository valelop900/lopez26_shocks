import pandas as pd
from scipy.stats import ks_2samp

old = pd.read_csv('notes/2026-07-13_resolution_w80.csv')
new = pd.read_csv('notes/2026-07-22_w80_new_large.csv')
w = pd.concat([old, new], ignore_index=True)

bpt = pd.read_csv('notes/2026-07-22_bpt_class_expanded.csv')
m = w.merge(bpt[['TARGETID', 'bpt_class']], on='TARGETID')

# seyferts only: does the large vs small width difference survive
sy = m[m['bpt_class'] == 'seyfert']
lg = sy[sy['sample'] == 'large']['w80']
sm = sy[sy['sample'] == 'small']['w80']
print('seyferts only: large n =', len(lg), 'small n =', len(sm))
print('median W80 large seyferts:', round(lg.median(), 1))
print('median W80 small seyferts:', round(sm.median(), 1))
print('KS p =', round(ks_2samp(lg, sm).pvalue, 4))

# seyfert vs liner within the small sample
small = m[m['sample'] == 'small']
s_sy = small[small['bpt_class'] == 'seyfert']['w80']
s_li = small[small['bpt_class'] == 'liner']['w80']
print()
print('small sample: seyfert n =', len(s_sy), 'liner n =', len(s_li))
print('median W80 small seyferts:', round(s_sy.median(), 1))
print('median W80 small liners:', round(s_li.median(), 1))
print('KS p =', round(ks_2samp(s_sy, s_li).pvalue, 4))
