import datetime as dt
import logging

import geopandas as gpd
import numpy as np
import pandas as pd


def gps_acceleration_to_df(file_dir, file_name) -> gpd.GeoDataFrame | pd.DataFrame:
    ###
    columns_name = ["index", "time", "text", "info"]
    ###

    with open(file_dir + file_name, encoding="utf-8") as f:
        texts = f.read().split("\n")

    raw_data: list[str] = []
    data: list[list[str]] = []
    for t in texts:
        if t == "":
            data.append(raw_data)
            raw_data = []
        else:
            raw_data.append(t)
    try:
        data_df: pd.DataFrame = pd.DataFrame(data, columns=columns_name)
    except ValueError:
        logging.warning("error in " + file_name + "  :this file is excluded")
        return pd.DataFrame()
    data_df = data_df.set_index("index")
    clean_data = data_df.drop(["info"], axis=1)
    acceleration_index, acceleration_x, acceleration_y, acceleration_z = [], [], [], []
    # 加速度
    for i in clean_data.index:
        text = str(clean_data.text[i])
        index = text.find("gsensori")
        acceleration = text[index + 9 + 6 : index + 9 + 6 + 11].split(",")
        if len(acceleration) != 3:
            continue
        acceleration_index.append(i)
        acceleration_x.append(acceleration[0])
        acceleration_y.append(acceleration[1])
        acceleration_z.append(acceleration[2])

    # TODO: 三次元変換が必要
    df_acceleration = pd.DataFrame([acceleration_index, acceleration_x, acceleration_y, acceleration_z]).T
    df_acceleration = df_acceleration.rename(
        columns={
            0: "in_file_index",
            1: "acceleration_x",
            2: "acceleration_y",
            3: "acceleration_z",
        }
    )
    acceleration = df_acceleration.set_index("in_file_index")
    acceleration = df_acceleration.astype(np.float64)

    # 經緯度
    #! 文字数で指定しているので緯度経度が大きく変化するとエラーが出る
    (
        pos_index,
        latitude_1,
        latitude_2,
        latitude_str,
        longitude_1,
        longitude_2,
        longitude_str,
    ) = (
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    )
    for i in clean_data.index:
        text = str(clean_data.text[i])
        index = text.find("GPRMC")
        if index == -1:
            continue
        pos_index.append(i)
        latitude_1.append(text[index + 5 + 13 : index + 5 + 13 + 2])
        latitude_2.append(text[index + 5 + 13 + 2 : index + 5 + 13 + 1 + 10])
        latitude_str.append(text[index + 5 + 13 + 11 + 1 : index + 5 + 13 + 11 + 1 + 1])
        longitude_1.append(text[index + 5 + 13 + 11 + 2 + 1 : index + 5 + 13 + 11 + 1 + 2 + 3])
        longitude_2.append(text[index + 5 + 13 + 11 + 2 + 4 : index + 5 + 13 + 11 + 1 + 2 + 12])
        longitude_str.append(text[index + 5 + 13 + 11 + 2 + 1 + 12 + 1 : index + 5 + 13 + 11 + 1 + 2 + 12 + 1 + 1])

    latitude_1 = [float(e) for e in latitude_1]
    latitude_2 = [float(e) / 60 for e in latitude_2]
    latitude_str = [str(e) for e in latitude_str]
    longitude_1 = [float(w) for w in longitude_1]
    longitude_2 = [float(w) / 60 for w in longitude_2]
    longitude_str = [str(w) for w in longitude_str]

    position = pd.DataFrame(
        [
            pos_index,
            latitude_1,
            latitude_2,
            latitude_str,
            longitude_1,
            longitude_2,
            longitude_str,
        ]
    ).T
    position = position.rename(
        columns={
            0: "in_file_index",
            1: "latitude1",
            2: "latitude2",
            3: "latitude_str",
            4: "longitude1",
            5: "longitude2",
            6: "longitude_str",
        }
    )
    position = position.set_index("in_file_index")
    position.index = position.index.astype(np.int64)
    # float に変換
    position["latitude1"] = position["latitude1"].astype(np.float64)
    position["latitude2"] = position["latitude2"].astype(np.float64)
    position["longitude1"] = position["longitude1"].astype(np.float64)
    position["longitude2"] = position["longitude2"].astype(np.float64)

    # 時間
    time_str: list[str] = file_name.split("_")[1:7]
    time_str = [int(i) for i in time_str]
    time = dt.datetime(time_str[0], time_str[1], time_str[2], time_str[3], time_str[4], time_str[5])
    pd.to_datetime(time)

    df = pd.concat(
        [acceleration, position],
        axis=1,
    )
    df = df.assign(file_name=file_name)
    pd_times = pd.Series([pd.to_datetime(time + dt.timedelta(milliseconds=i * 100)) for i in range(len(df))])
    df = df.assign(time=pd_times.values)
    df = df.set_index("time")
    # 緯度経度の補間
    df = df.interpolate(method="linear")
    df = df.ffill()

    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.longitude1 + df.longitude2, df.latitude1 + df.latitude2, crs="EPSG:4326"),
    )

    # lat,lon を追加
    gdf = gdf.assign(lat=gdf.geometry.y)
    gdf = gdf.assign(lon=gdf.geometry.x)
    return gdf.dropna()
