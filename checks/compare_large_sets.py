import pandas as pd

bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
lum = pd.read_csv('notes/2026-07-28_luminosity_check.csv')[['TARGETID', 'log_L_radio', 'Physical_Size']]

# monday's chain: inner merge with lum, logL cut, size cut
mon = bpt.merge(lum, on='TARGETID')
mon = mon[mon['log_L_radio'] > 24]
mon = mon[(mon['sample'] == 'small') | (mon['Physical_Size'] > 25)]
mon_lg = set(mon[(mon['sample'] == 'large') & (mon['bpt_class'] == 'seyfert')]['TARGETID'])

# today's chain: trust lumcut_v2, size cut only
tod = bpt.merge(lum, on='TARGETID', how='left')
tod = tod[(tod['sample'] == 'small') | (tod['Physical_Size'] > 25)]
tod_lg = set(tod[(tod['sample'] == 'large') & (tod['bpt_class'] == 'seyfert')]['TARGETID'])

print('monday large Sy:', len(mon_lg))
print('today large Sy:', len(tod_lg))
print('in today only:', sorted(tod_lg - mon_lg))
print('in monday only:', sorted(mon_lg - tod_lg))