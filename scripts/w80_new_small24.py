import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

c = 299792.458

fits = pd.read_csv('notes/2026-07-31_oiii_fits_new_small24.csv')
cat = pd.read_csv('data/VLASS3_2_OI_small.csv')

fits['sample'] = 'small'

# instrument resolution correction, same as before
m = fits.copy()
m['lam_obs'] = 5006.84 * (1 + m['Z'])
m['R'] = np.interp(m['lam_obs'], [5760, 7620], [3200, 4100])
m['sig_inst'] = c / (m['R'] * 2.3548)
m['narrow_corr'] = np.sqrt(np.clip(m['oiii_narrow_sigma_kms']**2 - m['sig_inst']**2, 0, None))

# catalog SNR from the new file
cat['snr'] = cat['OIII_5007_FLUX'] * np.sqrt(cat['OIII_5007_FLUX_IVAR'])
m = m.merge(cat[['TARGETID_1', 'snr']], left_on='TARGETID', right_on='TARGETID_1')
m = m.drop(columns='TARGETID_1')
m['broad_det'] = m['oiii_broad_amp'] > 3 * m['oiii_broad_amp_err']

# W80 from the summed profile, same as before
w80 = []
for i, r in m.iterrows():
    v = np.linspace(-5000, 5000, 20001)
    prof = r['oiii_narrow_amp'] * np.exp(-0.5 * (v / r['oiii_narrow_sigma_kms'])**2) \
         + r['oiii_broad_amp'] * np.exp(-0.5 * (v / r['oiii_broad_sigma_kms'])**2)
    csum = np.cumsum(prof) / prof.sum()
    w80.append(np.interp(0.90, csum, v) - np.interp(0.10, csum, v))
m['w80'] = w80

print('new large: n =', len(m))
print('median W80 new large:', round(m['w80'].median(), 1))
print('median catalog SNR new large:', round(m['snr'].median(), 1))
print('broad detected:', m['broad_det'].sum(), 'of', len(m))

m.to_csv('notes/2026-07-31_w80_new_small24.csv', index=False)
print('saved notes/2026-07-31_w80_new_small24.csv')

# combine with old results and rerun the comparison
old = pd.read_csv('notes/2026-07-13_resolution_w80.csv')
both = pd.concat([old, m], ignore_index=True)

lg = both[both['sample'] == 'large']['w80']
sm = both[both['sample'] == 'small']['w80']
print('combined: large n =', len(lg), 'small n =', len(sm))
print('median W80 large:', round(lg.median(), 1))
print('median W80 small:', round(sm.median(), 1))
print('W80 KS p =', round(ks_2samp(lg, sm).pvalue, 4))
