import pandas as pd
import glob, os, re


#%%
#configuration to be changed if needed

folder_path = r"/media/sf_Junk.Paul/Measurements/Week 13/10cm_QCM+probe_N2_singleshots"
pattern = "*.csv"
skiprows = 11
time_col = 0
data_col = 3
t0, t1 = 0.0, 1e-3
voltage_to_ioncurrent = 1.4/400 #

#%%

#change depending on files

group_spec = """
0Pa_0T:0-0
0Pa_0.25T:1-1
0Pa_0.1T:2-2
0Pa_0.2T:3-3
0Pa_0.05T:4-4
0Pa_0.15T:5-5
0.1Pa_0T:5-24
0.1Pa_0.25T:37-52
0.1Pa_0.1T:60-90
0.1Pa_0.2T:91-112
0.1Pa_0.05T:113-144
0.1Pa_0.015T:145-171
0.05Pa_0T:172-203
0.05Pa_0.25T:204-232
0.05Pa_0.1T:233-261
0.05Pa_0.2T:262-284
0.05Pa_0.05T:285-316
0.05Pa_0.15T:317-345
0.2Pa_0T:346-377
0.2Pa_0.25T:378-389
0.2Pa_0.1T:390-409
0.2Pa_0.2T:410-421
0.2Pa_0.05T:422-449
0.2Pa_0.15T:450-469
0.3Pa_0T:470-470
0.3Pa_0.25T:471-471
0.3Pa_0.1T:472-472
0.3Pa_0.2T:473-473
0.3Pa_0.05T:474-474
0.3Pa_0.15T:475-475
0.075Pa_0T:476-476
0.075Pa_0.25T:477-477
0.075Pa_0.1T:478-478
0.075Pa_0.2T:480-480
0.075Pa_0.05T:481-481
0.075Pa_0.15T:482-482
0.025Pa_0T:483-483
0.025Pa_0.25T:484-484
0.025Pa_0.1T:485-485
0.025Pa_0.2T:486-486
0.025Pa_0.05T:488-488
0.025Pa_0.15T:490-490
"""


#%%

out_per_group = "groups_ion_current.csv"

def parse_group_spec(spec: str):
    groups = []
    for token in re.split(r"\n+", spec.strip()):
        if not token:
            continue
        label, payload = token.split(":", 1) if ":" in token else (token, token)
        idxs = set()
        for part in re.split(r"[,\s]+", payload.strip()):
            if not part: continue
            if "-" in part:
                a, b = map(int, part.split("-", 1))
                idxs.update(range(min(a,b), max(a,b)+1))
            else:
                idxs.add(int(part))
        groups.append((label.strip(), idxs))
    return groups        

#%%

def extract_index(fname: str):
    m = re.search(r"(\d+)", fname)
    return int(m.group(1)) if m else None

def average_file(path):
    df = pd.read_csv(path, header=None, skiprows=skiprows, sep=None, engine="python") 
    df = df.apply(pd.to_numeric, errors = "coerce")
    t = df.iloc[:, time_col]
    mask = t.between(t0, t1, inclusive="both")
    
    return df.loc[mask, data_col].mean()          

def sort_key(label):
    # expects e.g. "0.1Pa_0.05T"
    m = re.search(r"_(\d*\.?\d+)T", label)
    return float(m.group(1)) if m else float("inf")

#%%

def main():
    files = sorted(glob.glob(os.path.join(folder_path, pattern)))
    per_file = []
    for path in files:
        fname = os.path.basename(path)
        try:
            val = average_file(path)
            per_file.append({"file": fname, "idx": extract_index(fname), "avg": val})
        except Exception as e:
            print(f"X{fname}: {e}")
    df = pd.DataFrame(per_file)
    groups = parse_group_spec(group_spec)
    
    idx_to_label = {}
    for label, idxs in groups:
        for n in idxs:
            idx_to_label[n] = label
            
    df["group"] = df["idx"].map(idx_to_label)
    
    
    
    grouped = (df.dropna(subset=["group"])
             .groupby("group")["avg"]
             .agg(["mean","std","count"])
             .reset_index())
    grouped = grouped.sort_values(by="group", key=lambda col: col.map(sort_key))

    grouped["Ion current"] = grouped["mean"] * voltage_to_ioncurrent    

    print(grouped)
    grouped.to_csv(out_per_group, index= False)
    print("f\nSaved: {out_per_group}")
    
if __name__ == "__main__":
    main()
            






