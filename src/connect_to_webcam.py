import cv2

capture = cv2.VideoCapture(0)
if not capture.isOpened():
    capture = cv2.VideoCapture(1)

while True:
    is_success, frame = capture.read()
    cv2.imshow("Object Detections", frame)
    if cv2.waitKey(1) == 27 or is_success == False:
        break
    
capture.release()
cv2.destroyAllWindows()