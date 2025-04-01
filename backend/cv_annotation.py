from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("yolov10x.pt")

image_path = "/tmp/cv/test.jpg"

results = model.predict(image_path)
result = results[0]

image = cv2.imread(image_path)

people = 0
for box in result.boxes:
    if box.cls[0] == 0:
        people += 1
        
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
        confidence = float(box.conf[0])
        
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        label = f"Person: {confidence:.2f}"
        cv2.putText(image, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        print(f"Person {people} detected with probability: {confidence:.2f}")

cv2.putText(image, f"Total people: {people}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

print(f"Number of people detected: {people}")

output_path = "detected_peoplev10.jpg"
cv2.imwrite(output_path, image)
print(f"Annotated image saved to {output_path}")