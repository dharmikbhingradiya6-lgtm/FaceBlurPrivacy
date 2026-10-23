import math


def distance(point1, point2):

    x1, y1 = point1
    x2, y2 = point2

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


def is_face_in_direction(
    fingertip,
    finger_base,
    face,
    max_distance=500
):

    x1, y1 = finger_base
    x2, y2 = fingertip

    face_x, face_y, face_w, face_h = face

    face_center = (
        face_x + face_w // 2,
        face_y + face_h // 2
    )

    fx, fy = face_center

    dx = x2 - x1
    dy = y2 - y1

    face_dx = fx - x2
    face_dy = fy - y2

    finger_length = math.sqrt(
        dx * dx +
        dy * dy
    )

    face_distance = math.sqrt(
        face_dx * face_dx +
        face_dy * face_dy
    )

    if finger_length == 0:
        return False

    if face_distance == 0:
        return True

    if face_distance > max_distance:
        return False

    dx /= finger_length
    dy /= finger_length

    face_dx /= face_distance
    face_dy /= face_distance

    dot = (
        dx * face_dx +
        dy * face_dy
    )

    return dot > 0.75