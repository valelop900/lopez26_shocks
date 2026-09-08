import pandas as pd
import numpy as np
from scipy.stats import ks_2samp, mannwhitneyu

print('================ CHECK 1: merge integrity ================')
large_old = pd.read_csv('data/OI_sample_large.csv')
small = pd.read_csv('data/OI_sample_small.csv')
large_new = pd.read_csv('data/VLASS3_2_OI_large.csv')
large_new = large_new.rename(columns={'TARGETID_1': 'TARGETID'})

# any object appearing in more than one catalog would double-count in the merge
ids_lo = set(large_old['TARGETID'])
ids_ln = set(large_new['TARGETID'])
ids_sm = set(small['TARGETID'])
print('old large vs new large overlap:', len(ids_lo & ids_ln))
print('large vs small overlap:', len((ids_lo | ids_ln) & ids_sm))
print('duplicate TARGETID inside old large:', large_old['TARGETID'].duplicated().sum())
print('duplicate TARGETID inside new large:', large_new['TARGETID'].duplicated().sum())
print('duplicate TARGETID inside small:', small['TARGETID'].duplicated().sum())

w1 = pd.read_csv('notes/2026-07-13_resolution_w80.csv')
w2 = pd.read_csv('notes/2026-07-22_w80_new_large.csv')
w80 = pd.concat([w1[['TARGETID', 'sample', 'w80']], w2[['TARGETID', 'sample', 'w80']]], ignore_index=True)
print('duplicate TARGETID in combined w80:', w80['TARGETID'].duplicated().sum())

# does the sample label in the w80 files agree with which catalog the object came from
lab = []
for t, s in zip(w80['TARGETID'], w80['sample']):
    true = 'large' if (t in ids_lo or t in ids_ln) else ('small' if t in ids_sm else 'missing')
    lab.append(true == s)
print('sample label mismatches:', len(lab) - sum(lab))
print()

print('================ CHECK 2: is D_L consistent with Z ================')
# recompute luminosity distance ourselves, flat LCDM H0=70 Om=0.3, and compare
def dl_mpc(z, n=2000):
    zz = np.linspace(0, z, n)
    ez = np.sqrt(0.3 * (1 + zz)**3 + 0.7)
    dc = np.trapz(1 / ez, zz) * 299792.458 / 70.0
    return (1 + z) * dc

df = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
df['D_L_check'] = [dl_mpc(z) for z in df['Z']]
df['dl_ratio'] = df['D_L'] / df['D_L_check']
print('D_L catalog / D_L recomputed: min %.3f median %.3f max %.3f' %
      (df['dl_ratio'].min(), df['dl_ratio'].median(), df['dl_ratio'].max()))
print('(should be within a few percent of 1.0, offset means different cosmology or units)')
print()

print('================ CHECK 3: Alpha and the K-correction ================')
print('Alpha: min %.2f median %.2f max %.2f' % (df['Alpha'].min(), df['Alpha'].median(), df['Alpha'].max()))
print('objects with Alpha > 0:', (df['Alpha'] > 0).sum(), ' Alpha < -1.5:', (df['Alpha'] < -1.5).sum())
# redo radio luminosity with a fixed alpha=-0.7 to see if odd alphas move the answer
dl_m = df['D_L'] * 3.086e22
df['log_L_radio_fixedalpha'] = np.log10(4 * np.pi * dl_m**2 * df['Flux'] * 1e-29 * (1 + df['Z'])**(-(1 - 0.7)))
lg = df[df['sample'] == 'large']
sm = df[df['sample'] == 'small']
print('median log_L_radio, per-object alpha: large %.3f small %.3f' %
      (lg['log_L_radio'].median(), sm['log_L_radio'].median()))
print('median log_L_radio, fixed alpha=-0.7: large %.3f small %.3f' %
      (lg['log_L_radio_fixedalpha'].median(), sm['log_L_radio_fixedalpha'].median()))
print('(if these disagree a lot, weird Alpha values matter)')
print()

print('================ CHECK 4: OIII flux quality ================')
z1 = df[df['OIII_5007_FLUX'] <= 0]
print('objects with OIII flux <= 0:', len(z1), list(z1['TARGETID']))
# pull the IVAR from the source catalogs to see if faint fluxes are even significant
cat_all = pd.concat([large_old[['TARGETID', 'OIII_5007_FLUX', 'OIII_5007_FLUX_IVAR']],
                     large_new[['TARGETID', 'OIII_5007_FLUX', 'OIII_5007_FLUX_IVAR']],
                     small[['TARGETID', 'OIII_5007_FLUX', 'OIII_5007_FLUX_IVAR']]], ignore_index=True)
cat_all['oiii_snr'] = cat_all['OIII_5007_FLUX'] * np.sqrt(cat_all['OIII_5007_FLUX_IVAR'])
m = df.merge(cat_all[['TARGETID', 'oiii_snr']], on='TARGETID', how='left')
print('objects with catalog OIII SNR < 3:', (m['oiii_snr'] < 3).sum())
print(m[m['oiii_snr'] < 3][['TARGETID', 'sample', 'oiii_snr']].to_string(index=False))
print()

print('================ CHECK 5: w80 values sanity ================')
print('w80: min %.0f median %.0f max %.0f' % (df['w80'].min(), df['w80'].median(), df['w80'].max()))
print('w80 < 200 km/s (suspiciously narrow):', (df['w80'] < 200).sum())
print('w80 > 2500 km/s (suspiciously broad):', (df['w80'] > 2500).sum())
# w80 for a single gaussian is 2.563 sigma, check ours are not below the narrow component alone
w_full = pd.concat([w1, w2], ignore_index=True)
w_full['w80_min_expected'] = 2.563 * w_full['oiii_narrow_sigma_kms']
bad = w_full[w_full['w80'] < 0.9 * w_full['w80_min_expected']]
print('objects where w80 < 90% of 2.563*narrow_sigma (should be ~none):', len(bad))
print()

print('================ CHECK 6: Physical_Size vs LAS and Z ================')
# size should equal LAS(arcsec) times angular scale at z, check the ratio is one constant
cat_sz = pd.concat([large_old[['TARGETID', 'LAS']], large_new[['TARGETID', 'LAS']],
                    small[['TARGETID', 'LAS']]], ignore_index=True)
m2 = df.merge(cat_sz, on='TARGETID', how='left')
da = m2['D_L'] / (1 + m2['Z'])**2                      # angular diameter distance, Mpc
scale = da * 1000 * np.pi / (180 * 3600)               # kpc per arcsec
m2['size_check'] = m2['LAS'] * scale
m2['size_ratio'] = m2['Physical_Size'] / m2['size_check']
print('Physical_Size / (LAS * scale): min %.3f median %.3f max %.3f' %
      (m2['size_ratio'].min(), m2['size_ratio'].median(), m2['size_ratio'].max()))
print('(a constant near 1 means LAS is arcsec; a constant like 60 means arcmin; scatter means trouble)')
print()

print('================ CHECK 7: real luminosity matching, nearest-neighbor pairs ================')
# range-trimming did not equalize the distributions, so pair each small with closest large
d2 = df[np.isfinite(df['log_L_oiii'])]
lg2 = d2[d2['sample'] == 'large'].reset_index(drop=True)
sm2 = d2[d2['sample'] == 'small'].reset_index(drop=True)
for c in ['log_L_radio', 'log_L_oiii']:
    used = set()
    pairs = []
    for i, row in sm2.iterrows():
        diffs = (lg2[c] - row[c]).abs()
        diffs[list(used)] = np.inf
        j = diffs.idxmin()
        if diffs[j] < 0.3:                              # only accept pairs within 0.3 dex
            used.add(j)
            pairs.append((row['w80'], lg2.loc[j, 'w80'], row[c], lg2.loc[j, c]))
    p = pd.DataFrame(pairs, columns=['w80_small', 'w80_large', 'lum_small', 'lum_large'])
    print(c, ': matched pairs within 0.3 dex:', len(p))
    if len(p) > 5:
        print('  median lum small %.3f large %.3f (now these should be close)' %
              (p['lum_small'].median(), p['lum_large'].median()))
        print('  median w80 small %.0f large %.0f' % (p['w80_small'].median(), p['w80_large'].median()))
        stat, pv = mannwhitneyu(p['w80_small'], p['w80_large'], alternative='greater')
        print('  Mann-Whitney p (small broader than large): %.4f' % pv)
    print()
