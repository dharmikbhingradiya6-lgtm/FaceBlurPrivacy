import cv2

from face_detector import FaceDetector
from utils import gaussian_blur, pixelate


class FaceBlur:

    def __init__(self):

        self.detector = FaceDetector()

    def blur_faces(
        self,
        image,
        blur_type="gaussian",
        blur_strength=101
    ):

        faces = self.detector.detect_faces(image)

        output = image.copy()

        for (x, y, w, h) in faces:

            x = max(0, x)
            y = max(0, y)

            w = min(
                w,
                image.shape[1] - x
            )

            h = min(
                h,
                image.shape[0] - y
            )

            if w <= 0 or h <= 0:
                continue

            face = output[
                y:y+h,
                x:x+w
            ]

            if face.size == 0:
                continue

            if blur_type == "gaussian":

                blurred_face = gaussian_blur(
                    face,
                    blur_strength
                )

            elif blur_type == "pixel":

                blurred_face = pixelate(
                    face,
                    blur_strength
                )

            else:

                blurred_face = face

            output[
                y:y+h,
                x:x+w
            ] = blurred_face

        return output, len(faces)