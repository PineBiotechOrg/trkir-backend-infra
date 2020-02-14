import os
import sys
from datetime import datetime
import json

from kafka import KafkaConsumer

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

from common.constants import KAFKA_SERVERS, DECODE_FORMAT
from images.common.helpers.make_mouse_features import make_mouse_features
from images.common.constants.mice_db_queries import MiceDbQueries
from images.common.constants.feature_constants import Features
from images.common.constants.constants import \
    ConsumerGroups, \
    Topics


def handle_make_data():
    """
    Here we receive streamed images and make data features.
    """

    consumer = KafkaConsumer(
        Topics.FeaturesMaker.value,
        bootstrap_servers=KAFKA_SERVERS,
        group_id=ConsumerGroups.FeaturesMaker.value,
    )

    for msg in consumer:
        mouse_id = msg.key.decode(DECODE_FORMAT)

        if MiceDbQueries.find_mouse(mouse_id) is not None:
            mouse_raw_data = json.loads(msg.value.decode(DECODE_FORMAT))

            last_features = MiceDbQueries.get_mouse_last_features(mouse_id)
            mouse_features = make_mouse_features(last_features, mouse_raw_data)
            # TODO: присылать настоящий таймштамп
            mouse_features[Features.Date.value] = datetime.now()
            mouse_features['mouse_id'] = mouse_id

            MiceDbQueries.insert_mouse_features(mouse_features)

    consumer.close()


if __name__ == "__main__":
    handle_make_data()
