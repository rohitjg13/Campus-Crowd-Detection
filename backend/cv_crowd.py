from os import system

from picamzero import Camera
from ultralytics import YOLO

model = YOLO("yolov8x.pt")


# results = model.predict("backend/test13.jpg")
camera = Camera()
system("mkdir /tmp/cv")
# camera.start_preview()
camera.take_photo("/tmp/cv/test.jpg")
# camera.take_photo("~/Desktop/test.jpg")
# camera.stop_preview()
results = model.predict("/tmp/cv/test.jpg")
# system("rm -rf /tmp/cv")
result = results[0]
people = 0
for box in result.boxes:
    if (
        box.cls[0] == 0 # and box.conf[0] > 0.75
    ):  # TODO: tweak probability threshold with representative images
        print(f" Person detected: {box.conf[0]}")
        people += 1
print(f" Number of people detected: {people}")
