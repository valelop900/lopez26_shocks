import numpy as np
from sparcl.client import SparclClient

new_ids = [39627887631929650,
           39627887787116738,
           39627936101302939,
           39627791519452623,
           39628051121705326,
           39627775098750148,
           39627726847476452,
           39627877989223494]

client = SparclClient()
inc = ['specid', 'flux', 'wavelength', 'specprimary', 'targetid']

for tid in new_ids:
    res = client.retrieve_by_specid(specid_list=[tid], include=inc,
                                    dataset_list=['DESI-DR1'])
    records = res.records
    if len(records) == 0:
        print(tid, 'NO SPECTRUM FOUND')
        continue
    # pick the primary spectrum
    primary = [r for r in records if r.specprimary][0]
    lam = primary.wavelength
    flam = primary.flux
    f = open('data/spectra/' + str(tid) + '_desispec.csv', 'w')
    f.write('Lambda,FLambda17\n')
    for i in range(len(lam)):
        f.write(str(lam[i]) + ',' + str(flam[i]) + '\n')
    f.close()
    print(tid, 'saved,', len(lam), 'rows')