import cv2
import time

from image_blur import FaceBlur


class VideoBlur:

    def __init__(self):

        self.face_blur = FaceBlur()

    def process_video(
        self,
        input_path,
        output_path,
        blur_type="gaussian",
        blur_strength=101
    ):

        video = cv2.VideoCapture(input_path)

        if not video.isOpened():

            print("Error: Could not open video.")

            return False

        fps = video.get(
            cv2.CAP_PROP_FPS
        )

        if fps <= 0:

            fps = 30

        width = int(
            video.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        height = int(
            video.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        total_frames = int(
            video.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        fourcc = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        writer = cv2.VideoWriter(
            output_path,
            fourcc,
            fps,
            (width, height)
        )

        if not writer.isOpened():

            print(
                "Error: Could not create output video."
            )

            video.release()

            return False

        frame_count = 0

        total_faces = 0

        start_time = time.time()

        while True:

            success, frame = video.read()

            if not success:

                break

            output_frame, face_count = (
                self.face_blur.blur_faces(
                    frame,
                    blur_type,
                    blur_strength
                )
            )

            total_faces += face_count

            frame_count += 1

            elapsed = time.time() - start_time

            if elapsed > 0:

                processing_fps = (
                    frame_count / elapsed
                )

            else:

                processing_fps = 0

            cv2.putText(
                output_frame,
                f"Faces: {face_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.putText(
                output_frame,
                f"FPS: {processing_fps:.2f}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            writer.write(
                output_frame
            )

            cv2.imshow(
                "Privacy Shield - Video",
                output_frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):

                break

        video.release()

        writer.release()

        cv2.destroyAllWindows()

        processing_time = (
            time.time() - start_time
        )

        print()
        print(
            "========== VIDEO STATISTICS =========="
        )
        print(
            "Frames Processed:",
            frame_count
        )
        print(
            "Total Faces Detected:",
            total_faces
        )
        print(
            "Processing Time:",
            f"{processing_time:.2f} seconds"
        )
        print(
            "Output:",
            output_path
        )
        print(
            "======================================"
        )

        return True