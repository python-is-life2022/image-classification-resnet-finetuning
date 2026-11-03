import threading
import time
import cv2
import numpy as np
from keras import models

model = models.load_model("C:/Users/amirm/webcam_resnet_transfer_learning/best_fine_tuning_model_parameters.keras")

LABELS = [
    "Mobile phone", "Laptop", "Computer keyboard", "Computer mouse",
    "Headphones", "Computer monitor", "Remote control", "Camera",
    "Book", "Pen", "Scissors", "Calculator",
    "Mug", "Bottle", "Coffee cup", "Plate", "Bowl", "Spoon", "Fork", "Knife",
    "Glasses", "Watch", "Backpack", "Clock",
    "Banana", "Apple", "Orange",
    "Person", "Human face", "Human hand",
]
THRESHOLD = 0.5

lock = threading.Lock()
latest_frame = None      
latest_pred = None       
running = True

def inference_loop():
    global latest_pred
    smooth = None
    while running:
        with lock:
            frame = None if latest_frame is None else latest_frame.copy()
        if frame is None:
            time.sleep(0.01)
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.resize(rgb, (224, 224)).astype("float32")[None]
        pred = model(image, training=False).numpy()[0]

        smooth = pred if smooth is None else 0.6 * smooth + 0.4 * pred  
        with lock:
            latest_pred = smooth

threading.Thread(target=inference_loop, daemon=True).start()

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)       
if not capture.isOpened():
    capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    is_success, frame = capture.read()
    if not is_success:
        break

    with lock:
        latest_frame = frame
        pred = latest_pred

    if pred is not None:
        found = [(LABELS[i], p) for i, p in enumerate(pred) if p >= THRESHOLD]
        found.sort(key=lambda x: x[1], reverse=True)
        y = 30
        for name, p in found:
            text = f"{name}: {p:.2f}"
            cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 4)
            cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            y += 30

    cv2.imshow("Object Detections", frame)
    if cv2.waitKey(1) == 27:
        break

running = False
capture.release()
cv2.destroyAllWindows()