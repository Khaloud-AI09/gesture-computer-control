
import cv2
import mediapipe as mp
import pyautogui
import time
import math

# ---------------- SAFETY ----------------
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

# ---------------- SETTINGS ----------------
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

SMOOTHING = 0.35
PINCH_THRESHOLD = 0.045
CLICK_COOLDOWN = 0.6

SCROLL_DEADZONE = 0.018
SCROLL_SENSITIVITY = 3
SCROLL_COOLDOWN = 0.08

VOLUME_COOLDOWN = 0.5
GESTURE_CONFIDENCE = 0.65

screen_width, screen_height = pyautogui.size()

# ---------------- MEDIAPIPE ----------------
options = mp.tasks.vision.GestureRecognizerOptions(
    base_options=mp.tasks.BaseOptions(
        model_asset_path="models/gesture_recognizer.task"
    ),
    running_mode=mp.tasks.vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)

recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(
    options
)

# ---------------- WEBCAM ----------------
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not camera.isOpened():
    print("Could not open webcam. Check camera permissions.")
    recognizer.close()
    raise SystemExit

# ---------------- STATE ----------------
smooth_x = screen_width // 2
smooth_y = screen_height // 2

last_click_time = 0.0
last_scroll_time = 0.0
last_volume_time = 0.0
last_scroll_y = None

start_time = time.perf_counter()

print("\nGesture Computer Control started!")
print("Point with your index finger: Move cursor")
print("Pinch thumb + index: Left click")
print("Victory / Peace + move hand: Scroll")
print("Thumbs up: Volume up")
print("Thumbs down: Volume down")
print("Press Q to quit.")
print("Move mouse to top-left corner for emergency stop.\n")

try:
    while True:
        success, frame = camera.read()

        if not success:
            continue

        # Mirror webcam preview
        frame = cv2.flip(frame, 1)

        # Reduce processing load
        small_frame = cv2.resize(
            frame, (320, 240),
            interpolation=cv2.INTER_AREA
        )

        rgb_frame = cv2.cvtColor(
            small_frame, cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        timestamp_ms = int(
            (time.perf_counter() - start_time) * 1000
        )

        result = recognizer.recognize_for_video(
            mp_image, timestamp_ms
        )

        status = "Show one hand"

        if result.hand_landmarks:
            landmarks = result.hand_landmarks[0]

            # Read the most confident recognized gesture
            gesture_name = "Unknown"
            gesture_score = 0.0

            if result.gestures and result.gestures[0]:
                category = result.gestures[0][0]
                gesture_name = category.category_name
                gesture_score = category.score

            if gesture_score < GESTURE_CONFIDENCE:
                gesture_name = "Unknown"

            index_tip = landmarks[8]
            thumb_tip = landmarks[4]

            # -------- CURSOR MOVEMENT --------
            # Keep cursor active for ordinary hand poses.
            # Thumbs-up/down and Victory are reserved controls.
            if gesture_name not in (
                "Victory", "Thumb_Up", "Thumb_Down"
            ):
                target_x = int(index_tip.x * screen_width)
                target_y = int(index_tip.y * screen_height)

                smooth_x += int(
                    (target_x - smooth_x) * SMOOTHING
                )
                smooth_y += int(
                    (target_y - smooth_y) * SMOOTHING
                )

                smooth_x = max(
                    0, min(screen_width - 1, smooth_x)
                )
                smooth_y = max(
                    0, min(screen_height - 1, smooth_y)
                )

                pyautogui.moveTo(smooth_x, smooth_y)

                status = "Cursor control"

            current_time = time.perf_counter()

            # -------- PINCH TO CLICK --------
            pinch_distance = math.hypot(
                thumb_tip.x - index_tip.x,
                thumb_tip.y - index_tip.y
            )

            if (
                pinch_distance < PINCH_THRESHOLD
                and gesture_name not in (
                    "Victory", "Thumb_Up", "Thumb_Down"
                )
                and current_time - last_click_time
                >= CLICK_COOLDOWN
            ):
                pyautogui.click()
                last_click_time = current_time
                status = "Left click!"

            # -------- VICTORY TO SCROLL --------
            if gesture_name == "Victory":
                status = "Scroll mode - move hand up/down"

                current_y = index_tip.y

                if last_scroll_y is not None:
                    movement = last_scroll_y - current_y

                    if (
                        abs(movement) > SCROLL_DEADZONE
                        and current_time - last_scroll_time
                        >= SCROLL_COOLDOWN
                    ):
                        amount = int(
                            movement * 100 * SCROLL_SENSITIVITY
                        )

                        # Keep each scroll step small
                        amount = max(-5, min(5, amount))

                        if amount != 0:
                            pyautogui.scroll(amount)
                            last_scroll_time = current_time

                last_scroll_y = current_y
            else:
                last_scroll_y = None

            # -------- THUMBS UP/DOWN: VOLUME --------
            if (
                gesture_name in ("Thumb_Up", "Thumb_Down")
                and current_time - last_volume_time
                >= VOLUME_COOLDOWN
            ):
                if gesture_name == "Thumb_Up":
                    pyautogui.press("volumeup")
                    status = "Volume up!"
                else:
                    pyautogui.press("volumedown")
                    status = "Volume down!"

                last_volume_time = current_time

            # Draw index fingertip on preview
            px = int(index_tip.x * small_frame.shape[1])
            py = int(index_tip.y * small_frame.shape[0])

            cv2.circle(
                small_frame, (px, py), 7, (0, 255, 0), -1
            )

            cv2.putText(
                small_frame,
                f"Gesture: {gesture_name}",
                (10, 55),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 0), 1
            )

        else:
            last_scroll_y = None

        # -------- ON-SCREEN STATUS --------
        cv2.putText(
            small_frame, status, (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55, (0, 255, 0), 2
        )

        cv2.putText(
            small_frame, "Q = Quit | Top-left = Emergency stop",
            (10, 225), cv2.FONT_HERSHEY_SIMPLEX,
            0.35, (255, 255, 255), 1
        )

        cv2.imshow("Gesture Computer Control", small_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except pyautogui.FailSafeException:
    print("Emergency stop activated.")

finally:
    camera.release()
    cv2.destroyAllWindows()
    recognizer.close()
    print("Gesture control stopped safely.")
