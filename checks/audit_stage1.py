import glob
import pandas as pd

# list every csv in notes/ and data/ with its columns and row count
for path in sorted(glob.glob('notes/*.csv') + glob.glob('data/*.csv')):
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(path, 'FAILED TO READ:', e)
        continue
    print(path, '  rows:', len(df))
    print('   ', list(df.columns))
    print()