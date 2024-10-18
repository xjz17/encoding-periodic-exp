import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from algorithm.period_encode import period_result


def abnormal_direct(data):
    mu = np.mean(data)
    sigma = np.std(data)
    return ((data < mu - 9 * sigma) | (data > mu + 9 * sigma)).astype(int)


FOLDER_PATH = "data_labeled"
FILE_PATH = "liantong_data_from2018-12-19to2019-01-31_8234.csv"
df = pd.read_csv(os.path.join(FOLDER_PATH, FILE_PATH))
data = df["value"].tolist()
label = df["label"].tolist()
# label_1 = abnormal_direct(data)
# plt.plot(data)
# plt.show()
_, __, res = period_result(data)
print(np.asarray(data))
print(np.asarray(res))
print(np.asarray(data) + np.asarray(res))
plt.plot(np.asarray(res))
for i in range(len(label)):
    if label[i] == 1:
        plt.scatter(i, res[i], c="red")
label_2 = abnormal_direct(res)
for i in range(len(label)):
    if label_2[i] == 1:
        plt.scatter(i, res[i], c="orange")
# plt.plot(np.asarray(res))
plt.show()
