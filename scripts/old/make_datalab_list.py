# reads the good targetids and prints them as a python list to paste into Data Lab

f = open("/Users/valeria/Desktop/nrao_project/notes/2026-07-07_good_targetids.txt")
ids = [line.strip() for line in f if line.strip()]
f.close()

print("good_ids = [")
for t in ids:
    print("    " + t + ",")
print("]")
print()
print("count:", len(ids))