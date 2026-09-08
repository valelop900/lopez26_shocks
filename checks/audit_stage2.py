import numpy as np
import pandas as pd
from scipy import stats

# ---------- rebuild the final sample from the masters ----------
lum = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')

lum = lum.drop_duplicates('TARGETID')
bpt = bpt.drop_duplicates('TARGETID')

print('sample labels in lum:', lum['sample'].unique())
print('sample labels in bpt:', bpt['sample'].unique())
print('class labels in bpt:', bpt['bpt_class'].unique())
print()

m = lum.merge(bpt[['TARGETID', 'bpt_class', 'log_oi_ha', 'log_oiii_hb']], on='TARGETID')

# paper cuts: log L > 24 both samples, size > 25 kpc for large
final = m[m['log_L_radio'] > 24]
is_large = final['sample'].str.lower().str.contains('large')
final = final[(~is_large) | (final['Physical_Size'] > 25)]

big = final[final['sample'].str.lower().str.contains('large')]
small = final[~final['sample'].str.lower().str.contains('large')]

print('== SAMPLE SIZES ==')
print('paper: 47 small, 30 large, 77 total')
print('computed:', len(small), 'small,', len(big), 'large,', len(final), 'total')
print()

def cls(df, name):
    return df[df['bpt_class'].str.lower().str.contains(name)]

print('== BPT CLASS COUNTS ==')
print('paper large: 26 seyfert, 4 liner, 0 sf')
print('computed large:', len(cls(big, 'sey')), 'seyfert,', len(cls(big, 'lin')), 'liner,',
      len(big) - len(cls(big, 'sey')) - len(cls(big, 'lin')), 'other')
print('paper small: 30 seyfert, 14 liner, 3 sf')
print('computed small:', len(cls(small, 'sey')), 'seyfert,', len(cls(small, 'lin')), 'liner,',
      len(small) - len(cls(small, 'sey')) - len(cls(small, 'lin')), 'other')
print()

# ---------- W80 ----------
ss = cls(small, 'sey')['w80'].dropna()
ls = cls(big, 'sey')['w80'].dropna()
sl = cls(small, 'lin')['w80'].dropna()

print('== W80, SEYFERTS ==')
print('paper: small median 688, large median 513 (old abstract said 548), KS p=0.0065, MW p=0.0026')
print('computed: small median %.0f (n=%d), large median %.0f (n=%d)' % (ss.median(), len(ss), ls.median(), len(ls)))
print('KS p = %.4f, MW p = %.4f' % (stats.ks_2samp(ss, ls).pvalue, stats.mannwhitneyu(ss, ls).pvalue))
print()
print('== W80, SMALL SEYFERT VS SMALL LINER ==')
print('paper: medians 688 and 548, KS p = 0.42')
print('computed: %.0f and %.0f, KS p = %.2f' % (ss.median(), sl.median(), stats.ks_2samp(ss, sl).pvalue))
print()
print('== EXTREME TAIL >1300 ==')
print('paper: entirely small sample')
print('small objects >1300:', (small['w80'] > 1300).sum(), '  large objects >1300:', (big['w80'] > 1300).sum())
print()

# ---------- BPT distance ----------
# Kewley 2006 Sy/LINER line in [OI] BPT: y = 1.18x + 1.30
d = (final['log_oiii_hb'] - 1.18 * final['log_oi_ha'] - 1.30) / np.sqrt(1 + 1.18**2)
d_big = d[final['sample'].str.lower().str.contains('large')]
d_small = d[~final['sample'].str.lower().str.contains('large')]

print('== BPT DISTANCE ==')
print('paper: large median 0.38, small median 0.19, MW p=0.029, AD p=0.026, KS p=0.12')
print('computed: large %.2f, small %.2f' % (d_big.median(), d_small.median()))
print('MW p = %.3f, KS p = %.2f' % (stats.mannwhitneyu(d_big, d_small).pvalue,
                                    stats.ks_2samp(d_big, d_small).pvalue))
ad = stats.anderson_ksamp([d_big.values, d_small.values])
print('AD p = %.3f' % ad.significance_level)
print()

# ---------- catalogs for NeV, Balmer, z ----------
cats = []
for path, key in [('data/OI_sample_small.csv', 'TARGETID'),
                  ('data/OI_sample_large.csv', 'TARGETID'),
                  ('data/VLASS3_2_OI_small.csv', 'TARGETID_1'),
                  ('data/VLASS3_2_OI_large.csv', 'TARGETID_1')]:
    c = pd.read_csv(path)
    if key != 'TARGETID':
        c = c.rename(columns={key: 'TARGETID'})
    cats.append(c[['TARGETID', 'Z', 'NEV_3426_FLUX', 'NEV_3426_FLUX_IVAR',
                   'HALPHA_FLUX', 'HBETA_FLUX']])
cat = pd.concat(cats).drop_duplicates('TARGETID')

f = final.merge(cat, on='TARGETID', suffixes=('', '_cat'))
print('final objects matched to catalogs:', len(f), 'of', len(final))
f['nev_err'] = 1.0 / np.sqrt(f['NEV_3426_FLUX_IVAR'])
f['nev3'] = f['NEV_3426_FLUX'] > 3 * f['nev_err']
f['nev5'] = f['NEV_3426_FLUX'] > 5 * f['nev_err']
f['balmer'] = f['HALPHA_FLUX'] / f['HBETA_FLUX']
f['islarge'] = f['sample'].str.lower().str.contains('large')

fb = f[f['islarge']]
fs = f[~f['islarge']]

print()
print('== REDSHIFT ==')
print('paper: small median 0.44, large median 0.36')
print('computed: small %.2f, large %.2f' % (fs['Z_cat'].median(), fb['Z_cat'].median()))
print()

print('== NEV DETECTION ==')
print('paper 3sig: large 60%%, small 30%%')
print('computed 3sig: large %d/%d = %.0f%%, small %d/%d = %.0f%%' %
      (fb['nev3'].sum(), len(fb), 100 * fb['nev3'].mean(),
       fs['nev3'].sum(), len(fs), 100 * fs['nev3'].mean()))
print('paper 5sig: large 57%%, small 21%%')
print('computed 5sig: large %.0f%%, small %.0f%%' % (100 * fb['nev5'].mean(), 100 * fs['nev5'].mean()))
mzb = fb[(fb['Z_cat'] > 0.30) & (fb['Z_cat'] < 0.45)]
mzs = fs[(fs['Z_cat'] > 0.30) & (fs['Z_cat'] < 0.45)]
print('paper matched z: 20 each, 60%% vs 35%%')
print('computed matched z: large n=%d %.0f%%, small n=%d %.0f%%' %
      (len(mzb), 100 * mzb['nev3'].mean(), len(mzs), 100 * mzs['nev3'].mean()))
print('paper: median NeV flux uncertainties nearly identical')
print('computed median nev_err: large %.3f, small %.3f' % (fb['nev_err'].median(), fs['nev_err'].median()))
print()

print('== BALMER DECREMENT ==')
print('paper: small median 4.00, large 3.56, MW p = 0.023')
print('computed: small %.2f, large %.2f, MW p = %.3f' %
      (fs['balmer'].median(), fb['balmer'].median(),
       stats.mannwhitneyu(fs['balmer'].dropna(), fb['balmer'].dropna()).pvalue))
lowb = fb[fb['balmer'] < 4]
lows = fs[fs['balmer'] < 4]
print('paper low-dust (<4) NeV: 84%% vs 33%%')
print('computed: large %d/%d = %.0f%%, small %d/%d = %.0f%%' %
      (lowb['nev3'].sum(), len(lowb), 100 * lowb['nev3'].mean(),
       lows['nev3'].sum(), len(lows), 100 * lows['nev3'].mean()))
print('paper large det vs nondet decrement: 3.25 vs 4.16, p = 0.01')
det = fb[fb['nev3']]['balmer'].dropna()
non = fb[~fb['nev3']]['balmer'].dropna()
print('computed: %.2f vs %.2f, MW p = %.3f' % (det.median(), non.median(),
      stats.mannwhitneyu(det, non).pvalue))
print('paper small: no difference, p = 0.26')
det = fs[fs['nev3']]['balmer'].dropna()
non = fs[~fs['nev3']]['balmer'].dropna()
print('computed: %.2f vs %.2f, MW p = %.2f' % (det.median(), non.median(),
      stats.mannwhitneyu(det, non).pvalue))
print()

# ---------- jet power (approximate, both spectral index sign conventions) ----------
print('== JET POWER Q ==')
print('paper: median log10(Q/W) = 35.6 large, 35.2 small')
alpha = final['Alpha']
L3 = 10**final['log_L_radio']
for sign, lab in [(1, 'alpha as stored'), (-1, 'alpha sign flipped')]:
    L151 = L3 * (151.0 / 3000.0)**(sign * alpha) / (4 * np.pi)
    logQ = np.log10(3e38 * (L151 / 1e28)**(6.0 / 7.0))
    qb = logQ[final['sample'].str.lower().str.contains('large')]
    qs = logQ[~final['sample'].str.lower().str.contains('large')]
    print('%s: large %.1f, small %.1f' % (lab, qb.median(), qs.median()))