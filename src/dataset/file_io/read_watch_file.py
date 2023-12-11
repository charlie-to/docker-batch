import os
from pprint import pprint

import pandas as pd

DATA_IMPORT_PATH = os.environ["DATA_IMPORT_PATH"]


def read_watch_file(participant_name: str) -> pd.DataFrame:
    df = pd.read_csv(
        DATA_IMPORT_PATH
        + participant_name
        + "/watch/watch_"
        + participant_name
        + ".csv"
    )
    pprint(df.head(5))
    return df
