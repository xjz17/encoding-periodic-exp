import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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


def draw(name: str, column_name: str, log_scale=False):
    df = pd.read_csv(os.path.join("exp_result", f"{name}.csv"))
    custom_order = {
        "temperature": 0,
        "volt": 1,
        "power": 2,
        "gps": 3,
        "dianwang": 4,
        "guoshou": 5,
        "liantong": 6,
        "yinlian": 7,
    }
    df["order"] = df["dataset"].map(custom_order)
    df = df.sort_values(by="order").reset_index()
    del df["order"]
    compression_algorithms = [
        "period",
        "ts_2diff",
        "sprintz",
        "gorilla",
        "rle",
        "chimp",
        "buff",
        "hire",
    ]

    show_name = {
        "period": "PERIOD",
        "ts_2diff": "TS_2DIFF",
        "gorilla": "GORILLA",
        "rle": "RLE",
        "plain": "PLAIN",
        "buff": "BUFF",
        "chimp": "CHIMP",
        "sprintz": "SPRINTZ",
        "hire": "HIRE",
    }
    df_melted = pd.melt(
        df,
        id_vars="dataset",
        var_name="Compression Algorithm",
        value_name=column_name,
    )

    bar_width = 0.8 / len(compression_algorithms)
    index_offset = np.arange(len(df["dataset"]))

    fig, ax = plt.subplots(figsize=(6.25, 6.25 * 0.625))

    for idx, algorithm in enumerate(compression_algorithms):
        subset = df_melted[df_melted["Compression Algorithm"] == algorithm]
        bar_x = index_offset + bar_width * idx
        ax.bar(
            bar_x,
            subset[column_name],
            width=bar_width,
            label=show_name[algorithm],
        )

    if log_scale:
        ax.set_yscale("log")
    ax.set_xlabel("Dataset", fontsize=FONT_SIZE)
    ax.set_ylabel(column_name, fontsize=FONT_SIZE)
    # ax.set_title("Compression Performance Across Databases", fontsize=FONT_SIZE)
    ax.set_xticks(index_offset + bar_width * (len(compression_algorithms) - 1) / 2)
    ax.set_xticklabels(
        df["dataset"].apply(dataset_showname).unique(), rotation=0, fontsize=FONT_SIZE
    )
    ax.legend(
        # title="Compression Algorithms",
        loc="upper center",
        bbox_to_anchor=(0.5, 1.25),
        ncol=4,
        fontsize=FONT_SIZE,
    )

    plt.tight_layout()
    plt.savefig(os.path.join("exp_result", f"{name}.png"))
    plt.savefig(os.path.join("exp_result", f"{name}.eps"))
    plt.clf()
    # plt.savefig("tmp/fig/result0329.png")


draw("compress_ratio", "Compression Ratio")
draw("encoding_time", "Encoding Time(s)", log_scale=True)
draw("decoding_time", "Decoding Time(s)", log_scale=True)
