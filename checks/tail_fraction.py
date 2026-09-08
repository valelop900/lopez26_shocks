import pandas as pd
from scipy.stats import fisher_exact

df = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
cut = df[df['log_L_radio'] > 24]

lg = cut[cut['sample'] == 'large']['w80']
sm = cut[cut['sample'] == 'small']['w80']

a, b = (sm > 1000).sum(), (sm <= 1000).sum()
c, d = (lg > 1000).sum(), (lg <= 1000).sum()
odds, p = fisher_exact([[a, b], [c, d]])

print('small %d of %d above 1000' % (a, a+b))
print('large %d of %d above 1000' % (c, c+d))
print('odds ratio %.2f  Fisher p = %.4f' % (odds, p))
