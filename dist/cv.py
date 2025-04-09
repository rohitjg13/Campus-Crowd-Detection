from picamzero import Camera
from picamzero import Camera
from ultralytics import YOLO
from os import system


def capture_cv_crowd():
    model = YOLO("yolov8x.pt")
    camera = Camera()
    camera.take_photo("/tmp/ccd/process.jpg")
    results = model.predict("/tmp/ccd/process.jpg")
    result = results[0]
    probability_threshold = (
        0.75  # TODO: tweak probability threshold with representative images
    ) sa
    people = 0
    for box in result.boxes:
        if box.cls[0] == 0 and box.conf[0] > probability_threshold:
            people += 1
    return people
