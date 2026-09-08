import numpy as np
import pandas as pd

c = 299792.458  # km/s

def fit_flux(df):
    lam_obs = 6300. * (1 + df['Z'])
    sig_n = df['oi_narrow_sigma_kms'] / c * lam_obs
    sig_b = df['oi_broad_sigma_kms'] / c * lam_obs
    f = np.sqrt(2*np.pi) * (df['oi_narrow_amp'].fillna(0)*sig_n.fillna(0)
                            + df['oi_broad_amp'].fillna(0)*sig_b.fillna(0))
    return f

fits = pd.concat([pd.read_csv('notes/2026-07-09_oi_fits.csv'),
                  pd.read_csv('notes/2026-07-22_oi_fits_new_large.csv'),
                  pd.read_csv('notes/2026-07-31_oi_fits_new_small24.csv')],
                 ignore_index=True).drop_duplicates('TARGETID')
fits['oi_flux_fit'] = fit_flux(fits)
print('fit fluxes computed:', len(fits))

oi1 = pd.read_csv('data/VLASS3_2_OI_large.csv')[['TARGETID_1', 'OI_6300_FLUX']]
oi2 = pd.read_csv('data/VLASS3_2_OI_small.csv')[['TARGETID_1', 'OI_6300_FLUX']]
cat = pd.concat([oi1, oi2], ignore_index=True).rename(
    columns={'TARGETID_1': 'TARGETID'}).drop_duplicates('TARGETID')

both = fits.merge(cat, on='TARGETID')
both = both[both['OI_6300_FLUX'] > 0]
ratio = both['oi_flux_fit'] / both['OI_6300_FLUX']
print('overlap objects:', len(both))
print('median fit/catalog ratio:', round(ratio.median(), 2))
print('scatter (16-84 pct):', round(ratio.quantile(0.16), 2), '-', round(ratio.quantile(0.84), 2))