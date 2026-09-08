import pandas as pd

small = pd.read_csv('data/OI_sample_small.csv')
large = pd.read_csv('data/OI_sample_large.csv')
csv_ids = set(small['TARGETID']) | set(large['TARGETID'])

m = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
m = m[m['log_L_radio'] > 24]
m = m[(m['sample'] == 'small') | (m['Physical_Size'] > 25)]

print('final sample size:', len(m))
print('small:', (m['sample'] == 'small').sum(), 'large:', (m['sample'] == 'large').sum())
print('in luminosity file but missing from the two CSVs:', len(set(m['TARGETID']) - csv_ids))