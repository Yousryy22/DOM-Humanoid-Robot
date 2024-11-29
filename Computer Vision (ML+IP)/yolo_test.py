from ultralytics import YOLO
import cv2

class InvalidTarget(Exception):
    pass

class ObjectDetector:
    def __init__(self, model_path='yolov8n.pt', target_object=None):
        #model
        self.model = YOLO(model_path)
        self.target_object = target_object.lower() if target_object else None

        # check lw el object mawgoda f yolo wla la
        if self.target_object and self.target_object not in[name.lower() for name in self.model.names.values()]:
            self.target_object= None
            raise InvalidTarget(
                f"error:{self.target_object} cant be detected"
            )

    def set_target_object(self, target_object):
        self.target_object = target_object.lower()
        if self.target_object not in [name.lower() for name in self.model.names.values()]:
            print(f"error:{self.target_object} cant be detected")
            self.target_object = None

    def detect_objects(self, frame):

        if not self.target_object:
            return frame  #skip el camera lw mafish detection

        # el contours
        results = self.model(frame)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])
                label = self.model.names[cls].lower()

                # draw contours 3la el object elly 3ayznha bs
                if label==self.target_object:
                    display_label = f"{label} {conf:.2f}"
                    cv2.rectangle(frame,(x1, y1),(x2,y2),(0, 255 ,0),2)
                    cv2.putText(frame,display_label,(x1,y1 -10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
        return frame

    def start_video_capture(self):
        if not self.target_object:
            print("no objects to detect  ")
            return

        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break


            output_frame= self.detect_objects(frame)

            cv2.imshow("YOLO v8 Detection",output_frame)

             # press q 3shan yrg3 ll chatbot
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    target_object = input("enter obj to detect: ").strip()
    detector=ObjectDetector(target_object=target_object)
    detector.start_video_capture()
