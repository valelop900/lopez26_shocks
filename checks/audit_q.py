import numpy as np
import pandas as pd

lum = pd.read_csv('notes/2026-07-28_luminosity_check.csv').drop_duplicates('TARGETID')
final = lum[lum['log_L_radio'] > 24]
is_large = final['sample'] == 'large'
final = final[(~is_large) | (final['Physical_Size'] > 25)]

for path in ['data/VLASS3_2_OI_small_Q.csv', 'data/VLASS3_2_OI_large_Q.csv']:
    q = pd.read_csv(path).rename(columns={'TARGETID_1': 'TARGETID'})
    q = q.drop_duplicates('TARGETID')
    in_final = q[q['TARGETID'].isin(final['TARGETID'])]
    print(path)
    print('  all rows: n=%d, median logQ = %.2f' % (len(q), q['logQ'].median()))
    print('  final-sample only: n=%d, median logQ = %.2f' % (len(in_final), in_final['logQ'].median()))