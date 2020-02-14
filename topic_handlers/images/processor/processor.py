import os
import sys
import json
import cv2

from kafka import KafkaConsumer
from kafka.errors import KafkaError

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

from common.helpers import on_send_success, on_send_error
from common.constants import KAFKA_SERVERS, PRODUCER, DECODE_FORMAT
from images.common.helpers.tracking_helpers import detect_mouse_data_from_img
from images.common.helpers.helpers import buffer_to_img
from images.common.constants.feature_constants import \
    Features, \
    HEAD_COORDINATES, \
    BODY_COORDINATES, \
    TAIL_COORDINATES
from images.common.constants.constants import \
    ConsumerGroups, \
    Topics, \
    ImageFormats


def handle_process_images():
    """
    Here we receive streamed images and get mouse raw data.
    """

    consumer = KafkaConsumer(
        Topics.Processor.value,
        bootstrap_servers=KAFKA_SERVERS,
        group_id=ConsumerGroups.Processor.value
    )

    for msg in consumer:
        try:
            img = buffer_to_img(msg.value)

            mouse_data, processed_image = detect_mouse_data_from_img(img)

            if mouse_data is not None:
                _, processed_image = cv2.imencode(ImageFormats.JPG, processed_image)

                # TODO: save processed image https://tracker.yandex.ru/VPAGROUPDEV-868

                area, head, center, tail, temp = mouse_data
                mouse_data_dict = {
                    Features.Area.value: area,
                    HEAD_COORDINATES: head,
                    BODY_COORDINATES: center,
                    TAIL_COORDINATES: tail,
                    Features.Temperature.value: temp,
                }

                future = PRODUCER.send(
                    Topics.FeaturesMaker.value,
                    key=msg.key,
                    value=json.dumps(mouse_data_dict).encode(DECODE_FORMAT),
                ).add_callback(on_send_success).add_errback(on_send_error)
                try:
                    future.get(timeout=10)
                except KafkaError as e:
                    # TODO: logging https://tracker.yandex.ru/VPAGROUPDEV-907
                    print(e)

        except Exception:
            continue

    consumer.close()
    PRODUCER.flush()


if __name__ == "__main__":
    handle_process_images()
