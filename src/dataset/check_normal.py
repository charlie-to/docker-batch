import os

from check import check_normalize, plot_hist_raw_accuracy, plot_hist_raw_rotated
from file_io import read_evt_file, read_watch_file

PARTICIPANT_NAMES = os.environ.get("PARTICIPANT_NAMES").split(" ")

if __name__ == "__main__":
    for participant_name in PARTICIPANT_NAMES:
        df = read_evt_file(participant_name)
        df_ans = read_watch_file(participant_name)
        check_normalize(df, participant_name)
        plot_hist_raw_rotated(df, df_ans, participant_name)
        plot_hist_raw_accuracy(df, df_ans, participant_name)
