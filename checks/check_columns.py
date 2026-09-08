import glob
import pandas as pd

for f in sorted(glob.glob('notes/*.csv')) + sorted(glob.glob('data/*.csv')):
    df = pd.read_csv(f)
    print(f, len(df))
    print(df.columns.tolist())
    print()
