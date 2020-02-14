"""
Get [area, head_coord, center_coord, tail_coord, temp_value] for image with mouse
"""
import cv2 as cv
import numpy as np

import sys
sys.path.append("../..")

from images.common.constants.tracking_constants import \
    PIX_THRESHOLD, \
    MIN_AREA, \
    MAX_AREA, \
    G_BLUR, \
    COLORS


def detect_mouse_data_from_img(img):
    gray_img, black_white_img = get_gray_and_black_white_img(img)

    white_contours = get_white_contours(black_white_img)

    contour_data = get_contour_data(white_contours)

    if contour_data is not None:
        body_parts = get_body_parts_data_from_contours(contour_data, gray_img, black_white_img)

        mouse_data = get_head_tail_temp(body_parts)

        return mouse_data, draw_body_parts(img, [mouse_data])

    else:
        return None, None


def get_gray_and_black_white_img(img):
    blurred_img = cv.GaussianBlur(img, G_BLUR, 0)

    trsh_const = np.max([PIX_THRESHOLD * np.max(img), 100])
    _, black_white_img = cv.threshold(blurred_img, trsh_const, 255, cv.THRESH_BINARY)

    return img, black_white_img


def get_white_contours(black_white_img):
    white_contours, _ = cv.findContours(black_white_img, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    return white_contours


def get_contour_data(contours):
    contour_result = None

    for c in contours:
        area = cv.contourArea(c)

        if area < MIN_AREA or MAX_AREA < area:
            continue

        center, eigenvect = get_orientation(c)
        contour_result = [area, center, eigenvect, c]
        break

    return contour_result


def get_orientation(contour):
    contour_len = len(contour)
    data_contour = np.empty((contour_len, 2), dtype=np.float64)
    for i in range(data_contour.shape[0]):
        data_contour[i, 0] = contour[i, 0, 0]
        data_contour[i, 1] = contour[i, 0, 1]

    mean = np.empty(0)
    mean, eigenvectors, eigenvalues = cv.PCACompute2(data_contour, mean)

    center = (int(mean[0, 0]), int(mean[0, 1]))

    # longest(most distribution = body alignment) eigenvector is eigenvectors[0]
    return center, eigenvectors[0]


def get_body_parts_data_from_contours(contour_data, gray_img, black_white_img):
    area, center, eigenvect, contour = contour_data

    temp, temp_arg = get_temperature_for_contour(contour, gray_img)
    head_or_tail = get_head_tail_points_for_contour(black_white_img, center, eigenvect)

    head, tail = decide_head_tail(head_or_tail, temp_arg)

    body_parts = [float(area), list(head), list(center), list(tail), float(temp)]

    return body_parts


def get_temperature_for_contour(contour, gray_img):
    # draw contour on black image
    black_img = np.zeros_like(gray_img)
    cv.drawContours(black_img, [contour], -1, color=255, thickness=-1)

    # we need to leave only one white part from gray image
    white_contour_indexes = np.where(black_img == 255)
    black_img[white_contour_indexes] = gray_img[white_contour_indexes]

    temp_arg = np.unravel_index(black_img.argmax(), black_img.shape)
    temp = gray_img[temp_arg]

    return temp, temp_arg


def get_head_tail_points_for_contour(black_white_img, center, eigenvect):
    # we need to find intersection of pca eigenvector and mouse's body contour (= head + tail)

    # we start from center
    head_or_tail = [center[:], center[:]]

    eigenvect = set_vector_direction(eigenvect)
    # go to opposite direction along the eigenvector and find intersection
    try:
        while black_white_img[int(head_or_tail[0][1]), int(head_or_tail[0][0])] != 0:
            head_or_tail[0] = [head_or_tail[0][0] + eigenvect[0], head_or_tail[0][1] + eigenvect[1]]

        while black_white_img[int(head_or_tail[1][1]), int(head_or_tail[1][0])] != 0:
            head_or_tail[1] = [head_or_tail[1][0] - eigenvect[0], head_or_tail[1][1] - eigenvect[1]]
    except:
        pass

    return head_or_tail


def set_vector_direction(eigenvect):
    # set eigenvector direction to "up"
    if eigenvect[0] * eigenvect[1] > 0:
        eigenvect = [abs(eigenvect[0]), abs(eigenvect[1])]
    else:
        if eigenvect[0] > 0:
            eigenvect = [-eigenvect[0], -eigenvect[1]]

    # if eigenvector is close to vertical
    if eigenvect[1] / eigenvect[0] > 50:
        eigenvect = [0, 1]

    # if eigenvector is close to horizontal
    elif eigenvect[0] / eigenvect[1] > 50:
        eigenvect = [1, 0]

    return eigenvect


def decide_head_tail(head_or_tail, temp_arg):
    # eyes is the hottest part of mouses body, so head should be closer to temp_arg
    if np.linalg.norm(np.array(head_or_tail[0]) - np.array(temp_arg)) < np.linalg.norm(np.array(head_or_tail[1]) - np.array(temp_arg)):
        head, tail = head_or_tail
    else:
        head, tail = head_or_tail[::-1]

    return head, tail


def get_head_tail_temp(body_parts):
    return body_parts


def draw_body_parts(img=None, drawing_parts=None):
    img_to_draw = img[:]

    drawing_parts = drawing_parts or detect_mouse_data_from_img(img_to_draw)

    list_ind_for_color = 0

    for part_ind, drawing_part in enumerate(drawing_parts):
        for part in drawing_part:
            if isinstance(part, list):
                cv.circle(img_to_draw, (int(part[0]), int(part[1])), radius=2, color=COLORS[list_ind_for_color], thickness=2)
                list_ind_for_color += 1
                list_ind_for_color %= 3

    return img_to_draw


def draw_text(img, text, bias_ind,
              font=cv.FONT_HERSHEY_SIMPLEX, font_scale=1, font_color=(255, 255, 255)):

    text_bottom_left_corner = (100, bias_ind * 30)

    cv.putText(img, text,
               text_bottom_left_corner,
               font,
               font_scale,
               font_color)


def pix_temp_to_temp(stat_file, temp_pixes):
    with open(stat_file, 'r') as stat_f:
        stat_data = stat_f.readlines()

    for i in range(len(temp_pixes)):
        splitted_line = stat_data[i].split()
        min_temp = float(splitted_line[-2])
        max_temp = float(splitted_line[-1])

        for j in range(len(temp_pixes[i])):
            temp_pixes[i][j] = (min_temp * (255 - temp_pixes[i][j]) + max_temp * temp_pixes[i][j]) / 255
