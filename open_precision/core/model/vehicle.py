from dataclasses import dataclass

import numpy as np


@dataclass
class Vehicle:
    name: str
    gps_receiver_offset: np.ndarray  # 3d vector from the rotation point of the vehicle (normally middle of the rear
    # axle a tractor) at ground height
    turn_radius_left: float
    turn_radius_right: float
    