import pandas as pd

df = pd.read_csv('notes/2026-07-29_bpt_class_lumcut.csv')
sf = df[(df['sample'] == 'small') & (df['bpt_class'] == 'sf')]
print(sf[['TARGETID', 'log_oi_ha', 'log_oiii_hb']])
