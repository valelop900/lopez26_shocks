import pandas as pd

large = pd.read_csv("/Users/valeria/Desktop/nrao_project/data/OI_sample_large.csv")
small = pd.read_csv("/Users/valeria/Desktop/nrao_project/data/OI_sample_small.csv")

both = pd.concat([large, small])

# keep just the TARGETID and redshift
table = both[["TARGETID", "Z"]].drop_duplicates()

out = "/Users/valeria/Desktop/nrao_project/notes/targetid_redshift.csv"
table.to_csv(out, index=False)

print("saved", len(table), "rows to", out)