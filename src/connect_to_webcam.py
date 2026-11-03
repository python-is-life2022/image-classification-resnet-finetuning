import cv2
import numpy as np
from keras import models

model = models.load_model("C:/Users/amirm/webcam_resnet_transfer_learning/best_model_transfer_learning.keras")

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

capture = cv2.VideoCapture(0)
if not capture.isOpened():
    capture = cv2.VideoCapture(1)

while True:
    is_success, frame = capture.read()
    if not is_success:
        break
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image = np.expand_dims(image, axis= 0)
    prediction = model(image, training=False).numpy()[0]
    found = [(LABELS[i], p) for i, p in enumerate(prediction) if p >= THRESHOLD]
    found.sort(key=lambda x: x[1], reverse=True)

    y = 30
    for name, p in found:
        text = f"{name}: {p:.2f}"
        cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 4)    # حاشیه‌ی مشکی
        cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)  # متن سبز
        y += 30

    cv2.imshow("Object Detections", frame)
    if cv2.waitKey(1) == 27:
        break
    print(prediction)
    
capture.release()
cv2.destroyAllWindows()