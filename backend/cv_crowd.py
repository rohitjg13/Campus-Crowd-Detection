from ultralytics import YOLO

model = YOLO("yolov8x.pt")


results = model.predict("backend/test.jpg")
result = results[0]
box = result.boxes[0]
cords = box.xyxy[0].tolist()
class_id = box.cls[0].item()
conf = box.conf[0].item()
print("Object type:", class_id)
print("Coordinates:", cords)
print("Probability:", conf)
print(result.names)