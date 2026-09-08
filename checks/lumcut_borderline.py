import pandas as pd

bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
lum = pd.read_csv('notes/2026-07-28_luminosity_check.csv')[['TARGETID', 'log_L_radio', 'Physical_Size']]
m = bpt.merge(lum, on='TARGETID', how='left')

print('in lumcut_v2 but log_L_radio <= 24 in luminosity_check:')
bad = m[m['log_L_radio'] <= 24]
print(bad[['TARGETID', 'sample', 'bpt_class', 'log_L_radio', 'Physical_Size']])
print()
print('in lumcut_v2 but missing from luminosity_check:')
print(m[m['log_L_radio'].isna()][['TARGETID', 'sample', 'bpt_class']])