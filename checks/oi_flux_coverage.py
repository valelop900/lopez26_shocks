import pandas as pd

m = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
m = m.merge(bpt[['TARGETID', 'bpt_class']], on='TARGETID')
m = m[m['log_L_radio'] > 24]
m = m[(m['sample'] == 'small') | (m['Physical_Size'] > 25)]
print('final sample:', len(m))

oi1 = pd.read_csv('data/VLASS3_2_OI_large.csv')[['TARGETID_1', 'OI_6300_FLUX']]
oi2 = pd.read_csv('data/VLASS3_2_OI_small.csv')[['TARGETID_1', 'OI_6300_FLUX']]
oi = pd.concat([oi1, oi2], ignore_index=True).rename(columns={'TARGETID_1': 'TARGETID'})
oi = oi.drop_duplicates('TARGETID')

t = m.merge(oi, on='TARGETID', how='left')
print('with OI flux from catalogs:', t['OI_6300_FLUX'].notna().sum())
print('missing:', t['OI_6300_FLUX'].isna().sum())
print(t[t['OI_6300_FLUX'].isna()].groupby(['sample', 'bpt_class']).size())