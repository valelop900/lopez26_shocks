import pandas as pd
import numpy as np

old_small = pd.read_csv('data/OI_sample_small.csv')
new_small = pd.read_csv('data/VLASS3_2_OI_small.csv').rename(columns={'TARGETID_1': 'TARGETID'})

ra1, dec1 = np.radians(old_small['RA']), np.radians(old_small['DEC'])
ra2, dec2 = np.radians(new_small['RA_1']), np.radians(new_small['DEC_1'])

min_seps = []
for r2, d2 in zip(ra2, dec2):
    sep = np.arccos(np.clip(
        np.sin(d2)*np.sin(dec1) + np.cos(d2)*np.cos(dec1)*np.cos(ra1 - r2), -1, 1))
    min_seps.append(np.degrees(sep.min()))

print('closest match for each new object (degrees), min/median/max:')
print(min(min_seps), np.median(min_seps), max(min_seps))
