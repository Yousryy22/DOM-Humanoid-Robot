#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def webcam_publisher():
    rospy.init_node('webcam_publisher', anonymous=True)

    # Create a publisher for the image topic
    pub = rospy.Publisher('/webcam/image_raw', Image, queue_size=10)

    # Initialize the CvBridge
    bridge = CvBridge()

    # Open the webcam (0 for default camera)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        rospy.logerr("Error: Could not open webcam.")
        return

    rospy.loginfo("Webcam node started. Publishing video stream...")

    # Set the publishing rate
    rate = rospy.Rate(30)  # 30 frames per second

    while not rospy.is_shutdown():
        # Capture a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            rospy.logerr("Error: Could not read frame from webcam.")
            break

        try:
            # Convert the OpenCV image to a ROS Image message
            ros_image = bridge.cv2_to_imgmsg(frame, encoding="bgr8")

            # Publish the image
            pub.publish(ros_image)
        except Exception as e:
            rospy.logerr(f"Error while publishing frame: {e}")
            break

        # Maintain the desired rate
        rate.sleep()

    # Release the webcam and close the node
    cap.release()
    rospy.loginfo("Webcam node stopped.")

if __name__ == '__main__':
    try:
        webcam_publisher()
    except rospy.ROSInterruptException:
        pass
