import glob
import os
from pprint import pprint

import geopandas as gpd
import numpy as np
import pandas as pd

from ..file_io import read_rec_file
from .get_gps_acceleration_to_df import gps_acceleration_to_df
from .get_rotation_array import get_rotation_array
from .speed import calculate_and_add_speed_data


def get_acc_all(file_dir: str, file_name_start_with: str = "") -> pd.DataFrame:
    # ファイル名取得
    file_names = glob.glob(file_dir + "/raw/" + file_name_start_with + "*")
    print(file_names)
    print(os.getcwd())
    gdf1: pd.DataFrame = gpd.GeoDataFrame()
    for file_name in file_names:
        _df = gps_acceleration_to_df(file_dir, file_name.split("/")[-1])
        _df = calculate_and_add_speed_data(_df)  # 各ファイルでspeedを計算
        gdf1 = pd.concat([gdf1, _df], axis=0)

    pprint(gdf1)
    # gdf1 が空の場合はエラー
    if gdf1.empty:
        raise ValueError("gdf1 is empty")

    # speed が０の時は静止している
    # そのときの加速度を基準にする
    # ?: なんかしらんけど動いている。後で修正が必要かもしれない。。。
    gdf1_speed_zero: pd.DataFrame = gdf1[gdf1["speed"] == 0]
    # *: evt ならrecを使用して補正
    if file_name_start_with == "EVT":
        gdf2: pd.DataFrame = read_rec_file(file_dir.split("/")[-1])
        gdf2_speed_zero: pd.DataFrame = gdf2[gdf2["speed"] == 0]
        gdf1_speed_zero = pd.concat([gdf1_speed_zero, gdf2_speed_zero], axis=0)
    rotation, norm = get_rotation_array(gdf1_speed_zero)

    def rotate(row):
        rotated = rotation.apply(
            np.array([row.acceleration_x, row.acceleration_y, row.acceleration_z])
        )  # type: ignore
        row.rotated_acceleration_x = rotated[0] / norm
        row.rotated_acceleration_y = rotated[1] / norm
        row.rotated_acceleration_z = rotated[2] / norm
        return row

    gdf1 = gdf1.assign(rotated_acceleration_x=0)
    gdf1 = gdf1.assign(rotated_acceleration_y=0)
    gdf1 = gdf1.assign(rotated_acceleration_z=0)
    gdf1 = gdf1.apply(rotate, axis=1)  # type: ignore
    return gdf1.dropna()
