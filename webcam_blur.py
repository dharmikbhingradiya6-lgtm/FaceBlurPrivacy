# import cv2
# import time

# from face_detector import FaceDetector
# from utils import gaussian_blur, pixelate


# class WebcamBlur:

#     def __init__(self):

#         self.detector = FaceDetector()

#     def start(
#         self,
#         blur_type="gaussian",
#         blur_strength=101
#     ):

#         camera = cv2.VideoCapture(0)

#         if not camera.isOpened():

#             print(
#                 "Error: Could not open webcam."
#             )

#             return

#         previous_time = time.time()

#         while True:

#             success, frame = camera.read()

#             if not success:

#                 print(
#                     "Error: Could not read frame."
#                 )

#                 break

#             faces = (
#                 self.detector.detect_faces(
#                     frame
#                 )
#             )

#             for (x, y, w, h) in faces:

#                 x = max(0, x)
#                 y = max(0, y)

#                 w = min(
#                     w,
#                     frame.shape[1] - x
#                 )

#                 h = min(
#                     h,
#                     frame.shape[0] - y
#                 )

#                 if w <= 0 or h <= 0:

#                     continue

#                 face = frame[
#                     y:y+h,
#                     x:x+w
#                 ]

#                 if face.size == 0:

#                     continue

#                 if blur_type == "gaussian":

#                     blurred_face = (
#                         gaussian_blur(
#                             face,
#                             blur_strength
#                         )
#                     )

#                 else:

#                     blurred_face = (
#                         pixelate(
#                             face,
#                             blur_strength
#                         )
#                     )

#                 frame[
#                     y:y+h,
#                     x:x+w
#                 ] = blurred_face

#             current_time = time.time()

#             difference = (
#                 current_time -
#                 previous_time
#             )

#             if difference > 0:

#                 fps = 1 / difference

#             else:

#                 fps = 0

#             previous_time = current_time

#             cv2.putText(
#                 frame,
#                 f"Faces: {len(faces)}",
#                 (20, 40),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 1,
#                 (0, 255, 0),
#                 2
#             )

#             cv2.putText(
#                 frame,
#                 f"FPS: {fps:.2f}",
#                 (20, 80),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 1,
#                 (0, 255, 0),
#                 2
#             )

#             cv2.putText(
#                 frame,
#                 "Press Q to Exit",
#                 (20, 120),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.8,
#                 (0, 255, 0),
#                 2
#             )

#             cv2.imshow(
#                 "Privacy Shield - Webcam",
#                 frame
#             )

#             key = cv2.waitKey(1) & 0xFF

#             if key == ord("q"):

#                 break

#         camera.release()

#         cv2.destroyAllWindows()



import cv2
import time

from face_detector import FaceDetector
from hand_detector import HandDetector

from utils import gaussian_blur, pixelate

from finger_target import is_face_in_direction


class WebcamBlur:

    def __init__(self):

        self.face_detector = FaceDetector()

        self.hand_detector = HandDetector()

    def start(
        self,
        blur_type="gaussian",
        blur_strength=101
    ):

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():

            print(
                "Error: Could not open webcam."
            )

            return

        previous_time = time.time()

        while True:

            success, frame = camera.read()

            if not success:

                break

            # --------------------------------
            # FACE DETECTION
            # --------------------------------

            faces = (
                self.face_detector.detect_faces(
                    frame
                )
            )

            # --------------------------------
            # HAND DETECTION
            # --------------------------------

            hands = (
                self.hand_detector.detect_hands(
                    frame
                )
            )

            target_faces = []

            # --------------------------------
            # FIND FACE BEING POINTED AT
            # --------------------------------

            for hand in hands:

                fingertip = hand["fingertip"]

                finger_base = hand["finger_base"]

                for face in faces:

                    if is_face_in_direction(
                        fingertip,
                        finger_base,
                        face
                    ):

                        if face not in target_faces:

                            target_faces.append(
                                face
                            )

            # --------------------------------
            # BLUR TARGET FACES
            # --------------------------------

            for (
                x,
                y,
                w,
                h
            ) in target_faces:

                x = max(0, x)
                y = max(0, y)

                w = min(
                    w,
                    frame.shape[1] - x
                )

                h = min(
                    h,
                    frame.shape[0] - y
                )

                if w <= 0 or h <= 0:

                    continue

                face = frame[
                    y:y+h,
                    x:x+w
                ]

                if face.size == 0:

                    continue

                if blur_type == "gaussian":

                    blurred_face = (
                        gaussian_blur(
                            face,
                            blur_strength
                        )
                    )

                else:

                    blurred_face = (
                        pixelate(
                            face,
                            blur_strength
                        )
                    )

                frame[
                    y:y+h,
                    x:x+w
                ] = blurred_face

            # --------------------------------
            # DRAW FINGER POINT
            # --------------------------------

            for hand in hands:

                fingertip = hand["fingertip"]

                finger_base = hand["finger_base"]

                cv2.circle(
                    frame,
                    fingertip,
                    8,
                    (255, 0, 0),
                    -1
                )

                cv2.line(
                    frame,
                    finger_base,
                    fingertip,
                    (255, 0, 0),
                    3
                )

            # --------------------------------
            # FPS
            # --------------------------------

            current_time = time.time()

            difference = (
                current_time -
                previous_time
            )

            if difference > 0:

                fps = 1 / difference

            else:

                fps = 0

            previous_time = current_time

            # --------------------------------
            # DISPLAY INFORMATION
            # --------------------------------

            cv2.putText(
                frame,
                f"Faces: {len(faces)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Target Faces: {len(target_faces)}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"FPS: {fps:.2f}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Point at a face | Q = Exit",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.imshow(
                "Privacy Shield - Finger Targeting",
                frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):

                break

        camera.release()

        cv2.destroyAllWindows()