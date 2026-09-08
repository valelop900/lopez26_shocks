import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

LARGE_COLOR = 'black'
SMALL_COLOR = '#5B2C6F'

m = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
m = m.merge(bpt[['TARGETID', 'bpt_class']], on='TARGETID')
m = m[m['log_L_radio'] > 24]
m = m[(m['sample'] == 'small') | (m['Physical_Size'] > 25)]

c1 = pd.read_csv('data/OI_sample_small.csv')
c2 = pd.read_csv('data/OI_sample_large.csv')
c3 = pd.read_csv('data/VLASS3_2_OI_small.csv').rename(columns={'TARGETID_1': 'TARGETID'})
c4 = pd.read_csv('data/VLASS3_2_OI_large.csv').rename(columns={'TARGETID_1': 'TARGETID'})
cat = pd.concat([c1, c2, c3, c4], ignore_index=True).drop_duplicates('TARGETID')
m = m.merge(cat[['TARGETID', 'HALPHA_FLUX', 'HBETA_FLUX',
                 'NEV_3426_FLUX', 'NEV_3426_FLUX_IVAR']], on='TARGETID')

m = m[(m['HALPHA_FLUX'] > 0) & (m['HBETA_FLUX'] > 0)]
m['balmer'] = m['HALPHA_FLUX'] / m['HBETA_FLUX']
m['nev_snr'] = m['NEV_3426_FLUX'] * np.sqrt(m['NEV_3426_FLUX_IVAR'])
print('objects with both Balmer lines:', len(m))

lg = m[m['sample'] == 'large']['balmer']
sm = m[m['sample'] == 'small']['balmer']
print('median Ha/Hb: large %.2f (n=%d)  small %.2f (n=%d)' % (lg.median(), len(lg), sm.median(), len(sm)))
print('MW p =', round(mannwhitneyu(lg, sm).pvalue, 4))

# does dust track the NeV non-detections?
print()
print('median Ha/Hb by NeV detection:')
for s in ['large', 'small']:
    sub = m[m['sample'] == s]
    d = sub[sub['nev_snr'] > 3]['balmer']
    n = sub[sub['nev_snr'] <= 3]['balmer']
    print('  %s: detected %.2f (n=%d), not detected %.2f (n=%d)'
          % (s, d.median(), len(d), n.median(), len(n)))

bins = np.arange(0, 12, 0.75)
plt.figure(figsize=(7, 5))
plt.hist(lg, bins=bins, weights=np.ones(len(lg))/len(lg), histtype='stepfilled',
         facecolor='0.8', edgecolor=LARGE_COLOR, linewidth=1.3,
         label='large (>25 kpc), n=%d' % len(lg))
plt.hist(sm, bins=bins, weights=np.ones(len(sm))/len(sm), histtype='stepfilled',
         facecolor='none', edgecolor=SMALL_COLOR, hatch='\\\\\\', linewidth=1.3,
         label='small (10-15 kpc), n=%d' % len(sm))s
plt.axvline(3.5, color='k', ls='--', lw=0.8)
plt.axvline(4.0, color='k', ls='--', lw=0.8)
plt.xlabel(r'H$\alpha$ / H$\beta$')
plt.ylabel('fraction of sample')
plt.legend()
plt.tight_layout()
plt.savefig('plots/fig_balmer.pdf')
plt.savefig('plots/2026-08-21_balmer.png', dpi=150)
print('saved plots/fig_balmer.pdf')