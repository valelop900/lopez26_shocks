import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

LARGE_COLOR = 'black'
SMALL_COLOR = '#5B2C6F'
MARKERS = {'seyfert': ('o', 45), 'liner': ('*', 110)}
c = 299792.458
mpc_to_cm = 3.086e24

fits = pd.concat([pd.read_csv('notes/2026-07-09_oi_fits.csv'),
                  pd.read_csv('notes/2026-07-22_oi_fits_new_large.csv'),
                  pd.read_csv('notes/2026-07-31_oi_fits_new_small24.csv')],
                 ignore_index=True).drop_duplicates('TARGETID')
lam_obs = 6300. * (1 + fits['Z'])
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

L3 = 10**m['log_L_radio']
L151 = L3 * (151/3000.)**(-0.7)
m['logQ_erg'] = np.log10(3e38 * (L151/(4*np.pi)/1e28)**(6./7)) + 7
dL = m['D_L'] * mpc_to_cm
m['logL_OI'] = np.log10(m['oi_flux'] * 1e-17 * 4*np.pi * dL**2)
m['logL_OIII'] = np.log10(m['OIII_5007_FLUX'] * 1e-17 * 4*np.pi * dL**2)

def panels(ycol, ylabel, outname):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), sharex=True, sharey=True)
    for ax, s, col in [(axes[0], 'small', SMALL_COLOR), (axes[1], 'large', LARGE_COLOR)]:
        for cl in ['seyfert', 'liner']:
            sub = m[(m['sample'] == s) & (m['bpt_class'] == cl)]
            mk, ms = MARKERS[cl]
            if s == 'large':
                ax.scatter(sub['logQ_erg'], sub[ycol], marker=mk, s=ms,
                           facecolors=col, edgecolors=col, label='%s (n=%d)' % (cl, len(sub)))
            else:
                ax.scatter(sub['logQ_erg'], sub[ycol], marker=mk, s=ms, facecolors='none',
                           edgecolors=col, linewidths=1.3, label='%s (n=%d)' % (cl, len(sub)))
        ax.set_title(s); ax.set_xlabel('log Q (erg/s)'); ax.legend(fontsize=8)
    axes[0].set_ylabel(ylabel)
    plt.tight_layout()
    plt.savefig('plots/%s.png' % outname, dpi=150)
    plt.savefig('plots/%s.pdf' % outname)
    plt.close()
    print('saved', outname)

panels('logL_OI', 'log L[OI] (erg/s)', 'fig_loi_vs_q_panels')
panels('logL_OIII', 'log L[OIII] (erg/s)', 'fig_loiii_vs_q_panels')