import pandas as pd

orig = pd.read_csv('notes/2026-07-09_oi_fits.csv')
new_large = pd.read_csv('notes/2026-07-22_oi_fits_new_large.csv')
new_small = pd.read_csv('notes/2026-07-31_oi_fits_new_small24.csv')

overlap_large = set(orig['TARGETID']) & set(new_large['TARGETID'])
overlap_small = set(orig['TARGETID']) & set(new_small['TARGETID'])

print('overlap with new_large:', len(overlap_large))
print('overlap with new_small24:', len(overlap_small))