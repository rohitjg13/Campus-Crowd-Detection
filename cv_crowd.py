from os import system

from picamzero import Camera
from ultralytics import YOLO

model = YOLO("yolov8x.pt")

camera = Camera()
system("mkdir /tmp/cv")
camera.take_photo("/tmp/cv/process.jpg")
results = model.predict("/tmp/cv/process.jpg")
system("rm /tmp/cv/process.jpg")
result = results[0]
probability_threshold = 0.75 # TODO: tweak probability threshold with representative images
people = 0
for box in result.boxes:
    if (
        box.cls[0] == 0 and box.conf[0] > probability_threshold
    ):
        people += 1
print(f" Number of people detected: {people}")
