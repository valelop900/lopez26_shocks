import pandas as pd
from scipy.stats import anderson_ksamp, ks_2samp, mannwhitneyu

df = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
cut = df[df['log_L_radio'] > 24]

lg = cut[cut['sample'] == 'large']['w80'].values
sm = cut[cut['sample'] == 'small']['w80'].values

ad = anderson_ksamp([lg, sm], variant='midrank')
print('W80 after cut:')
print('AD p = %.4f' % ad.pvalue)
print('KS p = %.4f' % ks_2samp(lg, sm).pvalue)
print('MW p = %.4f' % mannwhitneyu(lg, sm).pvalue)
