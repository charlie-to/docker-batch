import os

import pandas as pd
from compare_median_fillter import acc_filter, apply_median_fillter
from file_io import read_evt_file

DATA_IMPORT_PATH = os.environ["DATA_IMPORT_PATH"]
PARTICIPANT_NAMES = os.environ["PARTICIPANT_NAMES"].split(" ")


def caluculate_accuracy(
    df: pd.DataFrame, df_ans: pd.DataFrame, total_file_counts: int
) -> float:
    correct_file_names = []
    miss_file_names = []
    wrong_file_names = []

    file_names = df.file_name.unique().tolist()
    file_names = [file_name.split(".")[0] for file_name in file_names]
    file_names_ans = (
        df_ans[(df_ans["acc_minus"] == 1) | (df_ans["acc_minus_danger"] == 1)][
            "file_name"
        ]
        .unique()
        .tolist()
    )
    file_names_ans = [file_name.split(".")[0] for file_name in file_names_ans]

    for file_name in file_names:
        if file_name in file_names_ans:
            correct_file_names.append(file_name)
        else:
            wrong_file_names.append(file_name)
    for file_name in file_names_ans:
        if file_name not in file_names:
            miss_file_names.append(file_name)

    print("total file counts : ", total_file_counts)
    print("correct file counts : ", len(correct_file_names))
    print("wrong file counts : ", len(wrong_file_names))
    print("miss file counts : ", len(miss_file_names))

    TP: int = len(correct_file_names)
    FN: int = len(miss_file_names)
    FP: int = len(wrong_file_names)
    TN: int = total_file_counts - TP - FN - FP

    acculacy: float = (TP + TN) / (TP + TN + FP + FN)

    print("TP : ", TP)
    print("TN : ", TN)
    print("FP : ", FP)
    print("FN : ", FN)
    print("acculacy : ", acculacy)
    return acculacy


def caluculate_recall(
    df: pd.DataFrame, df_ans: pd.DataFrame, total_file_counts: int
) -> float:
    correct_file_names = []
    miss_file_names = []
    wrong_file_names = []

    file_names = df.file_name.unique().tolist()
    file_names = [file_name.split(".")[0] for file_name in file_names]
    file_names_ans = (
        df_ans[(df_ans["acc_minus"] == 1) | (df_ans["acc_minus_danger"] == 1)][
            "file_name"
        ]
        .unique()
        .tolist()
    )
    file_names_ans = [file_name.split(".")[0] for file_name in file_names_ans]

    for file_name in file_names:
        if file_name in file_names_ans:
            correct_file_names.append(file_name)
        else:
            wrong_file_names.append(file_name)
    for file_name in file_names_ans:
        if file_name not in file_names:
            miss_file_names.append(file_name)

    print("total file counts : ", total_file_counts)
    print("correct file counts : ", len(correct_file_names))
    print("wrong file counts : ", len(wrong_file_names))
    print("miss file counts : ", len(miss_file_names))

    TP: int = len(correct_file_names)
    FN: int = len(miss_file_names)
    FP: int = len(wrong_file_names)
    TN: int = total_file_counts - TP - FN - FP

    recall: float = TP / (TP + FN)

    print("TP : ", TP)
    print("TN : ", TN)
    print("FP : ", FP)
    print("FN : ", FN)
    print("recall : ", recall)
    return recall


if __name__ == "__main__":
    # Read in the data
    df = read_evt_file(PARTICIPANT_NAMES[0])
    # Read in the answer data
    df_ans = pd.read_csv(
        DATA_IMPORT_PATH + PARTICIPANT_NAMES[0] + "/processed/iwaki_watch.csv"
    )
    # thresholds
    thresholds = [0.1, 0.2, 0.3, 0.4, 0.5]
    window_size = [5, 8, 10, 15, 20, 25]

    file_counts = len(df.file_name.unique().tolist())
    # * calculate accuracy for each threshold and window size
    acculacy_list: list[list[float]] = []
    for threshold in thresholds:
        print("***** threshold : ", threshold, " *****")
        _acculacy_list: list[float] = []
        for ws in window_size:
            print("*** window size : ", ws, " ***")
            col_name = "rotated_acceleration_x"
            df2 = apply_median_fillter(df, col_name, window_size=ws)
            df3 = acc_filter(df2, "x", ws, threshold)
            acculacy = caluculate_accuracy(df3, df_ans, file_counts)
            _acculacy_list.append(acculacy)
        acculacy_list.append(_acculacy_list)
    # acculacy list to dataframe
    df_acculacy = pd.DataFrame(acculacy_list, index=thresholds, columns=window_size)

    # * calculate recall for each threshold and window size
    recall_list: list[list[float]] = []
    for threshold in thresholds:
        print("***** threshold : ", threshold, " *****")
        _recall_list: list[float] = []
        for ws in window_size:
            print("*** window size : ", ws, " ***")
            col_name = "rotated_acceleration_x"
            df2 = apply_median_fillter(df, col_name, window_size=ws)
            df3 = acc_filter(df2, "x", ws, threshold)
            recall = caluculate_recall(df3, df_ans, file_counts)
            _recall_list.append(recall)
        recall_list.append(_recall_list)
    # recall list to dataframe
    df_recall = pd.DataFrame(recall_list, index=thresholds, columns=window_size)

    print(df_acculacy)
    print(df_recall)
