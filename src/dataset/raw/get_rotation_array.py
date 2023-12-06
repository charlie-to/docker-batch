from typing import Tuple

import numpy as np
import numpy.linalg as LA
import pandas as pd
from scipy.spatial.transform import Rotation as R


def get_rotation_array(df_stable: pd.DataFrame) -> Tuple[np.ndarray, float]:
    """静止時のデータから回転行列を作成する

    Args:
        df_stable (pd.DataFrame): 静止時のデータ

    Returns:
        Tuple[np.ndarray, float]: 回転行列と回転後の重力加速度の大きさ
    """
    gravity = np.array([0, 0, 1])
    before_rotation = np.array(
        [
            df_stable["acceleration_x"].mode()[0],
            df_stable["acceleration_y"].mode()[0],
            df_stable["acceleration_z"].mode()[0],
        ]
    )

    # normal vector
    print("gravity:", gravity)
    print("before rotation:", before_rotation)
    axis = np.cross(gravity, before_rotation)
    axis = axis / LA.norm(axis)

    # angle
    inner = np.inner(gravity, before_rotation)
    norms = LA.norm(gravity) * LA.norm(before_rotation)
    rad = np.arccos(np.clip(inner / norms, -1, 1))

    # rotation
    rotation = R.from_rotvec(rad * axis)
    rotation = rotation.inv()
    rotated_gravity = rotation.apply(before_rotation)
    rotated_gravity_norm = LA.norm(rotated_gravity)

    print("check it is changed gravity:", rotated_gravity / rotated_gravity_norm)
    return rotation, rotated_gravity_norm  # type: ignore
