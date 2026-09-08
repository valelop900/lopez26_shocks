import pandas as pd

ids = [39627818971172910, 39628398418463562]

lum = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
print(lum[lum['TARGETID'].isin(ids)])
print()

q = pd.read_csv('data/VLASS3_2_OI_large_Q.csv')
hit = q[q['TARGETID_1'].isin(ids)]
print(hit[['TARGETID_1', 'Flux', 'D_L', 'Z', 'Physical_size', 'logL3']] if len(hit) else 'not in new large catalog')