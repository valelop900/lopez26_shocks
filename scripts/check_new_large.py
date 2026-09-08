import pandas as pd

new = pd.read_csv('data/VLASS3_2_OI_large.csv')
w80 = pd.read_csv('notes/2026-07-13_resolution_w80.csv')

lg = w80[w80['sample'] == 'large']
print(len(new), 'objects in new file')
print(len(lg), 'large objects with W80')

missing = set(lg['TARGETID']) - set(new['TARGETID_1'])
print('missing from new file:', missing)
