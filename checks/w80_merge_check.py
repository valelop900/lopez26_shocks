import pandas as pd

old = pd.read_csv('notes/2026-07-13_resolution_w80.csv')
new = pd.read_csv('notes/2026-07-22_w80_new_large.csv')
w = pd.concat([old, new], ignore_index=True)
print('w80 rows:', len(w))

bpt22 = pd.read_csv('notes/2026-07-22_bpt_class_expanded.csv')
bpt31 = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
lum = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
print('bpt 07-22 rows:', len(bpt22))
print('bpt 07-31 lumcut_v2 rows:', len(bpt31))
print('lum rows:', len(lum))

m1 = w.merge(bpt22[['TARGETID', 'bpt_class']], on='TARGETID')
print('after merge with bpt 07-22:', len(m1))
m2 = m1.merge(lum[['TARGETID', 'log_L_radio']], on='TARGETID')
print('after merge with lum:', len(m2))
print('lost in lum merge:', len(m1) - len(m2))

m3 = w.merge(bpt31, on='TARGETID')
print('after merge with bpt 07-31 lumcut_v2:', len(m3))
print(m3.groupby(['sample', 'bpt_class']).size() if 'sample' in m3.columns else bpt31.columns.tolist())