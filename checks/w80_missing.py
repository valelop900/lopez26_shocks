import pandas as pd

old = pd.read_csv('notes/2026-07-13_resolution_w80.csv')
new = pd.read_csv('notes/2026-07-22_w80_new_large.csv')
w = pd.concat([old, new], ignore_index=True)

bpt31 = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
missing = bpt31[~bpt31['TARGETID'].isin(w['TARGETID'])]
print(missing.groupby(['sample', 'bpt_class']).size())