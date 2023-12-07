import os

from check import check_normalize
from file_io import read_evt_file

PARTICIPANT_NAMES = os.environ.get("PARTICIPANT_NAMES").split(" ")

if __name__ == "__main__":
    for participant_name in PARTICIPANT_NAMES:
        df = read_evt_file(participant_name)
        check_normalize(df, participant_name)
