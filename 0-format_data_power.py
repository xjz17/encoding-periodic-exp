import os
import numpy as np
import pandas as pd

if not os.path.exists("data"):
    os.makedirs("data")

DATA_LENGTH = 10**4

with open(os.path.join("origin", "power", "household_power_consumption.txt"), "r") as f:
    lines = f.readlines()

meta = lines[0]
data = lines[1:]

current_index = 0

meta_name = meta.split(";")[2]
for index in range((len(data) + DATA_LENGTH - 1) // DATA_LENGTH):
    current_data = data[current_index : min(current_index + DATA_LENGTH, len(data))]
    current_index += min(current_index + DATA_LENGTH, len(data)) - current_index
    current_result = []
    for line in current_data:
        s = line.split(";")[2]
        if s == "?":
            s = "0"
        current_result.append(int(float(s) * 10**3))
    df = pd.DataFrame(data={"value": current_result})
    df.to_csv(os.path.join("data", f"power_{meta_name}_{index}.csv"), index=False)
