import numpy as np
import cv2

from common.constants import DECODE_FORMAT
from images.common.constants.constants import \
    BUFFER_SEPARATOR, \
    PACKET_LENGTH, \
    PACKET_OFFSET, \
    IMG_HEIGHT, \
    IMG_WIDTH


def bytes_to_int(a, b):
    return (a << 8) | b


def normalize_image(img):
    img = np.array(img)
    img_min = np.min(img)
    img_max = np.max(img)

    if img_max != img_min:
        return (255 * ((img - img_min) / (img_max - img_min))).astype(int)

    return np.zeros((IMG_HEIGHT // 2, IMG_WIDTH))


def buffer_to_img(buffer):
    # uint_buff = np.array(buffer.decode(DECODE_FORMAT)[:-2].split(BUFFER_SEPARATOR)).astype(np.uint8)
    #
    # img = np.array(np.array_split(uint_buff, len(uint_buff) // PACKET_LENGTH))
    # img = img[:, PACKET_OFFSET:]
    #
    # # TODO: убрать питоновский for https://tracker.yandex.ru/VPAGROUPDEV-908
    # new_img = []
    # for row in range(0, IMG_HEIGHT, 2):
    #     new_row = []
    #     for part in range(2):
    #         for pix in range(0, IMG_WIDTH, 2):
    #             new_row.append(bytes_to_int(img[row + part][pix], img[row + part][pix + 1]))
    #     new_img.append(new_row)
    #
    # return normalize_image(new_img)
    return cv2.imdecode(np.frombuffer(buffer[:-2], np.uint8), cv2.IMREAD_GRAYSCALE)
