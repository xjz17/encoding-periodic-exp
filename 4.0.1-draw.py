import os
import pandas as pd
import matplotlib.pyplot as plt

INPUT_PATH = "data_labeled"
files = os.listdir(INPUT_PATH)

OUTPUT_PATH = "fig_labeled"
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

for file in files:
    df = pd.read_csv(os.path.join(INPUT_PATH, file))
    data = df["value"].tolist()
    label = df["label"].tolist()
    plt.plot(data)
    for i in range(len(label)):
        if label[i] == 1:
            plt.scatter(i, data[i], c="red")
    plt.savefig(os.path.join(OUTPUT_PATH, file.replace("csv", "png")))
    plt.clf()
