import pandas as pd

new = pd.read_csv('data/VLASS3_2_OI_large.csv')

qc = new[['TARGETID_1', 'RA_1', 'DEC_1', 'Z', 'LAS', 'Physical_size', 'Type']].copy()
qc.columns = ['TARGETID', 'RA', 'DEC', 'Z', 'LAS', 'Physical_size', 'Type']
qc['verdict'] = ''
qc.to_csv('data/QC_new_large.csv', index=False)
print(len(qc), 'rows written to data/QC_new_large.csv')
