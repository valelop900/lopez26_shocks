import pandas as pd

df = pd.read_csv('data/VLASS3_2_OI_small.csv')
print(df['Physical_size'].describe())
