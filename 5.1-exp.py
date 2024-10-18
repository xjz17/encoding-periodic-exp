import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
from algorithm.period_encode import period_result
from algorithm.period_encode import period_direct_result
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()


def mse_loss(test, pred):
    # a_true = scaler.fit_transform(a.reshape(-1, 1))
    # b_true = scaler.transform(b.reshape(-1, 1))
    return mean_squared_error(test, pred) / max(1, np.mean(test) ** 2)


def get_predict(td_train: np.ndarray, test_len: int) -> np.ndarray:
    # td_train = td_train[max(0, len(td_train) - 3 * test_len) :]
    time_series_data = pd.Series(td_train, index=range(len(td_train)))

    model = ARIMA(time_series_data, order=(0, 0, 0))
    model_fit = model.fit()

    forecast: pd.Series = model_fit.predict(
        start=len(time_series_data), end=len(time_series_data) + test_len - 1
    )
    return forecast.to_numpy()


DATA_DIR = "data"
RESULT_PATH = os.path.join("exp_result", "prediction.csv")

result = {"dataset": [], "name": [], "type": [], "mse": [], "time": []}

files = os.listdir(DATA_DIR)
for index, file in enumerate(files):
    print(f"{index}/{len(files)}")
    dataset = file.split("_")[0]
    file_full = os.path.join(DATA_DIR, file)
    df = pd.read_csv(file_full)
    data = df["value"].to_numpy()

    # plt.plot(data)
    # plt.savefig("fig1.png")
    # plt.clf()

    split_size = int(len(data) * 0.7)
    td_train = data[:split_size]
    td_test = data[split_size:]

    # start = time.time()
    # td_pred = get_predict(td_train, len(td_test))
    # end = time.time()
    # mse = mean_squared_error(td_test, td_pred)
    # result["dataset"].append(dataset)
    # result["name"].append(file)
    # result["mse"].append(mse)
    # result["type"].append("origin")
    # result["time"].append(end - start)

    p, dataf, res = period_result(data[:split_size].tolist())
    start = time.time()
    if p == 0:
        td_pred = get_predict(td_train, len(td_test))
        end = time.time()
        mse = mse_loss(td_test, td_pred)
        result["dataset"].append(dataset)
        result["name"].append(file)
        result["mse"].append(mse)
        result["type"].append("Compressed data")
        result["time"].append(end - start)
    else:
        k = (len(res) + p - 1) // p

        dataf_to_data = np.tile(
            np.round(np.fft.irfft(dataf, n=p)).astype(np.int64),
            reps=((len(data) + p - 1) // p,),
        )[: len(data)]
        # plt.plot(data)
        # plt.plot(dataf_to_data)
        # plt.show()

        td_train = res

        # plt.plot(res)
        # plt.savefig("fig2.png")
        # plt.clf()

        td_test = data[split_size:]
        td_pred = get_predict(td_train, len(td_test))
        td_pred = -td_pred + np.asarray(dataf_to_data[len(td_train) :])
        end = time.time()

        mse = mse_loss(td_test, td_pred)
        result["dataset"].append(dataset)
        result["name"].append(file)
        result["mse"].append(mse)
        result["type"].append("Compressed data")
        result["time"].append(end - start)

    start = time.time()
    p, dataf, res = period_direct_result(data[:split_size].tolist())
    if p == 0:
        td_pred = get_predict(td_train, len(td_test))
        end = time.time()
        mse = mse_loss(td_test, td_pred)
        result["dataset"].append(dataset)
        result["name"].append(file)
        result["mse"].append(mse)
        result["type"].append("Origin data")
        result["time"].append(end - start)
    else:
        k = (len(res) + p - 1) // p

        dataf_to_data = np.tile(
            np.round(np.fft.irfft(dataf, n=p)).astype(np.int64),
            reps=((len(data) + p - 1) // p,),
        )[: len(data)]
        # plt.plot(data)
        # plt.plot(dataf_to_data)
        # plt.show()

        td_train = res

        # plt.plot(res)
        # plt.savefig("fig3.png")
        # plt.clf()
        td_test = data[split_size:]
        td_pred = get_predict(td_train, len(td_test))
        td_pred = -td_pred + np.asarray(dataf_to_data[len(td_train) :])
        end = time.time()

        mse = mse_loss(td_test, td_pred)
        result["dataset"].append(dataset)
        result["name"].append(file)
        result["mse"].append(mse)
        result["type"].append("Origin data")
        result["time"].append(end - start)
    # exit(0)

df = pd.DataFrame(data=result)
df.to_csv(RESULT_PATH, index=False)
