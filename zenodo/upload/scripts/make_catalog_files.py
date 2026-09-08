import pandas as pd

keep = ['TARGETID', 'Name', 'RA', 'DEC', 'Z', 'Flux', 'E_Flux', 'LAS',
        'Physical_Size', 'Alpha', 'E_Alpha', 'D_L',
        'NEV_3426_FLUX', 'NEV_3426_FLUX_IVAR',
        'OI_6300_FLUX', 'OI_6300_FLUX_IVAR',
        'OIII_5007_FLUX', 'OIII_5007_FLUX_IVAR',
        'HALPHA_FLUX', 'HALPHA_FLUX_IVAR',
        'HBETA_FLUX', 'HBETA_FLUX_IVAR',
        'HALPHA_BROAD_FLUX', 'HALPHA_BROAD_FLUX_IVAR']

files = ['data/OI_sample_small.csv', 'data/OI_sample_large.csv',
         'data/VLASS3_2_OI_small.csv', 'data/VLASS3_2_OI_large.csv']
cat = []
renames = {'TARGETID_1': 'TARGETID', 'RA_1': 'RA', 'DEC_1': 'DEC',
           'Physical_size': 'Physical_Size'}
for f in files:
    d = pd.read_csv(f)
    d = d.rename(columns={k: v for k, v in renames.items() if k in d.columns})
    cat.append(d)
cat = pd.concat(cat, ignore_index=True).drop_duplicates('TARGETID')

w80 = pd.concat([pd.read_csv('notes/2026-07-13_resolution_w80.csv'),
                 pd.read_csv('notes/2026-07-22_w80_new_large.csv'),
                 pd.read_csv('notes/2026-07-31_w80_new_small24.csv')],
                ignore_index=True).drop_duplicates('TARGETID')

bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
lum = pd.read_csv('notes/2026-07-28_luminosity_check.csv').drop_duplicates('TARGETID')

m = 1.18
b = 1.30
bpt['sl_distance'] = (bpt['log_oiii_hb'] - m*bpt['log_oi_ha'] - b) / (1 + m**2)**0.5

out = bpt[['TARGETID', 'sample', 'bpt_class', 'sl_distance']]
out = out.merge(lum[['TARGETID', 'log_L_radio']], on='TARGETID')
out = out.merge(w80[['TARGETID', 'w80']], on='TARGETID')
out = out.merge(cat[keep], on='TARGETID')
print('rows:', len(out))

cols = ['TARGETID', 'sample', 'Name', 'RA', 'DEC', 'Z', 'Flux', 'E_Flux', 'LAS',
        'Physical_Size', 'Alpha', 'E_Alpha', 'D_L', 'log_L_radio', 'w80',
        'bpt_class', 'sl_distance'] + keep[12:]
out = out[cols]

for s in ['small', 'large']:
    sub = out[out['sample'] == s]
    sub.to_csv('data/catalog_%s.csv' % s, index=False)
    print(s, len(sub), 'rows ->', 'data/catalog_%s.csv' % s)