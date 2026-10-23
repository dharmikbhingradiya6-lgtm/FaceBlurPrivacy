import cv2
import mediapipe as mp
import math


class HandDetector:

    def __init__(self, confidence=0.5):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=confidence,
            min_tracking_confidence=0.5
        )

    def detect_hands(self, frame):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = self.hands.process(rgb)

        hands = []

        if results.multi_hand_landmarks:

            h, w, _ = frame.shape

            for hand_landmarks in results.multi_hand_landmarks:

                landmarks = []

                for landmark in hand_landmarks.landmark:

                    x = int(landmark.x * w)
                    y = int(landmark.y * h)

                    landmarks.append((x, y))

                fingertip = landmarks[8]
                finger_base = landmarks[5]

                pointing = self.is_pointing(
                    landmarks
                )

                hands.append({
                    "landmarks": landmarks,
                    "fingertip": fingertip,
                    "finger_base": finger_base,
                    "pointing": pointing
                })

        return hands

    def calculate_distance(
        self,
        point1,
        point2
    ):

        x1, y1 = point1
        x2, y2 = point2

        return math.sqrt(
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2
        )

    def is_pointing(self, landmarks):

        # Index finger
        index_tip = landmarks[8]
        index_pip = landmarks[6]

        # Middle finger
        middle_tip = landmarks[12]
        middle_pip = landmarks[10]

        # Ring finger
        ring_tip = landmarks[16]
        ring_pip = landmarks[14]

        # Pinky
        pinky_tip = landmarks[20]
        pinky_pip = landmarks[18]

        index_extended = (
            index_tip[1] < index_pip[1]
        )

        middle_closed = (
            middle_tip[1] > middle_pip[1]
        )

        ring_closed = (
            ring_tip[1] > ring_pip[1]
        )

        pinky_closed = (
            pinky_tip[1] > pinky_pip[1]
        )

        return (
            index_extended
            and middle_closed
            and ring_closed
            and pinky_closed
        )