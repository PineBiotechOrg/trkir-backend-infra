import os
import sys

from kafka import KafkaConsumer

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

from common.constants import KAFKA_SERVERS, DECODE_FORMAT, BUFFER_END
from images.common.constants.mice_db_queries import MiceDbQueries
from images.common.constants.constants import \
    ConsumerGroups, \
    Topics


def handle_save_images():
    """
    Here we receive streamed images from the RPI and send them to the next topics.
    """

    consumer = KafkaConsumer(
        Topics.Saver.value,
        bootstrap_servers=KAFKA_SERVERS,
        group_id=ConsumerGroups.Saver.value,
    )

    for msg in consumer:
        mouse_id = msg.key.decode(DECODE_FORMAT)

        if MiceDbQueries.find_mouse(mouse_id) is not None:
            try:
                image = msg.value[:-len(BUFFER_END)]

                MiceDbQueries.insert_mouse_last_image(mouse_id, image, commit=True)
                MiceDbQueries.insert_mouse_image(mouse_id, image)
            except Exception:
                # broken image
                continue

    consumer.close()


if __name__ == "__main__":
    handle_save_images()
