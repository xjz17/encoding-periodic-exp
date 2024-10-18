import os
import numpy as np
import pandas as pd

df = pd.read_csv(os.path.join("origin", "gps", "anon_gps_tracks_with_dive.csv"))

dfs = [(key, group) for key, group in df.groupby("bird")]
for key, df in dfs:
    data = pd.DataFrame(data={"value": (df["lat"] * 10**6).astype(np.int64)})
    data.to_csv(os.path.join("data", f"gps_{key}.csv"), index=False)
