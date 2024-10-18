import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

FONT_SIZE = 10


def dataset_showname(name: str):
    if name == "dianwang":
        return "grid"
    elif name == "guoshou":
        return "safe"
    elif name == "liantong":
        return "mobile"
    elif name == "yinlian":
        return "bank"
    return name


INPUT_PATH = os.path.join("exp_result", "abnormal_detect_draw.csv")
RESULT_PATH = os.path.join("exp_result", "abnormal_detect.png")
RESULT_PATH_EPS = os.path.join("exp_result", "abnormal_detect.eps")

df = pd.read_csv(INPUT_PATH)
type_array = df["type"].drop_duplicates().to_numpy()
dataset_array = df["dataset"].drop_duplicates().apply(dataset_showname).to_numpy()
# print(type_array)

bar_width = 0.8 / len(type_array)
index_offset = np.arange(len(dataset_array))

fig, axs = plt.subplots(1, 2, figsize=(6.25, 6.25 * 3.5 / 8))

for idx, type in enumerate(type_array):
    subset = df[df["type"] == type]
    bar_x = index_offset + bar_width * idx
    axs[0].bar(
        bar_x,
        subset["score"],
        width=bar_width,
        label=type,
    )

axs[0].set_title("(a) F1-score of methods", fontsize=FONT_SIZE)
axs[0].set_xlabel("Dataset", fontsize=FONT_SIZE)
axs[0].set_ylabel("F1-score", fontsize=FONT_SIZE)

axs[0].set_xticks(index_offset + bar_width * (len(type_array) - 1) / 2)
axs[0].set_xticklabels(dataset_array, rotation=0, fontsize=FONT_SIZE)

fig.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, 1),
    ncol=len(type_array),
    fontsize=FONT_SIZE,
)


for idx, type in enumerate(type_array):
    subset = df[df["type"] == type]
    bar_x = index_offset + bar_width * idx
    axs[1].bar(
        bar_x,
        subset["time"],
        width=bar_width,
        label=type,
    )

axs[1].set_title("(b) Time cost of methods", fontsize=FONT_SIZE)
axs[1].set_xlabel("Dataset", fontsize=FONT_SIZE)
axs[1].set_ylabel("Time cost(s)", fontsize=FONT_SIZE)
axs[1].set_yscale("log")

axs[1].set_xticks(index_offset + bar_width * (len(type_array) - 1) / 2)
axs[1].set_xticklabels(dataset_array, rotation=0, fontsize=FONT_SIZE)

plt.tight_layout()
plt.subplots_adjust(top=0.75)
plt.savefig(RESULT_PATH)
plt.savefig(RESULT_PATH_EPS)
