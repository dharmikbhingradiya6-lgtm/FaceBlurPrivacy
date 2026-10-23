# 🛡️ FaceBlurPrivacy: Privacy Protection System

A computer vision-powered privacy protection system that automatically detects human faces in images, recorded videos, and live webcam streams, applying real-time face blurring or pixelation to safeguard individual identities.

---

## 📌 Features

- **Multi-Source Support:**
  - 🖼️ **Image Blurring:** Process `.jpg`, `.png`, and other image formats.
  - 🎥 **Video Blurring:** Batch-process recorded videos (`.mp4`) with synchronized audio and video frames.
  - 📹 **Live Webcam Blurring:** Real-time webcam privacy filter with high FPS.
- **Multiple Blurring Modes:**
  - **Gaussian Blur:** Smooth, high-intensity blurring.
  - **Pixelate:** Retro mosaic / pixelation effect.
- **Advanced Computer Vision Capabilities:**
  - Powered by **MediaPipe Face Detection** and **OpenCV** for accurate multi-face tracking.
  - **Hand Gesture & Finger Targeting:** Detect hand gestures and point towards specific faces for selective blurring/unblurring.
- **User-Friendly Desktop GUI:**
  - Built with **Tkinter** and **PIL** for a smooth, intuitive desktop user experience.
  - Easy controls to select input files, adjust blur strength, toggle effects, and view processed outputs.

---

## 🛠️ Tech Stack & Requirements

- **Language:** Python 3.9+ (Python 3.11 recommended)
- **Computer Vision:** OpenCV (`opencv-python`), MediaPipe (`mediapipe`)
- **Numerical Processing:** NumPy
- **GUI & Imaging:** Tkinter, Pillow (`PIL`)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/dharmikbhingradiya6-lgtm/FaceBlurPrivacy.git
cd FaceBlurPrivacy
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Launch the desktop GUI:

```bash
python app.py
```

Or run standalone modules directly:
- **Webcam Mode:** `python webcam_blur.py`
- **Image Mode:** `python image_blur.py`
- **Video Mode:** `python video_blur.py`

---

## 📂 Project Structure

```text
FaceBlurPrivacy/
├── assets/             # Project assets and documentation media
├── input/              # Sample input media
│   ├── images/         # Input test images
│   └── videos/         # Input test videos
├── output/             # Saved processed results
├── about project.txt   # Project overview notes
├── app.py              # Main application entry point (GUI launcher)
├── face_detector.py    # MediaPipe face detection module
├── finger_target.py    # Finger direction & target calculation logic
├── gui.py              # Tkinter graphical user interface
├── hand_detector.py    # MediaPipe hand tracking & gesture module
├── image_blur.py       # Image processing pipeline
├── utils.py            # Gaussian blur & pixelate utility functions
├── video_blur.py       # Video processing pipeline
├── webcam_blur.py      # Real-time webcam stream pipeline
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
