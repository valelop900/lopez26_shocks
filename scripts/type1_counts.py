import pandas as pd

files = ['data/OI_sample_small.csv', 'data/OI_sample_large.csv',
         'data/VLASS3_2_OI_small.csv', 'data/VLASS3_2_OI_large.csv']

cat = []
for f in files:
    d = pd.read_csv(f)
    if 'TARGETID_1' in d.columns:
        d = d.rename(columns={'TARGETID_1': 'TARGETID'})
    cat.append(d)
cat = pd.concat(cat, ignore_index=True).drop_duplicates('TARGETID')

m = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
m = m.merge(bpt[['TARGETID', 'bpt_class']], on='TARGETID')
m = m[m['log_L_radio'] > 24]
m = m[(m['sample'] == 'small') | (m['Physical_Size'] > 25)]
print('sample size:', len(m), '| small:', (m['sample']=='small').sum(),
      'large:', (m['sample']=='large').sum())

m = m.merge(cat[['TARGETID', 'HALPHA_BROAD_FLUX']], on='TARGETID')
print('matched to catalog:', len(m))
m['type1'] = m['HALPHA_BROAD_FLUX'].fillna(0) > 0

for s in ['small', 'large']:
    sub = m[m['sample'] == s]
    print(s, 'type1:', sub['type1'].sum(), 'of', len(sub))