
# Gesture Computer Control 

An AI-powered, real-time hand gesture recognition system that lets users control basic computer functions using a webcam.

This project uses Python, OpenCV, and Google's MediaPipe Gesture Recognizer to detect hand landmarks and recognize gestures. The detected hand positions and gestures are mapped to mouse and system actions.

## ✨ Features

- **Cursor movement:** Move the mouse using your index fingertip.
- **Left-click:** Pinch your thumb and index finger together.
- **Scrolling:** Use the Victory/Peace gesture and move your hand vertically.
- **Volume up:** Show a thumbs-up gesture.
- **Volume down:** Show a thumbs-down gesture.
- **Safety controls:** Press `Q` to quit or use the PyAutoGUI corner failsafe.

##  Technologies Used

- Python
- OpenCV — webcam capture and preview
- MediaPipe — hand landmark detection and gesture recognition
- PyAutoGUI — mouse and volume-key control

##  How It Works

1. OpenCV captures frames from the webcam.
2. MediaPipe processes the frames to detect hand landmarks and classify recognized gestures.
3. The program tracks the index fingertip to calculate cursor coordinates.
4. The distance between the thumb and index fingertip is used to detect a pinch for clicking.
5. Recognized gestures trigger scrolling or volume-key actions through PyAutoGUI.

The project uses a pre-trained MediaPipe model rather than training a custom model from scratch.

##  Gesture-to-Action Mapping

| Hand input | Computer action |
|---|---|
| Index fingertip movement | Move cursor |
| Thumb and index pinch | Left-click |
| Victory/Peace gesture + vertical movement | Scroll |
| Thumbs up | Increase volume |
| Thumbs down | Decrease volume |
| Press `Q` | Exit program |

##  Requirements

- Python 3.12 (or another compatible Python version)
- A working webcam
- Windows or another supported desktop environment
- The MediaPipe model file at `models/gesture_recognizer.task`

##  Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd gesture-computer-control
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Add the model

Place the official MediaPipe Gesture Recognizer model at:

`models/gesture_recognizer.task`

The model file is required to run the program.

### 5. Run the project

```powershell
python main.py
```

Press `Q` to exit.

##  Safety and Limitations

- Mouse and volume actions are performed on the local computer.
- Gesture recognition may vary with lighting, camera quality, and hand position.
- The system requires camera access and a compatible webcam.
- Use the emergency stop if mouse movement becomes unexpected.
- Avoid testing clicks on sensitive or destructive controls.

## Screenshots and Demo

Project screenshots will be added to the `screenshots/` directory.

A demonstration video can be provided separately with the project submission.

##  Future Improvements

- Customizable gestures and controls
- Better cursor calibration and smoothing
- Adjustable scrolling sensitivity
- Improved gesture confidence and error handling
- A settings interface for accessibility and personalization

##  References

- [MediaPipe Gesture Recognizer](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer)
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/)

---

Developed as a hands-on computer-vision project.
