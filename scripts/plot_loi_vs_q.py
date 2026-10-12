import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import paperstyle

# makes fig_loi_vs_q.pdf: [OI] luminosity against jet power.
# reads the [OI] fit tables and luminosity table in notes/ and data/catalog_*_Q.csv. run from the project root.

LARGE_COLOR = 'black'
SMALL_COLOR = '#5B2C6F'
MARKERS = {'seyfert': ('o', paperstyle.S1['o']), 'liner': ('*', paperstyle.S1['*'])}
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

fig, ax = plt.subplots(figsize=paperstyle.ONE_PANEL)
for s in ['large', 'small']:
    for cl in ['seyfert', 'liner']:
        sub = m[(m['sample'] == s) & (m['bpt_class'] == cl)]
        mk, ms = MARKERS[cl]
        if s == 'large':
            ax.scatter(sub['logQ_erg'], sub['logL_OI'], marker=mk, s=ms,
                       facecolors=LARGE_COLOR, edgecolors=LARGE_COLOR,
                       label='large %s (%d)' % (LABELS[cl], len(sub)))
        else:
            ax.scatter(sub['logQ_erg'], sub['logL_OI'], marker=mk, s=ms,
                       facecolors='none', edgecolors=SMALL_COLOR, linewidths=1.0,
                       label='small %s (%d)' % (LABELS[cl], len(sub)))

lo, hi = 41, 45
ax.plot([lo, hi], [lo, hi], 'k--')
ax.plot([lo, hi], [lo-2, hi-2], 'k:')
ax.set_xlim(m['logQ_erg'].min()-0.3, m['logQ_erg'].max()+0.8)
ax.set_ylim(m['logL_OI'].min()-0.5, m['logL_OI'].max()+0.6)
ax.set_xlabel(r'log Q (erg s$^{-1}$)', fontsize=paperstyle.LABEL1)
ax.set_ylabel(r'log L[O I] (erg s$^{-1}$)', fontsize=paperstyle.LABEL1)
ax.tick_params(labelsize=paperstyle.TICK1)
ax.legend(loc='lower right', fontsize=8, framealpha=1)
plt.tight_layout()

# the two reference lines are labelled along the lines, at the angle they have on the page
x0, x1 = ax.get_xlim()
p0 = ax.transData.transform((x0 + 0.05, x0 + 0.05))
p1 = ax.transData.transform((x0 + 0.55, x0 + 0.55))
ang = np.degrees(np.arctan2(p1[1] - p0[1], p1[0] - p0[0]))
ax.text(x0 + 0.14, x0 + 0.14 + 0.06, 'L[O I] = Q', rotation=ang, rotation_mode='anchor', ha='left', va='bottom', fontsize=9)
ax.text(43.55, 43.55 - 2 - 0.08, '1% of Q', rotation=ang, rotation_mode='anchor', ha='left', va='top', fontsize=9)
plt.savefig('plots/fig_loi_vs_q.png', dpi=paperstyle.PNG_DPI)
plt.savefig('plots/fig_loi_vs_q.pdf')
print('saved')