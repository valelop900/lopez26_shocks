import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

LARGE_COLOR = 'black'
SMALL_COLOR = '#5B2C6F'
MARKERS = {'seyfert': ('o', 45), 'liner': ('*', 110), 'sf': ('^', 55)}

m = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
m = m.merge(bpt[['TARGETID', 'bpt_class']], on='TARGETID')
m = m[m['log_L_radio'] > 24]
m = m[(m['sample'] == 'small') | (m['Physical_Size'] > 25)]
print('sample:', len(m))

c1 = pd.read_csv('data/OI_sample_small.csv')
c2 = pd.read_csv('data/OI_sample_large.csv')
c3 = pd.read_csv('data/VLASS3_2_OI_small.csv').rename(columns={'TARGETID_1': 'TARGETID'})
c4 = pd.read_csv('data/VLASS3_2_OI_large.csv').rename(columns={'TARGETID_1': 'TARGETID'})
cat = pd.concat([c1, c2, c3, c4], ignore_index=True).drop_duplicates('TARGETID')
cols = ['TARGETID', 'NEV_3426_FLUX', 'NEV_3426_FLUX_IVAR', 'HBETA_FLUX']
m = m.merge(cat[cols], on='TARGETID', how='left')
print('with NeV column:', m['NEV_3426_FLUX'].notna().sum(), 'of', len(m))

# keep only NeV detections at >3 sigma with positive flux
m['nev_snr'] = m['NEV_3426_FLUX'] * np.sqrt(m['NEV_3426_FLUX_IVAR'])
det = m[(m['nev_snr'] > 3) & (m['NEV_3426_FLUX'] > 0) & (m['HBETA_FLUX'] > 0)].copy()
print('NeV detected (>3 sigma):')
print(det.groupby(['sample', 'bpt_class']).size())

det['log_nev_hb'] = np.log10(det['NEV_3426_FLUX'] / det['HBETA_FLUX'])
det['log_oiii_hb'] = np.log10(det['OIII_5007_FLUX'] / det['HBETA_FLUX'])

plt.figure(figsize=(8, 6))
for s in ['large', 'small']:
    for cl in ['seyfert', 'liner', 'sf']:
        sub = det[(det['sample'] == s) & (det['bpt_class'] == cl)]
        if not len(sub):
            continue
        mk, ms = MARKERS[cl]
        if s == 'large':
            plt.scatter(sub['log_nev_hb'], sub['log_oiii_hb'], marker=mk, s=ms,
                        facecolors=LARGE_COLOR, edgecolors=LARGE_COLOR,
                        label='large %s (n=%d)' % (cl, len(sub)))
        else:
            plt.scatter(sub['log_nev_hb'], sub['log_oiii_hb'], marker=mk, s=ms,
                        facecolors='none', edgecolors=SMALL_COLOR, linewidths=1.3,
                        label='small %s (n=%d)' % (cl, len(sub)))

plt.xlabel('log [NeV]3426 / H$\\beta$')
plt.ylabel('log [OIII]5007 / H$\\beta$')
plt.legend(fontsize=8, loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.tight_layout()
plt.savefig('plots/2026-08-12_oiii_nev.png', dpi=150)
plt.savefig('plots/fig_oiii_nev.pdf')
print('saved')