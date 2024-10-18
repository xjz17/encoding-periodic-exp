import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import os

FONT_SIZE = 10
INPUT_PATH = os.path.join("exp_result", "classify_result.pkl")

with open(INPUT_PATH, "rb") as f:
    (
        conf_matrix,
        unique_labels,
        time_cost,
        conf_matrix_direct,
        unique_labels_direct,
        time_cost_direct,
    ) = pickle.load(f)

fig, ax = plt.subplots(1, 3, figsize=(6.5, 2.5))

sns.heatmap(
    conf_matrix,
    annot=True,
    fmt="d",
    cmap="Blues",
    cbar=False,
    xticklabels=unique_labels,
    yticklabels=unique_labels,
    ax=ax[0],
)
ax[0].set_xlabel("Predicted Label", fontsize=FONT_SIZE)
ax[0].set_ylabel("True Label", fontsize=FONT_SIZE)
ax[0].set_title("(a) Compressed Data", fontsize=FONT_SIZE)

sns.heatmap(
    conf_matrix_direct,
    annot=True,
    fmt="d",
    cmap="Oranges",
    cbar=False,
    xticklabels=unique_labels_direct,
    yticklabels=unique_labels_direct,
    ax=ax[1],
)
ax[1].set_xlabel("Predicted Label", fontsize=FONT_SIZE)
ax[1].set_ylabel("True Label", fontsize=FONT_SIZE)
ax[1].set_title("(b) Origin Data", fontsize=FONT_SIZE)

ax[2].bar(
    ["Compressed", "Origin"],
    [time_cost, time_cost_direct],
    color=plt.rcParams["axes.prop_cycle"].by_key()["color"][:2],
)
ax[2].set_xlabel("Method", fontsize=FONT_SIZE)
ax[2].set_ylabel("Time Cost(s)", fontsize=FONT_SIZE)
ax[2].set_title("(c) Time Cost", fontsize=FONT_SIZE)

plt.tight_layout()
# plt.show()
plt.savefig(os.path.join("exp_result", "classify.eps"))
plt.savefig(os.path.join("exp_result", "classify.png"))
