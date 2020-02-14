from enum import Enum


class Features(Enum):
    Area = 'area'
    Size = 'size'
    Speed = 'speed'
    Rotation = 'rotation'
    Temperature = 'temperature'
    TemperatureSpeed = 'temperature_speed'
    Date = 'date'


# default feature helper values
class Defaults(Enum):
    BodySpeed = 0
    HeadSpeed = 0
    LastSize = 15
    LastSizeVector = [1, 0]
    LastTemperature = 30


HEAD_COORDINATES = 'head'
BODY_COORDINATES = 'center'
TAIL_COORDINATES = 'tail'

HEAD_COORDINATE_X = 'x_{}'.format(HEAD_COORDINATES)
HEAD_COORDINATE_Y = 'y_{}'.format(HEAD_COORDINATES)

BODY_COORDINATE_X = 'x_{}'.format(BODY_COORDINATES)
BODY_COORDINATE_Y = 'y_{}'.format(BODY_COORDINATES)

TAIL_COORDINATE_X = 'x_{}'.format(TAIL_COORDINATES)
TAIL_COORDINATE_Y = 'y_{}'.format(TAIL_COORDINATES)
