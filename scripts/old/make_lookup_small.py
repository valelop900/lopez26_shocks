import pandas as pd

df = pd.read_csv("/Users/valeria/Desktop/nrao_project/data/OI_sample_small.csv")

for i in range(len(df)):
    row = i + 1
    name = df["Name"][i]
    ra = df["RA"][i]
    dec = df["DEC"][i]
    tid = df["TARGETID"][i]
    print(row, name, ra, dec, tid)