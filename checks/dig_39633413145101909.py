import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

t = 39633413145101909

# 1. every parameter your fitter produced, all four lines
for name, path in [('OIII', 'notes/2026-07-08_oiii_fits.csv'),
                   ('OI', 'notes/2026-07-09_oi_fits.csv'),
                   ('HB', 'notes/2026-07-15_hbeta_fits.csv'),
                   ('HA', 'notes/2026-07-16_halpha_fits.csv')]:
    tab = pd.read_csv(path)
    hit = tab[tab['TARGETID'] == t]
    print('----', name, path)
    if len(hit) == 0:
        print('  not in this file')
    else:
        print(hit.T.to_string())
    print()

# 2. what DESI's own pipeline measured for the same object
cols_want = ['TARGETID', 'Z', 'HALPHA_FLUX', 'HALPHA_FLUX_IVAR',
             'HBETA_FLUX', 'OIII_5007_FLUX', 'OI_6300_FLUX',
             'NII_6584_FLUX', 'HALPHA_SIGMA', 'OIII_5007_SIGMA']
for path in ['data/OI_sample_small.csv', 'data/VLASS3_2_OI_small.csv']:
    cat = pd.read_csv(path)
    if 'TARGETID_1' in cat.columns:
        cat = cat.rename(columns={'TARGETID_1': 'TARGETID'})
    hit = cat[cat['TARGETID'] == t]
    print('----', path)
    if len(hit) == 0:
        print('  not in this catalog')
    else:
        have = [c for c in cols_want if c in cat.columns]
        print(hit[have].T.to_string())
        z = hit['Z'].iloc[0]
    print()

# 3. the spectrum itself, three panels around the key lines
try:
    spec = pd.read_csv(f'data/spectra/{t}_desispec.csv')
except FileNotFoundError:
    print('no spectrum file at data/spectra/%d_desispec.csv' % t)
    raise SystemExit
wave = spec['Lambda'] / (1 + z)
flux = spec['FLambda17']

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
for ax, (lo, hi, marks) in zip(axes, [
        (4930, 5090, [4958.9, 5006.8]),
        (6230, 6380, [6300.3, 6363.8]),
        (6420, 6700, [6548.0, 6562.8, 6583.5])]):
    
    sel = (wave > lo) & (wave < hi)
    ax.plot(wave[sel], flux[sel], 'k', lw=0.8)
    for lam in marks:
        ax.axvline(lam, color='gray', ls=':', lw=0.8)
    ax.set_xlabel('rest wavelength (A)')
axes[0].set_ylabel('flux')
plt.tight_layout()
plt.savefig('plots/2026-08-21_dig_3347.png', dpi=150)
print('saved plots/2026-08-21_dig_3347.png')
