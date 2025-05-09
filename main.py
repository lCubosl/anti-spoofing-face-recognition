# For better performance
# 1.uninstall torch, torchvideo, torchaudio
# 2.go to https://pytorch.org/get-started/locally/
# 3.setup according to your system specifications and then copy the "run this command" 
# this runs pytorch locally on your gpu (before: 10fps | after: 30/35fps)

from ultralytics import YOLO
import cv2
import cvzone
import math
import time

confidence = 0.6

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

model = YOLO("../models/n_version2.pt")

classNames = ["fake", "real"]

prev_frame_time = 0
new_frame_time = 0

while True:
  new_frame_time = time.time()
  success, img = cap.read()
  results = model(img, stream=True, verbose=False)

  for r in results:
    boxes = r.boxes
    for box  in boxes:
      x1, y1, x2, y2 = box.xyxy[0]
      x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2),

      w, h = x2 - x1, y2 - y1

      conf = math.ceil((box.conf[0] * 100)) /100
      cls = int(box.cls[0])

      if conf > confidence:
        if classNames[cls] == 'real':
          color = (0, 255, 0)
        else:
          color = (0, 0, 255)

        cvzone.cornerRect(img, (x1, y1, w, h), colorC=color, colorR=color)
        cvzone.putTextRect(img, 
                           f"{classNames[cls].upper()} {int(conf*100)}%", 
                           (max(0, x1), 
                            max(35, y1)), 
                            scale=2, 
                            thickness=4,
                            colorR= color,
                            colorB= color
                            )
        
  
  fps = 1 / (new_frame_time - prev_frame_time)
  prev_frame_time = new_frame_time
  print(fps)

  cv2.imshow("Image", img)
  cv2.waitKey(1)