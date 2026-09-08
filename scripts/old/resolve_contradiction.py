import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

c = 299792.458

fits = pd.read_csv('notes/2026-07-08_oiii_fits.csv')
avg = pd.read_csv('notes/2026-07-13_fwhm_avg.csv')
large = pd.read_csv('data/OI_sample_large.csv')
small = pd.read_csv('data/OI_sample_small.csv')

# drop the two excluded objects
bad = [39627802344950353, 39627701220278777]
fits = fits[~fits['TARGETID'].isin(bad)]

large_ids = set(large['TARGETID'])
fits['sample'] = ['large' if t in large_ids else 'small' for t in fits['TARGETID']]

# step 0: recompute the disputed numbers straight from the files
print('n per sample:')
print(fits.groupby('sample').size())
print('median narrow sigma km/s:')
print(fits.groupby('sample')['oiii_narrow_sigma_kms'].median())
print('median broad sigma km/s:')
print(fits.groupby('sample')['oiii_broad_sigma_kms'].median())

good = [int(x) for x in open('notes/2026-07-07_good_targetids.txt')]
cat = pd.concat([large.assign(sample='large'), small.assign(sample='small')])
cat = cat[cat['TARGETID'].isin(good)]
cat['snr'] = cat['OIII_5007_FLUX'] * np.sqrt(cat['OIII_5007_FLUX_IVAR'])
print('catalog median OIII sigma:')
print(cat.groupby('sample')['OIII_5007_SIGMA'].median())
print('catalog median OIII SNR:')
print(cat.groupby('sample')['snr'].median())

if 'Z' in fits.columns:
    m = fits.copy()
else:
    m = fits.merge(avg[['TARGETID', 'Z']], on='TARGETID')
m['lam_obs'] = 5006.84 * (1 + m['Z'])
m['R'] = np.interp(m['lam_obs'], [5760, 7620], [3200, 4100])
m['sig_inst'] = c / (m['R'] * 2.3548)
m['narrow_corr'] = np.sqrt(np.clip(m['oiii_narrow_sigma_kms']**2 - m['sig_inst']**2, 0, None))
print('median instrumental sigma km/s:')
print(m.groupby('sample')['sig_inst'].median())
print('median narrow sigma after correction:')
print(m.groupby('sample')['narrow_corr'].median())

m = m.merge(cat[['TARGETID', 'snr']], on='TARGETID')
m['broad_det'] = m['oiii_broad_amp'] > 3 * m['oiii_broad_amp_err']
lo = max(m[m['sample'] == 'large']['snr'].min(), m[m['sample'] == 'small']['snr'].min())
hi = min(m[m['sample'] == 'large']['snr'].max(), m[m['sample'] == 'small']['snr'].max())
band = m[(m['snr'] >= lo) & (m['snr'] <= hi)]
print('matched SNR range:', round(lo, 1), 'to', round(hi, 1))
print(band.groupby('sample')['snr'].median())
print(band.groupby('sample')['broad_det'].agg(['size', 'mean']))

w80 = []
for i, r in m.iterrows():
    v = np.linspace(-5000, 5000, 20001)
    prof = r['oiii_narrow_amp'] * np.exp(-0.5 * (v / r['oiii_narrow_sigma_kms'])**2) \
         + r['oiii_broad_amp'] * np.exp(-0.5 * (v / r['oiii_broad_sigma_kms'])**2)
    csum = np.cumsum(prof) / prof.sum()
    w80.append(np.interp(0.90, csum, v) - np.interp(0.10, csum, v))
m['w80'] = w80
print('median W80 km/s:')
print(m.groupby('sample')['w80'].median())
a = m[m['sample'] == 'large']['w80']
b = m[m['sample'] == 'small']['w80']
print('W80 KS p =', round(ks_2samp(a, b).pvalue, 4))

m.to_csv('notes/2026-07-13_resolution_w80.csv', index=False)
print('saved notes/2026-07-13_resolution_w80.csv')