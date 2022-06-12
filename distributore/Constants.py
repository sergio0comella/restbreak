from math import nan

START = -1
BASE = 0
INSERT = 1
RUN = 2
COMPUTING = 3
GOAL = 4

WAITING = 305
UNKNOWN = nan

TIME_BEFORE_CA = 5

WHEEL_RADIUS = 10.2
MAX_SPEED = 6.28
ROTSPEED = 40  # <== ω -> ω = v/r (0.61 rad/s) --> (40 grd/s)
ADJSPEED = 0.15
SPEED = MAX_SPEED * ADJSPEED


SX = 1
SY = 10
TIMESTEP = 32
F = -123
W = -123
S = 'A'
C = 66
L = 0
O = -123

GO_DX = 1
GO_SX = 2
CROSS = 3
OBS_FOUNDED = 4

       # 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18  19 20
MAP = [[W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],  # 0
       [W, F, F, F, W, F, F, F, F, F, 0, F, F, F, F, F, W, F, F, F, W],  # 1
       [W, F, F, F, W, F, F, F, F, F, L, F, F, F, F, F, W, F, F, F, W],  # 2
       [W, F, F, F, W, F, F, F, F, F, L, F, F, F, F, F, W, F, F, F, W],  # 3
       [W, F, F, F, W, F, C, L, L, L, C, L, L, L, C, F, W, F, F, F, W],  # 4
       [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 5
       [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 6
       [W, F, F, F, 1, L, C, L, L, L, C, L, L, L, C, L, 6, F, F, F, W],  # 7
       [W, W, W, W, W, F, L, F, F, F, L, F, F, F, L, F, W, W, W, W, W],  # 8
       [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 9
       [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 10
       [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 11
       [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 12
       [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 13
       [W, F, F, F, 2, L, C, L, L, L, C, L, L, L, C, L, 5, F, F, F, W],  # 14
       [W, W, W, W, W, F, L, F, F, F, L, F, F, F, L, F, W, W, W, W, W],  # 15
       [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 16
       [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 17
       [W, F, F, F, 3, L, C, L, L, L, C, L, L, L, C, L, 4, F, F, F, W],  # 18
       [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],  # 19
       [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W]]  # 20


NORTH = 0.0
SOUTH = 180.0
EAST = 270.0
WEST = 90.0

OFFICE_NUMBER = 10
LOCK = 1
UNLOCK = 0


