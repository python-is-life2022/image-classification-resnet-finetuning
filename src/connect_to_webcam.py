import cv2
import keras
import numpy as np
from keras import models

model = models.load_model("C:/Users/amirm/webcam_resnet_transfer_learning/webcam_model_transfer_learning_resnet50.keras")

capture = cv2.VideoCapture(0)
if not capture.isOpened():
    capture = cv2.VideoCapture(1)

while True:
    is_success, frame = capture.read()
    if not is_success:
        break
    image = cv2.resize(frame, (224, 224))
    image = keras.applications.resnet50.preprocess_input(image.astype('float32'))
    image = np.expand_dims(image, axis= 0)
    prediction = model.predict(image)
    cv2.imshow("Object Detections", frame)
    if cv2.waitKey(1) == 27:
        break
    print(prediction)
    
capture.release()
cv2.destroyAllWindows()