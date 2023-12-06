import numpy as np
import pandas as pd


def calc_distance(lat1, lng1, lat2, lng2):
    R = 6371.0  # 地球の平均半径

    # 度数法からラジアンに変換
    lat1 = np.deg2rad(lat1)
    lng1 = np.deg2rad(lng1)
    lat2 = np.deg2rad(lat2)
    lng2 = np.deg2rad(lng2)

    C = np.cos(lat1) * np.cos(lat2) * np.cos(lng1 - lng2) + np.sin(lat1) * np.sin(lat2)
    # print(C)
    try:
        d_km = R * np.arccos(C)
    except RuntimeWarning:
        print("RuntimeWarning")
        print(C)
        d_km = 0
    return d_km


def calculate_and_add_speed_data(gdf: pd.DataFrame) -> pd.DataFrame:
    speeds: list[float] = []
    for index in range(0, len(gdf) - 1):
        s1 = gdf.iloc[index]
        s2 = gdf.iloc[index + 1]
        speed = (
            calc_distance(s1.geometry.x, s1.geometry.y, s2.geometry.x, s2.geometry.y)
            * 10
            * 3600
        )
        if speed > 110:
            speed = 0
        speeds.append(speed)
    speeds.insert(0, 0)
    np_speeds = np.array(speeds)
    gdf = gdf.assign(speed=np_speeds)
    gdf = gdf.assign(speed_diff=gdf.speed.diff())
    return gdf
