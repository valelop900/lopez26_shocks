import pandas as pd

# swaps in the free centroid W80 from oiii_profiles.py for one object, everywhere it is stored

tid = 39628159028563219
ref = pd.read_csv('notes/2026-09-13_oiii_profiles_highw80.csv')
new = ref.loc[ref['TARGETID'] == tid, 'w80_refit'].iloc[0]

files = ['notes/2026-07-31_w80_new_small24.csv',
         'data/catalog_small.csv',
         'zenodo/upload/catalog_lopez_lacy_2026.csv']

for f in files:
    d = pd.read_csv(f)
    i = d.index[d['TARGETID'] == tid]
    old = d.loc[i, 'w80'].iloc[0]
    # release table keeps one decimal
    d.loc[i, 'w80'] = round(new, 1) if 'zenodo' in f else new
    d.to_csv(f, index=False)
    print('%-45s %s: %.1f -> %.1f' % (f, tid, old, d.loc[i, 'w80'].iloc[0]))
