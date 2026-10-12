import os
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, mannwhitneyu, anderson_ksamp

# catalog is one level up
here = os.path.dirname(os.path.abspath(__file__))
d = pd.read_csv(os.path.join(here, '..', 'catalog_lopez_lacy_2026.csv'))
sm = d[d['sample'] == 'small']
lg = d[d['sample'] == 'large']

print('rows in file: %d' % len(d))
print('counts: small %d  large %d' % (len(sm), len(lg)))
print('duplicate TARGETIDs in file: %d' % d['TARGETID'].duplicated().sum())
print('duplicate TARGETIDs: small %d  large %d'
      % (sm['TARGETID'].duplicated().sum(), lg['TARGETID'].duplicated().sum()))
print('in both samples:', len(set(sm['TARGETID']) & set(lg['TARGETID'])))
for name, s in [('small', sm), ('large', lg)]:
    c = s['bpt_class'].value_counts()
    print('bpt counts %s: seyfert %d  liner %d  sf %d'
          % (name, c.get('seyfert', 0), c.get('liner', 0), c.get('sf', 0)))
print()

sm_sy = sm[sm['bpt_class'] == 'seyfert']['w80']
lg_sy = lg[lg['bpt_class'] == 'seyfert']['w80']
print('W80 median seyferts only: small %.1f (n=%d)  large %.1f (n=%d)'
      % (sm_sy.median(), len(sm_sy), lg_sy.median(), len(lg_sy)))
print('W80 KS p = %.4f' % ks_2samp(sm_sy, lg_sy).pvalue)
print('W80 MW p = %.4f' % mannwhitneyu(sm_sy, lg_sy).pvalue)
sm_li = sm[sm['bpt_class'] == 'liner']['w80']
print('W80 median small only: seyfert %.1f (n=%d)  liner %.1f (n=%d)'
      % (sm_sy.median(), len(sm_sy), sm_li.median(), len(sm_li)))
print('W80 small seyfert vs liner KS p = %.2f' % ks_2samp(sm_sy, sm_li).pvalue)
print()

print('sl_distance median: small %.2f  large %.2f'
      % (sm['sl_distance'].median(), lg['sl_distance'].median()))
print('sl_distance MW p = %.3f'
      % mannwhitneyu(lg['sl_distance'], sm['sl_distance']).pvalue)
print('sl_distance AD p = %.3f'
      % anderson_ksamp([lg['sl_distance'], sm['sl_distance']],
                       variant='midrank').pvalue)
print('sl_distance KS p = %.2f'
      % ks_2samp(lg['sl_distance'], sm['sl_distance']).pvalue)
print()

nev_snr = {}
nev_det = {}
for name, s in [('small', sm), ('large', lg)]:
    nev_snr[name] = s['NEV_3426_FLUX'] * np.sqrt(s['NEV_3426_FLUX_IVAR'])
    nev_det[name] = (nev_snr[name] > 3) & (s['NEV_3426_FLUX'] > 0)

for sig in [3, 5]:
    row = []
    for name, s in [('small', sm), ('large', lg)]:
        det = (nev_snr[name] > sig) & (s['NEV_3426_FLUX'] > 0)
        row.append('%s %.0f%% (%d/%d)' % (name, 100*det.sum()/len(s), det.sum(), len(s)))
    print('NeV %d sigma: %s  %s' % (sig, row[0], row[1]))

row = []
for name, s in [('small', sm), ('large', lg)]:
    m = (s['Z'] > 0.30) & (s['Z'] < 0.45)
    det = nev_det[name] & m
    row.append('%s %.0f%% (%d/%d)' % (name, 100*det.sum()/m.sum(), det.sum(), m.sum()))
print('NeV 3 sigma, 0.30 < z < 0.45: %s  %s' % (row[0], row[1]))
print()

bd = {}
for name, s in [('small', sm), ('large', lg)]:
    good = (s['HALPHA_FLUX'] > 0) & (s['HBETA_FLUX'] > 0)
    bd[name] = (s['HALPHA_FLUX'] / s['HBETA_FLUX']).where(good)
    print('balmer median %s %.2f (n=%d)'
          % (name, bd[name].median(), bd[name].notna().sum()))
print('balmer MW p = %.3f'
      % mannwhitneyu(bd['large'].dropna(), bd['small'].dropna()).pvalue)

row = []
for name, s in [('small', sm), ('large', lg)]:
    m = bd[name] < 4
    det = nev_det[name] & m
    row.append('%s %.0f%% (%d/%d)' % (name, 100*det.sum()/m.sum(), det.sum(), m.sum()))
print('NeV 3 sigma, balmer < 4: %s  %s' % (row[0], row[1]))

for name in ['small', 'large']:
    nd = bd[name][~nev_det[name]].dropna()
    de = bd[name][nev_det[name]].dropna()
    print('balmer %s, NeV nondet %.2f (n=%d) vs det %.2f (n=%d), MW p = %.2f'
          % (name, nd.median(), len(nd), de.median(), len(de),
             mannwhitneyu(nd, de).pvalue))
print()

for name, d in [('small', sm), ('large', lg)]:
    t1 = (d['HALPHA_BROAD_FLUX'].fillna(0) > 0).sum()
    print('type1 %s: %d of %d' % (name, t1, len(d)))
print()

mpc_to_m = 3.086e22
mjy_to_si = 1e-29
for name, d in [('small', sm), ('large', lg)]:
    alpha = d['Alpha'].fillna(-0.7)
    L3 = 4*np.pi * (d['D_L']*mpc_to_m)**2 * (d['Flux']*mjy_to_si) * (1+d['Z'])**(-1-alpha)
    print('log_L_radio from Flux, max diff %s %.3f'
          % (name, (np.log10(L3) - d['log_L_radio']).abs().max()))
    L151 = L3 * (151/3000.)**(-0.7)
    Q = 3e38 * (L151/(4*np.pi)/1e28)**(6./7)
    print('logQ median %s %.2f' % (name, np.log10(Q).median()))
