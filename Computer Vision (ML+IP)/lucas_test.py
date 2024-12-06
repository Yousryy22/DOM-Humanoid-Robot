from ultralytics import YOLO
import cv2
import numpy as np

class InvalidTarget(Exception):
    pass

class ObjectDetector:
    def __init__(self,model_path='yolov8n.pt',target_object=None):
        self.model= YOLO(model_path)
        self.target_object = target_object.lower() if target_object else None

        if self.target_object and self.target_object not in [name.lower() for name in self.model.names.values()]:
            self.target_object = None
            raise InvalidTarget(
                f"error: {self.target_object} can't be detected"
            )

        #lucas parameters
        self.lk_params= dict(winSize=( 15 , 15),maxLevel=2,criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,0.03))
        self.tracking_points= []
        self.prev_gray= None

    def set_target_object(self,target_object):
        self.target_object =target_object.lower()
        if self.target_object not in [name.lower() for name in self.model.names.values()]:
            print(f"error: {self.target_object} can't be detected")
            self.target_object = None

    def detect_objects( self,frame):
        if not self.target_object:
            return frame  #skip for no target obj

        #yolo
        results =self.model(frame)
        gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        new_tracking_points =[]

        #cen. point
        height,width= frame.shape[:2]
        center_x,center_y= width//2 , height//2
        cv2.circle(frame,(center_x , center_y),10,(255,255,0),2)

        found_contours =False #contours flag

        for result in results:
            for box in result.boxes:
                x1, y1,x2,y2 = map(int,box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])
                label = self.model.names[cls].lower()

                if label == self.target_object:
                    found_contours = True
                    display_label = f"{label} {conf:.2f}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, display_label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                    #cen. point of contour
                    obj_center_x, obj_center_y = (x1 + x2) // 2, (y1 + y2) // 2
                    new_tracking_points.append((obj_center_x, obj_center_y))
                    cv2.circle(frame, (obj_center_x, obj_center_y), 5, (0, 0, 255), -1)

        if found_contours:
            #replace lucas point when new one iss formed
            self.tracking_points = np.array(new_tracking_points,dtype=np.float32).reshape(-1,1,2)
        elif self.prev_gray is not None and len(self.tracking_points) >0:

            #depend on lucas pt only if contiurs are lost
            next_points, status,__ =cv2.calcOpticalFlowPyrLK(self.prev_gray,gray_frame ,self.tracking_points,None,**self.lk_params)

            # retain successfully tracked pts
            self.tracking_points = next_points[status.flatten() == 1].reshape(-1, 1, 2)

        #lucas pt :
        for point in self.tracking_points:
            px, py = point.ravel().astype(int)
            distance = np.sqrt((px - center_x) ** 2 + (py - center_y) ** 2)  # Euclidean distance
            cv2.line(frame, (center_x, center_y), (px, py), (0, 255, 255), 1)  # Draw a line to the Lucas point
            cv2.putText(frame,f"Dist: {distance:.2f}",(px,py -10),cv2.FONT_HERSHEY_SIMPLEX, 0.5 ,(255,255,255),1)

        #update gray
        self.prev_gray= gray_frame
        return frame

    def start_video_capture(self):
        if not self.target_object:
            print(" no objects to detect")
            return

        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            output_frame = self.detect_objects(frame)
            cv2.imshow("YOLO v8 Detection", output_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    target_object = input("enter obj to detect: ").strip()
    detector = ObjectDetector(target_object=target_object)
    detector.start_video_capture()
