import pandas as pd
import numpy as np

m = pd.read_csv('notes/2026-07-13_resolution_w80.csv')
m['broad_det'] = m['oiii_broad_amp'] > 3 * m['oiii_broad_amp_err']

# detection rate in bins of catalog SNR
bins = [0, 25, 50, 100, 250]
m['snr_bin'] = pd.cut(m['snr'], bins)
print('broad detection rate by SNR bin:')
print(m.groupby(['snr_bin', 'sample'], observed=True)['broad_det'].agg(['size', 'mean']))
print()

# what would the large sample look like at the small sample's noise level
target = m[m['sample'] == 'small']['snr'].median()
lg = m[m['sample'] == 'large'].copy()
lg['err_scaled'] = lg['oiii_broad_amp_err'] * (lg['snr'] / target)
lg['det_scaled'] = lg['oiii_broad_amp'] > 3 * lg['err_scaled']
print('target snr', round(target, 1))
print('large detection rate as observed', round(lg['broad_det'].mean(), 3))
print('large detection rate at small-sample noise', round(lg['det_scaled'].mean(), 3))
print('small detection rate observed', round(m[m['sample'] == 'small']['broad_det'].mean(), 3))