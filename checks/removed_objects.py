import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

df = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
sm = df[df['sample'] == 'small']
kept = sm[sm['log_L_radio'] > 24]
gone = sm[sm['log_L_radio'] <= 24]

print('small kept', len(kept), 'median w80 %.1f' % kept['w80'].median())
print('small removed', len(gone), 'median w80 %.1f' % gone['w80'].median())
print('KS p between kept and removed: %.4f' % ks_2samp(kept['w80'], gone['w80']).pvalue)
print()
print('corr(log_L_radio, w80) within small sample: %.3f'
      % np.corrcoef(sm['log_L_radio'], sm['w80'])[0,1])
