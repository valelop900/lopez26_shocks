import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, mannwhitneyu, anderson_ksamp

# every number quoted in the paper, from the release catalog and the fit tables in notes/.

d = pd.read_csv('zenodo/upload/catalog_lopez_lacy_2026.csv')
sm = d[d['sample'] == 'small']
lg = d[d['sample'] == 'large']
print('n small %d  large %d' % (len(sm), len(lg)))

for name, s in [('small', sm), ('large', lg)]:
    print('type1 %s: %d of %d' % (name, (s['HALPHA_BROAD_FLUX'].fillna(0) > 0).sum(), len(s)))
for name, s in [('small', sm), ('large', lg)]:
    c = s['bpt_class'].value_counts()
    print('bpt %s: seyfert %d  liner %d  sf %d' % (name, c.get('seyfert', 0), c.get('liner', 0), c.get('sf', 0)))
print()

ss = sm[sm['bpt_class'] == 'seyfert']['w80']
ls = lg[lg['bpt_class'] == 'seyfert']['w80']
sl = sm[sm['bpt_class'] == 'liner']['w80']
print('W80 median seyferts: small %.0f (n=%d)  large %.0f (n=%d)' % (ss.median(), len(ss), ls.median(), len(ls)))
print('W80 seyferts KS p = %.4f   MW p = %.4f' % (ks_2samp(ss, ls).pvalue, mannwhitneyu(ss, ls).pvalue))
print('W80 small seyfert %.0f vs small liner %.0f (n=%d)  KS p = %.2f' % (ss.median(), sl.median(), len(sl), ks_2samp(ss, sl).pvalue))
print('W80 max large %.0f   small sources above 1300: %d   large above 1300: %d'
      % (lg['w80'].max(), (sm['w80'] > 1300).sum(), (lg['w80'] > 1300).sum()))
print()

a, b = sm['sl_distance'], lg['sl_distance']
print('SL median small %.2f  large %.2f' % (a.median(), b.median()))
print('SL MW p = %.3f   AD p = %.3f   KS p = %.2f'
      % (mannwhitneyu(a, b).pvalue, anderson_ksamp([a.values, b.values], variant='midrank').pvalue, ks_2samp(a, b).pvalue))
print()

d['nev_sn'] = d['NEV_3426_FLUX'] * np.sqrt(d['NEV_3426_FLUX_IVAR'])
d['nev3'] = (d['nev_sn'] > 3) & (d['NEV_3426_FLUX'] > 0)
d['nev5'] = (d['nev_sn'] > 5) & (d['NEV_3426_FLUX'] > 0)
sm = d[d['sample'] == 'small'].copy()
lg = d[d['sample'] == 'large'].copy()
def rate(x, col='nev3'):
    return '%.0f%% (%d/%d)' % (100 * x[col].mean(), x[col].sum(), len(x))
print('NeV 3sig: small %s  large %s' % (rate(sm), rate(lg)))
print('NeV 5sig: small %s  large %s' % (rate(sm, 'nev5'), rate(lg, 'nev5')))
zs = sm[(sm['Z'] > 0.30) & (sm['Z'] < 0.45)]; zl = lg[(lg['Z'] > 0.30) & (lg['Z'] < 0.45)]
print('NeV 3sig, 0.30<z<0.45: small %s  large %s' % (rate(zs), rate(zl)))
print()

for s in (sm, lg):
    s['bd'] = (s['HALPHA_FLUX'] / s['HBETA_FLUX']).where((s['HALPHA_FLUX'] > 0) & (s['HBETA_FLUX'] > 0))
print('balmer median small %.2f  large %.2f  MW p = %.3f'
      % (sm['bd'].median(), lg['bd'].median(), mannwhitneyu(lg['bd'].dropna(), sm['bd'].dropna()).pvalue))
print('NeV 3sig, Ha/Hb < 4: small %s  large %s' % (rate(sm[sm['bd'] < 4]), rate(lg[lg['bd'] < 4])))
for name, s in [('small', sm), ('large', lg)]:
    nd = s['bd'][~s['nev3']].dropna(); de = s['bd'][s['nev3']].dropna()
    print('balmer %s: NeV nondet %.2f (n=%d)  det %.2f (n=%d)  MW p = %.2f' % (name, nd.median(), len(nd), de.median(), len(de), mannwhitneyu(nd, de).pvalue))
print()

# jet power, willott with f=1, flat alpha=-0.7 to 151 MHz, L151 in W/Hz/sr
mpc_to_m = 3.086e22
for name, s in [('small', sm), ('large', lg)]:
    L3 = 4*np.pi * (s['D_L']*mpc_to_m)**2 * (s['Flux']*1e-29) * (1 + s['Z'])**(-1 - s['Alpha'].fillna(-0.7))
    L151 = L3 * (151/3000.)**(-0.7)
    s['logQ'] = np.log10(3e38 * (L151/(4*np.pi)/1e28)**(6./7))
    print('logQ median %s %.2f' % (name, s['logQ'].median()))

c = 299792.458
oi = pd.concat([pd.read_csv('notes/2026-07-09_oi_fits.csv'), pd.read_csv('notes/2026-07-22_oi_fits_new_large.csv'),
                pd.read_csv('notes/2026-07-31_oi_fits_new_small24.csv')], ignore_index=True).drop_duplicates('TARGETID')
lam = 6300.30 * (1 + oi['Z'])
oi['oi_flux'] = np.sqrt(2*np.pi) * (oi['oi_narrow_amp'].fillna(0) * (oi['oi_narrow_sigma_kms']/c*lam).fillna(0)
                                    + oi['oi_broad_amp'].fillna(0) * (oi['oi_broad_sigma_kms']/c*lam).fillna(0))
both = pd.concat([sm, lg]).merge(oi[['TARGETID', 'oi_flux']], on='TARGETID')
both['logL_OI'] = np.log10(both['oi_flux'] * 1e-17 * 4*np.pi * (both['D_L']*3.086e24)**2)
frac = both['logL_OI'] - (both['logQ'] + 7)
print('L_OI/Q > 0.01: %d of %d (%.0f%%)   small %d/%d  large %d/%d'
      % ((frac > -2).sum(), len(both), 100*(frac > -2).mean(),
         ((frac > -2) & (both['sample'] == 'small')).sum(), (both['sample'] == 'small').sum(),
         ((frac > -2) & (both['sample'] == 'large')).sum(), (both['sample'] == 'large').sum()))
print()

# ---- new for the revision ----
print('--- broad [OIII] offsets, free-centroid refit')
dv = pd.read_csv('notes/2026-09-18_oiii_dv_all.csv').drop(columns='w80').merge(d[['TARGETID', 'w80']], on='TARGETID')
dv['det'] = dv['broad_amp'] > 3 * dv['broad_err']
hi = dv[(dv['sample'] == 'small') & (dv['w80'] > 1300)]
print('small W80 > 1300: n=%d, broad detected %d, of which dv < -150: %d, dv > +150: %d'
      % (len(hi), hi['det'].sum(), (hi['det'] & (hi['dv'] < -150)).sum(), (hi['det'] & (hi['dv'] > 150)).sum()))
hi = dv[(dv['sample'] == 'small') & (dv['w80'] > 1000) & dv['det']]
print('small W80 > 1000, broad detected: n=%d, dv < -150: %d, |dv| < 150: %d' % (len(hi), (hi['dv'] < -150).sum(), (hi['dv'].abs() < 150).sum()))
for name in ['small', 'large']:
    x = dv[(dv['sample'] == name) & dv['det']]
    print('median broad offset %s: %+.0f km/s (n=%d)' % (name, x['dv'].median(), len(x)))
print()

print('--- NeV vs W80 within each sample')
for name, s in [('small', sm), ('large', lg)]:
    de, nd = s[s['nev3']], s[~s['nev3']]
    print('%s: det median W80 %.0f (n=%d)  nondet %.0f (n=%d)  MW p = %.2f' % (name, de['w80'].median(), len(de), nd['w80'].median(), len(nd), mannwhitneyu(de['w80'], nd['w80']).pvalue))
    hiw = s[s['w80'] > s['w80'].median()]; low = s[s['w80'] <= s['w80'].median()]
    print('%s: NeV rate above median W80 (%.0f) %s   below %s' % (name, s['w80'].median(), rate(hiw), rate(low)))
for cl in ['seyfert', 'liner', 'sf']:
    print('small NeV rate by class %s: %s' % (cl, rate(sm[sm['bpt_class'] == cl])))
print()

print('--- NeV vs AGN type, luminosity, hardness')
for s in (sm, lg):
    s['logL'] = np.log10(4*np.pi*(s['D_L']*3.086e24)**2 * s['OIII_5007_FLUX']*1e-17)
    s['oiii_hb'] = s['OIII_5007_FLUX'] / s['HBETA_FLUX']
sy_s = sm[sm['bpt_class'] == 'seyfert']; sy_l = lg[lg['bpt_class'] == 'seyfert']
print('seyferts only NeV 3sig: small %s  large %s' % (rate(sy_s), rate(sy_l)))
print('log L[OIII] median small %.2f  large %.2f' % (sm['logL'].median(), lg['logL'].median()))
print('[OIII]/Hb median seyferts small %.2f  large %.2f' % (sy_s['oiii_hb'].median(), sy_l['oiii_hb'].median()))
cut = 5
print('hardness matched (seyferts with [OIII]/Hb > %d): small %s  large %s' % (cut, rate(sy_s[sy_s['oiii_hb'] > cut]), rate(sy_l[sy_l['oiii_hb'] > cut])))
tol = 0.15
lgs = lg.sort_values('logL'); used = set(); pairs = []
for i, r in sm.sort_values('logL').iterrows():
    cand = lgs[~lgs.index.isin(used)]
    j = (cand['logL'] - r['logL']).abs().idxmin()
    if abs(lgs.loc[j, 'logL'] - r['logL']) < tol:
        used.add(j); pairs.append((r['nev3'], lgs.loc[j, 'nev3']))
p = np.array(pairs)
print('L[OIII] matched 1:1 within %.2f dex: %d pairs, NeV small %.0f%% (%d)  large %.0f%% (%d)'
      % (tol, len(p), 100*p[:, 0].mean(), p[:, 0].sum(), 100*p[:, 1].mean(), p[:, 1].sum()))
de = d[d['nev3']]
de_s, de_l = de[de['sample'] == 'small'], de[de['sample'] == 'large']
r_s = de_s['NEV_3426_FLUX'] / de_s['OIII_5007_FLUX']; r_l = de_l['NEV_3426_FLUX'] / de_l['OIII_5007_FLUX']
print('NeV/[OIII] among detections: small median %.3f (n=%d)  large %.3f (n=%d)  MW p = %.3f' % (r_s.median(), len(r_s), r_l.median(), len(r_l), mannwhitneyu(r_s, r_l).pvalue))
ul_s = (3/np.sqrt(sm[~sm['nev3']]['NEV_3426_FLUX_IVAR']) / sm[~sm['nev3']]['OIII_5007_FLUX']).median()
ul_l = (3/np.sqrt(lg[~lg['nev3']]['NEV_3426_FLUX_IVAR']) / lg[~lg['nev3']]['OIII_5007_FLUX']).median()
print('3sig NeV/[OIII] upper limit, nondetections: small median %.3f  large %.3f  ratio small/large %.1f' % (ul_s, ul_l, ul_s/ul_l))
print()

print('--- broad vs narrow [OIII]/Hb, each component at 2 sigma')
def load(*fs):
    return pd.concat([pd.read_csv('notes/' + f) for f in fs], ignore_index=True)
oiii = load('2026-07-08_oiii_fits.csv', '2026-07-22_oiii_fits_new_large.csv', '2026-07-31_oiii_fits_new_small24.csv')
hb = load('2026-07-15_hbeta_fits.csv', '2026-07-22_hbeta_fits_new_large.csv', '2026-07-31_hbeta_fits_new_small24.csv')
m = oiii.merge(hb, on='TARGETID', suffixes=('', '_hb')).drop_duplicates('TARGETID').merge(d[['TARGETID', 'sample']], on='TARGETID')
for comp in ['narrow', 'broad']:
    fo = m['oiii_%s_amp' % comp] * m['oiii_%s_sigma_kms' % comp] * 5006.8
    fh = m['hb_%s_amp' % comp] * m['hb_%s_sigma_kms' % comp] * 4861.3
    ok = (fo > 0) & (fh > 0) & (m['oiii_%s_amp' % comp] > 2*m['oiii_%s_amp_err' % comp]) & (m['hb_%s_amp' % comp] > 2*m['hb_%s_amp_err' % comp])
    m['y_' + comp] = np.log10(fo / fh).where(ok)
b2 = m.dropna(subset=['y_narrow', 'y_broad'])
for name in ['small', 'large']:
    x = b2[b2['sample'] == name]
    print('%s: broad lower than narrow in %d of %d, median broad-narrow %+.2f dex' % (name, (x['y_broad'] < x['y_narrow']).sum(), len(x), (x['y_broad'] - x['y_narrow']).median()))
print('all: broad lower in %d of %d' % ((b2['y_broad'] < b2['y_narrow']).sum(), len(b2)))
nn = m.dropna(subset=['y_narrow'])
print('narrow component only, log[OIII]/Hb median: small %.2f (n=%d)  large %.2f (n=%d)  MW p = %.3f'
      % (nn[nn['sample'] == 'small']['y_narrow'].median(), (nn['sample'] == 'small').sum(),
         nn[nn['sample'] == 'large']['y_narrow'].median(), (nn['sample'] == 'large').sum(),
         mannwhitneyu(nn[nn['sample'] == 'small']['y_narrow'], nn[nn['sample'] == 'large']['y_narrow']).pvalue))
print()

print('--- fisher exact p on the NeV detection counts, small vs large')
from scipy.stats import fisher_exact
def fisher(a, b, col='nev3'):
    t = [[a[col].sum(), len(a) - a[col].sum()], [b[col].sum(), len(b) - b[col].sum()]]
    return fisher_exact(t)[1]
print('3sig            p = %.3f' % fisher(sm, lg))
print('5sig            p = %.3f' % fisher(sm, lg, 'nev5'))
print('0.30<z<0.45     p = %.2f' % fisher(zs, zl))
print('Ha/Hb < 4       p = %.3f' % fisher(sm[sm['bd'] < 4], lg[lg['bd'] < 4]))
print('seyferts only   p = %.3f' % fisher(sy_s, sy_l))
print('hardness cut    p = %.2f' % fisher(sy_s[sy_s['oiii_hb'] > cut], sy_l[sy_l['oiii_hb'] > cut]))
