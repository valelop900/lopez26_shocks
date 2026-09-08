import pandas as pd

new = pd.read_csv('data/VLASS3_2_OI_large.csv')
ids = new['TARGETID_1']
ids.to_csv('notes/2026-07-22_new_large_targetids.txt', index=False, header=False)
print(len(ids), 'ids saved')
