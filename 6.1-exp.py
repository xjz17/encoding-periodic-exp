from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd
import os
from algorithm.period_encode import period_result
from algorithm.period_encode import period_direct_result
import pickle
import time

RESULT_PATH = os.path.join("exp_result", "classify_result.pkl")
DATA_SEED = 65
RF_SEED = 43


def get_features(data: np.ndarray, use_direct=False):
    K = 3
    start = time.time()
    p, dataf, res = (
        period_direct_result(data.tolist())
        if use_direct
        else period_result(data.tolist())
    )
    if not use_direct:
        start = time.time()
    result = [p, np.mean(res), np.std(res)]
    for i in range(K):
        if i < len(dataf):
            result.append(dataf[i].real)
            result.append(dataf[i].imag)
        else:
            result.append(0)
            result.append(0)
    end = time.time()
    return result, end - start


def exp(dfs: list[tuple[any, pd.DataFrame]], use_direct=False):
    features_list = []
    labeles_list = []
    time_cost = 0
    start = time.time()
    for key, df in dfs:
        data_lat = df.reset_index()["lat"].to_numpy()
        data_lon = df.reset_index()["lon"].to_numpy()
        data_alt = df.reset_index()["alt"].to_numpy()
        end = time.time()
        time_cost += end - start
        start = time.time()
        # data_coverage_ratio = df.reset_index()["coverage_ratio"].to_numpy()
        features_lat, time_cost_lat = get_features(data_lat, use_direct)
        features_lon, time_cost_lon = get_features(data_lon, use_direct)
        features_alt, time_cost_alt = get_features(data_alt, use_direct)
        time_cost += time_cost_lat + time_cost_lon + time_cost_alt
        start = time.time()
        features_list.append(features_lat + features_lon + features_alt)
        species = df.reset_index()["species"].to_numpy()[0]
        labeles_list.append(species)
        end = time.time()
        time_cost += end - start
        start = time.time()

    features = np.array(features_list)
    labels = np.array(labeles_list)

    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.5, random_state=DATA_SEED
    )

    clf = RandomForestClassifier(n_estimators=100, random_state=RF_SEED)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    unique_labels = np.unique(labels)

    conf_matrix = confusion_matrix(y_test, y_pred, labels=unique_labels)

    end = time.time()
    time_cost += end - start
    start = time.time()

    return conf_matrix, unique_labels, time_cost


df = pd.read_csv(os.path.join("origin", "gps", "anon_gps_tracks_with_dive.csv"))
dfs = [(key, group) for key, group in df.groupby("bird")]

conf_matrix, unique_labels, time_cost = exp(dfs, use_direct=False)
conf_matrix_direct, unique_labels_direct, time_cost_direct = exp(dfs, use_direct=True)
print(time_cost)
print(time_cost_direct)

with open(RESULT_PATH, "wb") as f:
    pickle.dump(
        (
            conf_matrix,
            unique_labels,
            time_cost,
            conf_matrix_direct,
            unique_labels_direct,
            time_cost_direct,
        ),
        f,
    )
