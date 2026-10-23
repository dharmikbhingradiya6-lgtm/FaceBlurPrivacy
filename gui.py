import tkinter as tk

from tkinter import filedialog
from tkinter import messagebox

import cv2
import os
import time
import threading

from PIL import Image
from PIL import ImageTk

from image_blur import FaceBlur
from video_blur import VideoBlur
from webcam_blur import WebcamBlur


class PrivacyShield:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Privacy Shield"
        )

        self.root.geometry(
            "700x750"
        )

        self.root.resizable(
            False,
            False
        )

        os.makedirs(
            "output",
            exist_ok=True
        )

        self.selected_file = None

        self.blur_type = (
            tk.StringVar(
                value="gaussian"
            )
        )

        self.blur_strength = (
            tk.IntVar(
                value=101
            )
        )

        self.create_interface()

    def create_interface(self):

        title = tk.Label(
            self.root,
            text="PRIVACY SHIELD",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=15)

        subtitle = tk.Label(
            self.root,
            text=(
                "Automatic Face Detection "
                "and Privacy Protection"
            ),
            font=("Arial", 12)
        )

        subtitle.pack()

        tk.Label(
            self.root,
            text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            font=("Arial", 12)
        ).pack()

        self.file_button = tk.Button(
            self.root,
            text="📁 Select Image / Video",
            font=("Arial", 13),
            width=28,
            height=2,
            command=self.select_file
        )

        self.file_button.pack(
            pady=15
        )

        self.file_label = tk.Label(
            self.root,
            text="No file selected",
            font=("Arial", 10)
        )

        self.file_label.pack()

        mode_frame = tk.LabelFrame(
            self.root,
            text=" Blur Method ",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )

        mode_frame.pack(
            pady=20
        )

        tk.Radiobutton(
            mode_frame,
            text="Gaussian Blur",
            variable=self.blur_type,
            value="gaussian",
            font=("Arial", 11)
        ).pack(
            side="left",
            padx=20
        )

        tk.Radiobutton(
            mode_frame,
            text="Pixelation",
            variable=self.blur_type,
            value="pixel",
            font=("Arial", 11)
        ).pack(
            side="left",
            padx=20
        )

        strength_frame = tk.LabelFrame(
            self.root,
            text=" Blur Strength ",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )

        strength_frame.pack(
            pady=10
        )

        self.strength_slider = tk.Scale(
            strength_frame,
            from_=11,
            to=201,
            resolution=2,
            orient="horizontal",
            variable=self.blur_strength,
            length=400,
            command=self.update_strength
        )

        self.strength_slider.pack()

        self.strength_label = tk.Label(
            strength_frame,
            text="Strength: 101",
            font=("Arial", 10)
        )

        self.strength_label.pack()

        button_frame = tk.Frame(
            self.root
        )

        button_frame.pack(
            pady=20
        )

        tk.Button(
            button_frame,
            text="🖼 Process Image",
            font=("Arial", 11),
            width=20,
            height=2,
            command=self.process_image
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=5
        )

        tk.Button(
            button_frame,
            text="🎥 Process Video",
            font=("Arial", 11),
            width=20,
            height=2,
            command=self.process_video
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        tk.Button(
            button_frame,
            text="📷 Open Webcam",
            font=("Arial", 11),
            width=20,
            height=2,
            command=self.open_webcam
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            pady=10
        )

        self.status = tk.Label(
            self.root,
            text="Status: Ready",
            font=("Arial", 11)
        )

        self.status.pack(
            pady=10
        )

        self.face_count_label = tk.Label(
            self.root,
            text="Faces Detected: --",
            font=("Arial", 12, "bold")
        )

        self.face_count_label.pack(
            pady=5
        )

        tk.Label(
            self.root,
            text="Output folder: ./output/",
            font=("Arial", 9)
        ).pack(
            pady=10
        )

        tk.Button(
            self.root,
            text="Exit",
            font=("Arial", 11),
            width=12,
            command=self.root.destroy
        ).pack(
            pady=5
        )

    def update_strength(self, value):

        self.strength_label.config(
            text=f"Strength: {int(float(value))}"
        )

    def select_file(self):

        file_path = filedialog.askopenfilename(
            title="Select Image or Video",
            filetypes=[
                (
                    "Images",
                    "*.jpg *.jpeg *.png *.bmp"
                ),
                (
                    "Videos",
                    "*.mp4 *.avi *.mov"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if file_path:

            self.selected_file = file_path

            self.file_label.config(
                text=os.path.basename(
                    file_path
                )
            )

            self.status.config(
                text="Status: File selected"
            )

    def process_image(self):

        if not self.selected_file:

            messagebox.showwarning(
                "No File",
                "Please select an image."
            )

            return

        extension = (
            os.path.splitext(
                self.selected_file
            )[1].lower()
        )

        if extension not in [
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp"
        ]:

            messagebox.showerror(
                "Invalid File",
                "Please select an image."
            )

            return

        image = cv2.imread(
            self.selected_file
        )

        if image is None:

            messagebox.showerror(
                "Error",
                "Could not read image."
            )

            return

        self.status.config(
            text="Status: Processing image..."
        )

        self.root.update()

        start = time.time()

        blur = FaceBlur()

        output, face_count = (
            blur.blur_faces(
                image,
                self.blur_type.get(),
                self.blur_strength.get()
            )
        )

        processing_time = (
            time.time() - start
        )

        output_path = (
            "output/"
            "privacy_image_"
            + time.strftime(
                "%Y%m%d_%H%M%S"
            )
            + ".jpg"
        )

        cv2.imwrite(
            output_path,
            output
        )

        self.face_count_label.config(
            text=(
                f"Faces Detected: "
                f"{face_count}"
            )
        )

        self.status.config(
            text=(
                f"Status: Completed "
                f"({processing_time:.2f}s)"
            )
        )

        self.show_comparison(
            image,
            output
        )

        messagebox.showinfo(
            "Processing Complete",
            (
                f"Faces detected: "
                f"{face_count}\n\n"
                f"Processing time: "
                f"{processing_time:.2f} seconds\n\n"
                f"Saved to:\n"
                f"{output_path}"
            )
        )

    def show_comparison(
        self,
        original,
        processed
    ):

        original_rgb = cv2.cvtColor(
            original,
            cv2.COLOR_BGR2RGB
        )

        processed_rgb = cv2.cvtColor(
            processed,
            cv2.COLOR_BGR2RGB
        )

        original_pil = Image.fromarray(
            original_rgb
        )

        processed_pil = Image.fromarray(
            processed_rgb
        )

        original_pil.thumbnail(
            (300, 300)
        )

        processed_pil.thumbnail(
            (300, 300)
        )

        comparison = tk.Toplevel(
            self.root
        )

        comparison.title(
            "Before / After"
        )

        tk.Label(
            comparison,
            text="Original",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        tk.Label(
            comparison,
            text="Protected",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        original_photo = ImageTk.PhotoImage(
            original_pil
        )

        processed_photo = ImageTk.PhotoImage(
            processed_pil
        )

        original_label = tk.Label(
            comparison,
            image=original_photo
        )

        original_label.grid(
            row=1,
            column=0,
            padx=10
        )

        processed_label = tk.Label(
            comparison,
            image=processed_photo
        )

        processed_label.grid(
            row=1,
            column=1,
            padx=10
        )

        original_label.image = (
            original_photo
        )

        processed_label.image = (
            processed_photo
        )

    def process_video(self):

        if not self.selected_file:

            messagebox.showwarning(
                "No File",
                "Please select a video."
            )

            return

        extension = (
            os.path.splitext(
                self.selected_file
            )[1].lower()
        )

        if extension not in [
            ".mp4",
            ".avi",
            ".mov"
        ]:

            messagebox.showerror(
                "Invalid File",
                "Please select a video."
            )

            return

        output_path = (
            "output/"
            "privacy_video_"
            + time.strftime(
                "%Y%m%d_%H%M%S"
            )
            + ".mp4"
        )

        self.status.config(
            text="Status: Processing video..."
        )

        def run():

            video = VideoBlur()

            success = (
                video.process_video(
                    self.selected_file,
                    output_path,
                    self.blur_type.get(),
                    self.blur_strength.get()
                )
            )

            if success:

                self.status.config(
                    text="Status: Video completed"
                )

                messagebox.showinfo(
                    "Complete",
                    (
                        "Video processing "
                        "completed.\n\n"
                        f"Saved to:\n"
                        f"{output_path}"
                    )
                )

            else:

                self.status.config(
                    text="Status: Video failed"
                )

                messagebox.showerror(
                    "Error",
                    "Video processing failed."
                )

        threading.Thread(
            target=run,
            daemon=True
        ).start()

    def open_webcam(self):

        self.status.config(
            text="Status: Webcam running..."
        )

        def run():

            webcam = WebcamBlur()

            webcam.start(
                self.blur_type.get(),
                self.blur_strength.get()
            )

            self.status.config(
                text="Status: Webcam stopped"
            )

        threading.Thread(
            target=run,
            daemon=True
        ).start()


if __name__ == "__main__":

    root = tk.Tk()

    app = PrivacyShield(
        root
    )

    root.mainloop()