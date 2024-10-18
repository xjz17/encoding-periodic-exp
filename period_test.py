import os
import pandas as pd
from algorithm.period_new_encode import get_period_segment
from algorithm.period_new_encode import get_period_sample

RESULT_PATH = "result.bin"


files = os.listdir("data")
for file in files:
    file_pull = os.path.join("data", file)
    df = pd.read_csv(file_pull)
    data = df["value"].tolist()
    print(file)
    print(f"segment: {get_period_segment(data)}")
    print(f"sample: {get_period_sample(data)}")
