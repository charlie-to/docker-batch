import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import scienceplots  # noqa
from file_io import read_evt_file, read_watch_file
from filter import acc_filter, apply_median_filter

DATA_IMPORT_PATH = os.environ["DATA_IMPORT_PATH"]
PARTICIPANT_NAMES = os.environ["PARTICIPANT_NAMES"].split(" ")


# 日本語化の呪文
mpl.use("pgf")

plt.style.use(["science", "ieee"])
plt.rcParams["text.usetex"] = True
plt.rcParams["pgf.texsystem"] = "lualatex"
plt.rcParams["font.family"] = "Noto Sans CJK JP"
plt.rcParams["font.serif"] = "Noto Sans CJK JP"
plt.rcParams["pgf.rcfonts"] = False


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
    print("********** file name hiyari **********")
    print(file_names_ans)

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

    TP: int = len(correct_file_names)  # True Positive : 正しく検出できたファイル数
    TN: int = len(miss_file_names)  # True Negative : 正しく検出できなかったファイル数
    FP: int = len(wrong_file_names)  # False Positive : 誤って検出したファイル数
    FN: int = total_file_counts - TP - TN - FP  # False Negative : 正しく検出しなかったファイル数

    acculacy: float = (TP + FN) / (TP + TN + FP + FN)

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

    TP: int = len(correct_file_names)  # True Positive : 正しく検出できたファイル数
    TN: int = len(miss_file_names)  # True Negative : 正しく検出できなかったファイル数
    FP: int = len(wrong_file_names)  # False Positive : 誤って検出したファイル数
    FN: int = total_file_counts - TP - TN - FP  # False Negative : 正しく検出しなかったファイル数

    # if true file counts is 0, recall is 0
    if TP + TN == 0:
        recall: float = 0
    else:
        recall = TP / (TP + TN)

    print("TP : ", TP)
    print("TN : ", TN)
    print("FP : ", FP)
    print("FN : ", FN)
    print("recall : ", recall)
    return recall


if __name__ == "__main__":
    for participant_name in PARTICIPANT_NAMES:
        # Read in the data
        df = read_evt_file(participant_name)
        df = df[df["file_name"].str.endswith("F.MP4.srt")]
        # Read in the answer data
        df_ans = read_watch_file(participant_name)
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
                df2 = apply_median_filter(df, col_name, window_size=ws)
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
                df2 = apply_median_filter(df, col_name, window_size=ws)
                df3 = acc_filter(df2, "x", ws, threshold)
                recall = caluculate_recall(df3, df_ans, file_counts)
                _recall_list.append(recall)
            recall_list.append(_recall_list)
        # recall list to dataframe
        df_recall = pd.DataFrame(recall_list, index=thresholds, columns=window_size)

        print(df_acculacy)
        print(df_recall)

        # * plot accuracy and recall and f value
        fig, ax = plt.subplots()
        df_acculacy.plot(ax=ax, marker="x")
        ax.set_xlabel("しきい値[G]")
        ax.set_ylabel("精度")
        ax.legend(title="ウィンドウサイズ", loc="lower right")
        fig.savefig(
            DATA_IMPORT_PATH
            + participant_name
            + "/plot/filter_params/accuracy_median_filter.png",
            dpi=300,
            bbox_inches="tight",
        )
        # plot
        fig, ax = plt.subplots()
        df_recall.plot(ax=ax, marker="x")
        ax.set_xlabel("しきい値[G]")
        ax.set_ylabel("再現率")
        ax.legend(title="ウィンドウサイズ", loc="lower right")
        fig.savefig(
            DATA_IMPORT_PATH
            + participant_name
            + "/plot/filter_params/recall_median_filter.png",
            dpi=300,
            bbox_inches="tight",
        )

        fig, ax = plt.subplots()
        df_f_measure = 2 * df_acculacy * df_recall / (df_acculacy + df_recall)
        df_f_measure.plot(ax=ax, marker="x")
        ax.set_xlabel("しきい値[G]")
        ax.set_ylabel("f値")
        ax.legend(title="ウィンドウサイズ", loc="lower right")
        fig.savefig(
            DATA_IMPORT_PATH
            + participant_name
            + "/plot/filter_params/f_measure_median_filter.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()
