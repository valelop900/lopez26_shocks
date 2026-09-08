import os
import numpy as np
import pandas as pd

# reads data/ and notes/ and writes zenodo/upload/, so work from the project root whatever
# directory this was called from
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

c = 299792.458
rounding = {'RA': 6, 'DEC': 6, 'Z': 5, 'Physical_Size': 2,
            'log_L_radio': 3, 'w80': 1, 'sl_distance': 4,
            'log_oi_ha': 4, 'log_oiii_hb': 4}

sm = pd.read_csv('data/catalog_small.csv')
lg = pd.read_csv('data/catalog_large.csv')

# the pyspeckit line fits behind Section 2.2 of the paper. these are what Figures 1, 3, 4
# and 5 and the sl_distance column are built from, so they have to ship.
def load(*names):
    return pd.concat([pd.read_csv('notes/' + n) for n in names],
                     ignore_index=True).drop_duplicates('TARGETID')

oiii = load('2026-07-08_oiii_fits.csv', '2026-07-22_oiii_fits_new_large.csv',
            '2026-07-31_oiii_fits_new_small24.csv')
oi = load('2026-07-09_oi_fits.csv', '2026-07-22_oi_fits_new_large.csv',
          '2026-07-31_oi_fits_new_small24.csv')
hb = load('2026-07-15_hbeta_fits.csv', '2026-07-22_hbeta_fits_new_large.csv',
          '2026-07-31_hbeta_fits_new_small24.csv')
ha = load('2026-07-16_halpha_fits.csv', '2026-07-22_halpha_fits_new_large.csv',
          '2026-07-31_halpha_fits_new_small24.csv')
fits = oiii.merge(oi, on='TARGETID', suffixes=('', '_oi'))
fits = fits.merge(hb, on='TARGETID', suffixes=('', '_hb'))
fits = fits.merge(ha, on='TARGETID', suffixes=('', '_ha'))

# integrate the Gaussians. narrow + broad only, the very broad component of Ha and Hb is
# the BLR and is left out, same as the BPT script.
def gauss(lam0, pairs):
    t = 0.
    for amp, sig in pairs:
        t = t + fits[amp].fillna(0) * fits[sig].fillna(0)/c * lam0*(1 + fits['Z'])
    return np.sqrt(2*np.pi) * t

fit = pd.DataFrame({'TARGETID': fits['TARGETID']})
fit['fit_HB_FLUX'] = gauss(4861.3, [('hb_narrow_amp', 'hb_narrow_sigma_kms'),
                                    ('hb_broad_amp', 'hb_broad_sigma_kms')])
fit['fit_OIII_5007_FLUX'] = gauss(5006.8, [('oiii_narrow_amp', 'oiii_narrow_sigma_kms'),
                                           ('oiii_broad_amp', 'oiii_broad_sigma_kms')])
fit['fit_OI_6300_FLUX'] = gauss(6300.30, [('oi_narrow_amp', 'oi_narrow_sigma_kms'),
                                          ('oi_broad_amp', 'oi_broad_sigma_kms')])
fit['fit_HA_FLUX'] = gauss(6562.8, [('ha_narrow_amp', 'ha_narrow_sigma_kms'),
                                    ('ha_broad_amp', 'ha_broad_sigma_kms')])
# [NII] kinematics are tied to Ha, so it has no sigma of its own
fit['fit_NII_6584_FLUX'] = gauss(6583.5, [('nii_narrow_amp', 'ha_narrow_sigma_kms'),
                                          ('nii_broad_amp', 'ha_broad_sigma_kms')])

bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
fit = fit.merge(bpt[['TARGETID', 'log_oi_ha', 'log_oiii_hb']], on='TARGETID')

# one file, small then large, keyed by TARGETID with the sample column telling them apart
d = pd.concat([sm, lg], ignore_index=True)
d = d.merge(fit, on='TARGETID', how='left')
for col, n in rounding.items():
    d[col] = d[col].round(n)

d.to_csv('zenodo/upload/catalog_lopez_lacy_2026.csv', index=False)
print('wrote zenodo/upload/catalog_lopez_lacy_2026.csv', len(d), 'rows',
      len(d.columns), 'columns')
