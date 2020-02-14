import numpy as np

from images.common.constants.feature_constants import \
    Features, \
    HEAD_COORDINATE_X, \
    HEAD_COORDINATE_Y, \
    BODY_COORDINATE_X, \
    BODY_COORDINATE_Y, \
    Defaults


def make_mouse_features(last_features, current_raw_data):
    center = np.array(current_raw_data['center'])
    head = np.array(current_raw_data['head'])

    if last_features is None:
        body_speed = Defaults.BodySpeed.value
        head_speed = Defaults.HeadSpeed.value
        last_size = Defaults.LastSize.value
        last_size_vector = Defaults.LastSizeVector.value
        last_temperature = Defaults.LastTemperature.value
    else:
        last_center = np.array([last_features[BODY_COORDINATE_X], last_features[BODY_COORDINATE_Y]])
        body_speed = np.sum((center - last_center) ** 2)
        body_speed = np.sqrt(body_speed)

        last_head = np.array([last_features[HEAD_COORDINATE_X], last_features[HEAD_COORDINATE_Y]])
        head_speed = np.sum((head - last_head) ** 2)
        head_speed = np.sqrt(head_speed)

        last_size = last_features[Features.Size.value]
        last_size_vector = last_head - last_center

        last_temperature = last_features[Features.Temperature.value]

    area = current_raw_data['area']

    size_vector = head - center
    size = np.linalg.norm(size_vector)

    if size != 0 and last_size != 0:
        if np.array_equal(size_vector, last_size_vector):
            rotation = 0
        else:
            rotation = np.arccos(
                np.dot(size_vector, last_size_vector) / (size * last_size))

        if np.isnan(rotation):
            rotation = 0
    else:
        rotation = 0

    temperature = current_raw_data['temperature']
    temperature_speed = temperature - last_temperature

    features = {
        Features.Area.value: float(area),
        Features.Size.value: float(size),
        Features.Speed.value: float(body_speed),
        Features.Rotation.value: float(rotation),
        Features.Temperature.value: float(temperature),
        Features.TemperatureSpeed.value: float(temperature_speed),
        HEAD_COORDINATE_X: int(head[0]),
        HEAD_COORDINATE_Y: int(head[1]),
        BODY_COORDINATE_X: int(center[0]),
        BODY_COORDINATE_Y: int(center[1]),
    }

    return features
