import pandas as pd

df = pd.read_csv("data/small_new_cut24.csv")
out = df[["TARGETID_1", "Z"]].rename(columns={"TARGETID_1": "TARGETID"})
out.to_csv("notes/2026-07-31_targetid_redshift_new24.csv", index=False)

print(len(out))
print(list(out["TARGETID"]))
