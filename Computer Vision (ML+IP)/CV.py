# pip install opencv-python
# pip install ultralytics

import cv2
from ultralytics import YOLO

# Load the YOLO v8 model (e.g., pre-trained on the COCO dataset)
model = YOLO('yolov8n.pt')  # Using the nano model for better speed

# the following lines used if we want to train the model ourself 
# model.train(
#   data='path/to/your/dataset.yaml',  # Path to the dataset YAML file containing training configuration
#   epochs=50,  # Number of epochs for training
#    imgsz=640,  # Image size
#    batch=8  # Batch size
#)


# Define a function to run YOLO on an image or video frame
def detect_objects(frame):
    results = model(frame)  # Perform detection
    for result in results:  # Process each detection
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            conf = box.conf[0]  # Confidence score
            cls = int(box.cls[0])  # Class ID

            # Draw bounding boxes and labels
            label = f"{model.names[cls]} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return frame


# Set up video capture from the ESP32 camera stream
esp32_ip = "<ESP32_IP>"  # Replace with your ESP32 camera IP
stream_url = f"http://{esp32_ip}/stream"
cap = cv2.VideoCapture(stream_url)

# Main loop to process video frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run object detection on the frame
    output_frame = detect_objects(frame)

    # Display the resulting frame
    cv2.imshow("YOLO v8 Detection", output_frame)

    # Exit with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
