#  _______               __      ___     
# |__   __|              \ \    / (_)    
#    | |_ __ __ _ _ __  __\ \  / / _ ___ 
#    | | '__/ _` | '_ \/ __\ \/ / | / __|
#    | | | | (_| | | | \__ \\  /  | \__ \
#    |_|_|  \__,_|_| |_|___/ \/   |_|___/
#   https://git.psi.ch/hipa_apps/TransVis
#
# Defines custom types which are used across
# the project.
#
# @Author: Adam Koprek

from typing import TypeAlias
import numpy.typing as npt
import numpy as np


# A 2D point
PNT:  TypeAlias = npt.NDArray[np.float64]    # (2,)

# A 2D set of points
PNTS: TypeAlias = npt.NDArray[np.float64]    # (M,2)

# A single cubic bezier segment
BEZ:  TypeAlias = npt.NDArray[np.float64]    # (4,2)

# A set of cubic bezier segments
BEZS: TypeAlias = npt.NDArray[np.float64]    # (M,4,2)

