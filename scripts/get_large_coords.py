import pandas as pd

df = pd.read_csv("data/QC_new_large.csv")
print(df.columns.tolist())
print(df[df["TARGETID"] == 39628216905763376])