import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml
import os
from mylib.period import get_period

FONT_SIZE = 11


def quantize(array: np.ndarray, beta):
    array = np.copy(array)
    count = 0
    for i in range(len(array)):
        count += int(array[i].real / beta).bit_length()
        count += int(array[i].imag / beta).bit_length()
        array[i] = (int(array[i].real / beta) * beta) + 1j * (
            int(array[i].imag / beta) * beta
        )
    return array, count


if not os.path.exists("result"):
    os.makedirs("result")

with open("toys.yml", "r", encoding="utf-8") as f:
    toys = yaml.full_load(f)

file = toys["period-complementation"]

data = pd.read_csv(os.path.join("data", f"{file['name']}.csv"))
data = data["value"].to_numpy()
p = get_period(data)
# print(p)

FIGURE_SIZE = (7, 7.5)
fig = plt.figure(figsize=FIGURE_SIZE)
axs = fig.subplots(nrows=3, ncols=2)

data_not_full = data[: int(p * file["not_full_period"])]

axs[0, 0].plot(data_not_full)
axs[0, 0].set_title("(a) Data with incomplete periods", fontsize=FONT_SIZE)

dataf_not_full = np.abs(np.fft.fft(data_not_full))[: file["frequency_length"]]

for i in range(len(dataf_not_full)):
    axs[1, 0].vlines(x=i, ymin=0, ymax=dataf_not_full[i], linewidth=1, color="brown")

index = list(range(len(dataf_not_full)))
index.sort(key=lambda x: dataf_not_full[x], reverse=True)
k = 6
for i in range(k):
    axs[1, 0].scatter(
        x=index[i],
        y=dataf_not_full[index[i]],
        marker="o",
        facecolors="none",
        edgecolors="brown",
    )
quantize_range_not_full = 2 ** (int(np.log2(dataf_not_full[index[k - 1]])) - 1)
axs[1, 0].axhline(y=quantize_range_not_full, color="red", linestyle="-")
# axs[0, 1].plot(
#     dataf_not_full,
#     color="orange",
# )
axs[1, 0].set_ylim(bottom=0)
axs[1, 0].set_title("(c) Frequency data with incomplete periods", fontsize=FONT_SIZE)

axs[0, 1].plot(data[: p * file["full_period"]])
axs[0, 1].set_title("(b) Data with complete periods", fontsize=FONT_SIZE)

data_full = data[: p * file["full_period"]]

dataf_full = np.abs(np.fft.fft(data_full))[: file["frequency_length"]]

# axs[1, 1].plot(
#     dataf_full,
#     color="orange",
# )

for i in range(len(dataf_full)):
    axs[1, 1].vlines(x=i, ymin=0, ymax=dataf_full[i], linewidth=1, color="brown")

# axs[1, 1].scatter(
#     list(range(0, file["frequency_length"], file["full_period"])),
#     dataf_full[:: file["full_period"]],
#     color="orange",
# )


index = list(range(len(dataf_full)))
index.sort(key=lambda x: dataf_full[x], reverse=True)
for i in range(k):
    axs[1, 1].scatter(
        x=index[i],
        y=dataf_full[index[i]],
        marker="o",
        facecolors="none",
        edgecolors="brown",
    )
quantize_range_full = 2 ** (int(np.log2(dataf_full[index[k - 1]])) - 1)
axs[1, 1].axhline(y=quantize_range_full, color="red", linestyle="-")

axs[1, 1].set_ylim(bottom=0)
axs[1, 1].set_xticks(range(0, len(dataf_full), file["full_period"]))
axs[1, 1].set_title("(d) Frequency data with complete periods", fontsize=FONT_SIZE)

quantize_range_start = 2**17
period_count = file["full_period"]
dataf_lossy_full = np.fft.fft(data_full)
for i in range(len(dataf_lossy_full)):
    if i % period_count != 0:
        dataf_lossy_full[i] = 0
dataf_lossy_full, count_full = quantize(dataf_lossy_full, quantize_range_start)

data_lossy_full = np.real(np.fft.ifft(dataf_lossy_full))
residual_full = data_full - data_lossy_full

axs[2, 1].plot(residual_full)
axs[2, 1].set_title("(f) Residual with complete periods", fontsize=FONT_SIZE)
axs[2, 1].set_ylim(bottom=-0.4 * 10**4, top=1.1 * 10**4)

quantize_range_last = quantize_range_start
while True:
    dataf_lossy_not_full, count_not_full = quantize(
        np.fft.fft(data_not_full), quantize_range_last
    )
    if count_not_full <= count_full:
        break
    quantize_range_last *= 2

data_lossy_not_full = np.real(np.fft.ifft(dataf_lossy_not_full))
residual_not_full = data_not_full - data_lossy_not_full

axs[2, 0].plot(residual_not_full)
axs[2, 0].set_title("(e) Residual with incomplete periods", fontsize=FONT_SIZE)
axs[2, 0].set_ylim(bottom=-0.4 * 10**4, top=1.1 * 10**4)

for i in range(3):
    for j in range(2):
        axs[i, j].ticklabel_format(
            style="sci", axis="y", scilimits=(0, 0), useOffset=False
        )

fig.tight_layout()
fig.savefig(os.path.join("result", "period-complementation-example.png"))
fig.savefig(os.path.join("result", "period-complementation-example.eps"))
fig.clf()

# FIGURE_SIZE = (3, 2)

# plt.figure(figsize=FIGURE_SIZE)
# plt.plot(dataf_not_full, color="orange")
# # plt.xticks([])
# # plt.yticks([])
# plt.savefig(
#     os.path.join("result", "period-complementation-dataf-not-full.png"),
#     bbox_inches="tight",
# )
# plt.savefig(
#     os.path.join("result", "period-complementation-dataf-not-full.eps"),
#     bbox_inches="tight",
# )
# plt.clf()

# plt.figure(figsize=FIGURE_SIZE)
# plt.plot(dataf_full, color="orange")
# plt.scatter(
#     list(range(0, file["frequency_length"], file["full_period"])),
#     dataf_full[:: file["full_period"]],
#     color="orange",
# )
# # plt.xticks([])
# # plt.yticks([])
# plt.savefig(
#     os.path.join("result", "period-complementation-dataf-full.png"), bbox_inches="tight"
# )
# plt.savefig(
#     os.path.join("result", "period-complementation-dataf-full.eps"), bbox_inches="tight"
# )
# plt.clf()
