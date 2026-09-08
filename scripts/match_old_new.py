import pandas as pd
import numpy as np

old = pd.read_csv('data/OI_sample_large.csv')
new = pd.read_csv('data/VLASS3_2_OI_large.csv')

# separation in arcsec between each old object and its nearest new object
for i in range(len(old)):
    dra = (new['RA_1'] - old['RA'][i]) * np.cos(np.radians(old['DEC'][i]))
    ddec = new['DEC_1'] - old['DEC'][i]
    sep = np.sqrt(dra**2 + ddec**2) * 3600
    print(old['TARGETID'][i], round(sep.min(), 1))
