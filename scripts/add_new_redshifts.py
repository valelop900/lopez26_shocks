import pandas as pd

zt = pd.read_csv('notes/targetid_redshift.csv')
new = pd.read_csv('data/VLASS3_2_OI_large.csv')

add = new[['TARGETID_1', 'Z']].copy()
add.columns = ['TARGETID', 'Z']

overlap = set(add['TARGETID']) & set(zt['TARGETID'])
print('already in lookup:', len(overlap))

zt = pd.concat([zt, add], ignore_index=True)
zt.to_csv('notes/targetid_redshift.csv', index=False)
print(len(zt), 'rows in lookup now')
