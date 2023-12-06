import os

import pandas as pd
from raw.get_acc_all import get_acc_all

data_import_path: str = os.environ["DATA_IMPORT_PATH"]
participant_names = os.environ["P_NAMES"].split(" ")


def save_evt_all(data_path: str) -> None:
    df1: pd.DataFrame = get_acc_all(data_path, file_name_start_with="EVT")
    df1.to_csv(data_path + "/processed/EVT_ALL.csv")
    print("EVT_ALL.csv saved")


def save_rec_all(data_path: str) -> None:
    df2: pd.DataFrame = get_acc_all(data_path, file_name_start_with="REC")
    df2.to_csv(data_path + "/processed/REC_ALL.csv")
    print("REC_ALL.csv saved")


if __name__ == "__main__":
    for participant in participant_names:
        save_evt_all(data_path=data_import_path + "/" + participant)
