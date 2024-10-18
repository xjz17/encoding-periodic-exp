import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


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


INPUT_PATH = os.path.join("exp_result", "exp_compare_draw.csv")
RESULT_PATH = os.path.join("exp_result", "compare.png")
RESULT_PATH_EPS = os.path.join("exp_result", "compare.eps")

df = pd.read_csv(INPUT_PATH)
type_array = ["previous", "average"]
dataset_array = [
    "temperature",
    "volt",
    "power",
    "gps",
    "dianwang",
    "guoshou",
    "liantong",
    "yinlian",
]
# print(type_array)

bar_width = 0.8 / len(type_array)
index_offset = np.arange(len(dataset_array))

fig, ax = plt.subplots(1, 1, figsize=(6, 3.5))

for idx, type in enumerate(type_array):
    subset = df[df["algorithm"] == type]
    bar_x = index_offset + bar_width * idx
    ax.bar(
        bar_x,
        subset["compress_ratio"],
        width=bar_width,
        label=type,
    )

# ax.set_title("(a) MSE loss of different method")
ax.set_xlabel("Dataset")
ax.set_ylabel("Compression Ratio")
# ax.set_yscale("log")

ax.set_xticks(index_offset + bar_width * (len(type_array) - 1) / 2)
ax.set_xticklabels(
    (np.vectorize(dataset_showname))(np.asarray(dataset_array)), rotation=0
)

fig.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, 1),
    ncol=len(type_array),
)


# for idx, type in enumerate(type_array):
#     subset = df[df["type"] == type]
#     bar_x = index_offset + bar_width * idx
#     axs[1].bar(
#         bar_x,
#         subset["time"],
#         width=bar_width,
#         label=type,
#     )

# axs[1].set_title("(b) Time cost of different method")
# axs[1].set_xlabel("Database")
# axs[1].set_ylabel("Time cost(s)")
# axs[1].set_yscale("log")

# axs[1].set_xticks(
#     index_offset + bar_width * (len(type_array) - 1) / 2
# )
# axs[1].set_xticklabels(dataset_array, rotation=0)

plt.tight_layout()
plt.subplots_adjust(top=0.9)
# plt.show()
plt.savefig(RESULT_PATH)
plt.savefig(RESULT_PATH_EPS)
