import os
import cv2
import sys

from kafka import KafkaConsumer
from kafka.errors import KafkaError

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

from common.helpers import on_send_success, on_send_error
from common.constants import KAFKA_SERVERS, PRODUCER, DECODE_FORMAT
from images.common.constants.mice_db_queries import MiceDbQueries
from images.common.helpers.helpers import buffer_to_img
from images.common.constants.constants import \
    ConsumerGroups, \
    Topics, \
    BROKER_PRODUCE_TOPICS


def distribute_images_from_pi():
    """
    Here we receive streamed image from the RPI and send them to the next topics.
    """

    consumer = KafkaConsumer(
        Topics.Broker.value,
        bootstrap_servers=KAFKA_SERVERS,
        group_id=ConsumerGroups.Broker.value,
    )

    for msg in consumer:
        mouse_id = msg.key.decode(DECODE_FORMAT)

        if MiceDbQueries.find_mouse(mouse_id) is not None:
            for topic in BROKER_PRODUCE_TOPICS:
                future = PRODUCER.send(
                    topic,
                    key=msg.key,
                    value=msg.value,
                ).add_callback(on_send_success).add_errback(on_send_error)
                try:
                    future.get(timeout=10)
                except KafkaError as e:
                    # TODO: logging https://tracker.yandex.ru/VPAGROUPDEV-907
                    print(e)

    consumer.close()
    PRODUCER.flush()


if __name__ == "__main__":
    distribute_images_from_pi()
