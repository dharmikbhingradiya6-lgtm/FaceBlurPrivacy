import cv2


def gaussian_blur(face, kernel_size=101):

    if kernel_size < 3:
        kernel_size = 3

    if kernel_size % 2 == 0:
        kernel_size += 1

    return cv2.GaussianBlur(
        face,
        (kernel_size, kernel_size),
        0
    )


def pixelate(face, pixel_size=15):

    h, w = face.shape[:2]

    pixel_size = max(2, pixel_size)

    small_width = max(1, w // pixel_size)
    small_height = max(1, h // pixel_size)

    temp = cv2.resize(
        face,
        (small_width, small_height),
        interpolation=cv2.INTER_LINEAR
    )

    pixelated = cv2.resize(
        temp,
        (w, h),
        interpolation=cv2.INTER_NEAREST
    )

    return pixelated