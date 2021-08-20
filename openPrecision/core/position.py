from dataclasses import dataclass

import numpy as np

import core


@dataclass
class Position:
    location: core.location.Location
    orientation:
