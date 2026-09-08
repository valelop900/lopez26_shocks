import pandas as pd

old_small = pd.read_csv('data/OI_sample_small.csv')
new_small = pd.read_csv('data/VLASS3_2_OI_small.csv').rename(columns={'TARGETID_1': 'TARGETID'})

overlap = set(old_small['TARGETID']) & set(new_small['TARGETID'])
print('overlap with existing small sample:', len(overlap))
print('new file row count:', len(new_small))
