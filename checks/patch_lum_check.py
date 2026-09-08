import pandas as pd

lum = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
q = pd.read_csv('data/VLASS3_2_OI_large_Q.csv')[['TARGETID_1', 'logL3']].rename(columns={'TARGETID_1': 'TARGETID'})

m = lum.merge(q, on='TARGETID', how='left')
m['log_L_radio'] = m['log_L_radio'].fillna(m['logL3'])
m = m.drop(columns='logL3')
print('remaining NaN log_L_radio:', m['log_L_radio'].isna().sum())
print(m[m['TARGETID'].isin([39627818971172910, 39628398418463562])][['TARGETID', 'log_L_radio']])
m.to_csv('notes/2026-07-28_luminosity_check.csv', index=False)
print('saved')