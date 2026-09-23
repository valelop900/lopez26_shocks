import numpy as np
import pandas as pd
import pyspeckit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import paperstyle
import figcheck

# makes fig_oiii_profiles.pdf: [OIII] profiles of the broadest small sources with the two-gaussian fit.
# same model as fit_oiii_all.py but the broad centroid can move +-20 A, and the offset is kept.
# reads data/catalog_small.csv and data/spectra/. run from the project root.

small = pd.read_csv('data/catalog_small.csv')
hi = small[small['w80'] > 1000].sort_values('w80', ascending=False)

c = 299792.458
ratio = 4958.9 / 5006.8
rows = []
fits_for_plot = {}

for i, r in hi.iterrows():
    tid = r['TARGETID']
    z = r['Z']
    spec = pd.read_csv('data/spectra/%d_desispec.csv' % tid)
    lam = spec['Lambda'].values
    flam = spec['FLambda17'].values
    o5007 = 5006.8 * (1 + z)
    o4959 = 4958.9 * (1 + z)

    sp = pyspeckit.Spectrum(data=flam, xarr=lam, xarrkwargs={'unit': 'Angstrom'})
    sp.plotter(xmin=o4959-60, xmax=o5007+80)
    sp.baseline(xmin=o4959-60, xmax=o5007+80, exclude=[o4959-25, o5007+25], subtract=True, order=1)
    guesses = [10, o5007, 2.5, 4, o5007, 10.0, 3.3, o4959, 2.5, 1.3, o4959, 10.0]
    limits = [(0, 0), (o5007-10, o5007+10), (0.5, 4.5), (0, 0), (o5007-20, o5007+20), (4.5, 30.0),
              (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
    limited = [(True, False), (True, True), (True, True), (True, False), (True, True), (True, True),
               (False, False), (False, False), (False, False), (False, False), (False, False), (False, False)]
    tied = ['', '', '', '', '', '', 'p[0]/3.0', 'p[1]*' + str(ratio), 'p[2]*' + str(ratio),
            'p[3]/3.0', 'p[4]*' + str(ratio), 'p[5]*' + str(ratio)]
    sp.specfit(fittype='gaussian', guesses=guesses, limits=limits, limited=limited, tied=tied)
    v = sp.specfit.parinfo.values
    e = sp.specfit.parinfo.errors

    dv = c * (v[4] - v[1]) / v[1]
    # W80 from this fit, same recipe as w80_new_small24.py but with the offset kept
    vv = np.linspace(-5000, 5000, 20001)
    prof = v[0]*np.exp(-0.5*(vv/(c*v[2]/v[1]))**2) + v[3]*np.exp(-0.5*((vv-dv)/(c*v[5]/v[4]))**2)
    cs = np.cumsum(prof)/prof.sum()
    w80_refit = np.interp(0.90, cs, vv) - np.interp(0.10, cs, vv)
    dv_err = c * np.hypot(e[4], e[1]) / v[1]
    at_limit = abs(v[4] - o5007) > 19.9     # broad centroid allowed +-20 A here, the paper fit used +-5
    rows.append([tid, z, r['w80'], w80_refit, r['bpt_class'], c*v[2]/v[1], c*v[5]/v[4], v[0], v[3], dv, dv_err, at_limit])
    fits_for_plot[tid] = (sp.xarr.value.copy(), sp.data.copy(), v)
    plt.close('all')

out = pd.DataFrame(rows, columns=['TARGETID', 'Z', 'w80', 'w80_refit', 'bpt_class', 'narrow_sigma_kms', 'broad_sigma_kms',
                                  'narrow_amp', 'broad_amp', 'dv_broad_kms', 'dv_err_kms', 'broad_at_limit'])
out.to_csv('notes/2026-09-13_oiii_profiles_highw80.csv', index=False)
print(out.round(1).to_string(index=False))
print()
blue = out[out['dv_broad_kms'] < -2*out['dv_err_kms']]
red = out[out['dv_broad_kms'] > 2*out['dv_err_kms']]
print('of %d small sources with W80 > 1000: broad component blueshifted at >2 sigma: %d, redshifted: %d, consistent with zero: %d'
      % (len(out), len(blue), len(red), len(out) - len(blue) - len(red)))
print('broad centroid pinned at the +-5 A fit limit:', int(out['broad_at_limit'].sum()))
print('note: +-5 A at these redshifts is only +-%.0f to +-%.0f km/s, so a larger outflow offset could not have been fit'
      % (c*5/(5006.8*(1+out['Z'].max())), c*5/(5006.8*(1+out['Z'].min()))))

# two panels: the -925 km/s object and the cleanest of the other high-W80 fits.
# 39628066753877605 left out, its narrow core at +250 km/s was missed by the fit.
show = [39628159028563219, 39633349756585024]
def g(x, a, mu, s):
    return a * np.exp(-0.5 * ((x - mu) / s)**2)

fig, axes = plt.subplots(1, 2, figsize=paperstyle.TWO_PANEL)
for ax, tid in zip(axes, show):
    x, y, v = fits_for_plot[tid]
    r = out[out['TARGETID'] == tid].iloc[0]
    vel = c * (x - 5006.8*(1 + r['Z'])) / (5006.8*(1 + r['Z']))
    m = (vel > -4000) & (vel < 3000)
    ax.step(vel[m], y[m], where='mid', color='k', label='data')
    tot = sum(g(x, v[3*k], v[3*k+1], v[3*k+2]) for k in range(4))
    ax.plot(vel[m], tot[m], 'r-', label='total fit')
    ax.plot(vel[m], g(x, v[0], v[1], v[2])[m], 'b--', label='narrow')
    ax.plot(vel[m], g(x, v[3], v[4], v[5])[m], 'g--', label='broad')
    ax.axvline(0, color='0.6', lw=0.8)
    ax.axvline(r['dv_broad_kms'], color='g', lw=0.8, ls=':')
    ax.set_ylabel(r'F$_\lambda$ (10$^{-17}$ erg s$^{-1}$ cm$^{-2}$ $\mathrm{\AA}^{-1}$)')
    ax.set_xlabel(r'v - v(narrow [O III]) (km s$^{-1}$)')
figcheck.place_legend(axes[0], 'profiles left')
plt.tight_layout()
plt.savefig('plots/fig_oiii_profiles.pdf')
plt.savefig('plots/fig_oiii_profiles.png', dpi=paperstyle.PNG_DPI)
print('saved plots/fig_oiii_profiles.pdf')
