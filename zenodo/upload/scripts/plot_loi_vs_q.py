import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

LARGE_COLOR = 'black'
SMALL_COLOR = '#5B2C6F'
MARKERS = {'seyfert': ('o', 45), 'liner': ('*', 110)}
LABELS = {'seyfert': 'Seyfert', 'liner': 'LINER'}
c = 299792.458
mpc_to_cm = 3.086e24

fits = pd.concat([pd.read_csv('notes/2026-07-09_oi_fits.csv'),
                  pd.read_csv('notes/2026-07-22_oi_fits_new_large.csv'),
                  pd.read_csv('notes/2026-07-31_oi_fits_new_small24.csv')],
                 ignore_index=True).drop_duplicates('TARGETID')
lam_obs = 6300.30 * (1 + fits['Z'])
sig_n = fits['oi_narrow_sigma_kms'] / c * lam_obs
sig_b = fits['oi_broad_sigma_kms'] / c * lam_obs
fits['oi_flux'] = np.sqrt(2*np.pi) * (fits['oi_narrow_amp'].fillna(0)*sig_n.fillna(0)
                                      + fits['oi_broad_amp'].fillna(0)*sig_b.fillna(0))

m = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
m = m.merge(bpt[['TARGETID', 'bpt_class']], on='TARGETID')
m = m.merge(fits[['TARGETID', 'oi_flux']], on='TARGETID')
m = m[m['log_L_radio'] > 24]
m = m[(m['sample'] == 'small') | (m['Physical_Size'] > 25)]
print('plotted objects:', len(m), 'of 77')

q = pd.concat([pd.read_csv('data/catalog_small_Q.csv'),
               pd.read_csv('data/catalog_large_Q.csv')], ignore_index=True)
m = m.merge(q[['TARGETID', 'logQ']], on='TARGETID')
m['logQ_erg'] = m['logQ'] + 7
dL = m['D_L'] * mpc_to_cm
m['logL_OI'] = np.log10(m['oi_flux'] * 1e-17 * 4*np.pi * dL**2)

fig, ax = plt.subplots(figsize=(7, 7))
ax.set_aspect('equal', adjustable='box')
for s in ['large', 'small']:
    for cl in ['seyfert', 'liner']:
        sub = m[(m['sample'] == s) & (m['bpt_class'] == cl)]
        mk, ms = MARKERS[cl]
        if s == 'large':
            ax.scatter(sub['logQ_erg'], sub['logL_OI'], marker=mk, s=ms,
                       facecolors=LARGE_COLOR, edgecolors=LARGE_COLOR,
                       label='large %s (n=%d)' % (LABELS[cl], len(sub)))
        else:
            ax.scatter(sub['logQ_erg'], sub['logL_OI'], marker=mk, s=ms,
                       facecolors='none', edgecolors=SMALL_COLOR, linewidths=1.3,
                       label='small %s (n=%d)' % (LABELS[cl], len(sub)))

lo, hi = 41, 45
ax.plot([lo, hi], [lo, hi], 'k--', lw=0.8, label='L[OI] = Q')
ax.plot([lo, hi], [lo-2, hi-2], 'k:', lw=0.8, label='1% of Q')
ax.set_xlim(m['logQ_erg'].min()-0.3, m['logQ_erg'].max()+0.3)
ax.set_ylim(m['logL_OI'].min()-0.3, m['logL_OI'].max()+0.3)
ax.set_xlabel('log Q (erg/s)', fontsize=14)
ax.set_ylabel('log L[OI] (erg/s)', fontsize=14)
ax.tick_params(labelsize=12)
ax.legend(fontsize=10, loc='lower right')
plt.tight_layout()
plt.savefig('plots/2026-08-27_loi_vs_q_v2.png', dpi=150)
plt.savefig('plots/fig_loi_vs_q.pdf')
print('saved')