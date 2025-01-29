//rosrun rosserial_python serial_node.py _port:=/dev/ttyUSB0 _baud:=115200


#include <ESP32Servo.h>
#include <ros.h>
#include <std_msgs/String.h>

// Servo objects for the robot's limbs (arms and legs)
Servo left_leg_upper, left_leg_middle, left_foot, left_leg_rotation;
Servo right_leg_upper, right_leg_middle, right_foot, right_leg_rotation;

// ROS node handle
ros::NodeHandle nh;

// Movement functions
void moveForward() {
  left_leg_rotation.write(56);
  right_leg_rotation.write(100);
  left_leg_upper.write(55);
  right_leg_upper.write(125);
  delay(350);
  left_leg_rotation.write(78);
  right_leg_rotation.write(78);
  left_leg_upper.write(60);
  right_leg_upper.write(120);
  delay(500);
}

void moveLeft() {
  left_leg_upper.write(65);
  right_leg_upper.write(112);
  left_leg_rotation.write(0);
  right_leg_rotation.write(0);
  delay(500);
  left_leg_upper.write(70);
  right_leg_upper.write(108);
  right_leg_rotation.write(90);
  left_leg_rotation.write(90);
  delay(1000);
}

void moveRight() {
  left_leg_upper.write(65);
  right_leg_upper.write(112);
  left_leg_rotation.write(140);
  right_leg_rotation.write(140);
  delay(800);
  left_leg_upper.write(70);
  right_leg_upper.write(108);
  right_leg_rotation.write(90);
  left_leg_rotation.write(90);
  delay(800);
}

void moveReverse() {
  for (int i = 0; i < 2; i++) {
    left_leg_upper.write(65);
    right_leg_upper.write(112);
    left_leg_rotation.write(0);
    right_leg_rotation.write(0);
    delay(800);
    left_leg_upper.write(70);
    right_leg_upper.write(108);
    right_leg_rotation.write(90);
    left_leg_rotation.write(90);
    delay(800);
  }
}

// Callback function for the servo_motion topic
void servoMotionCallback(const std_msgs::String& msg) {
  if (strcmp(msg.data, "forward") == 0) {
    moveForward();
  } else if (strcmp(msg.data, "left") == 0) {
    moveLeft();
  } else if (strcmp(msg.data, "right") == 0) {
    moveRight();
  } else if (strcmp(msg.data, "reverse") == 0) {
    moveReverse();
  }
}

// ROS subscriber
ros::Subscriber<std_msgs::String> sub("servo_motion", &servoMotionCallback);

void setup() {
  // Initialize servos
  Serial.begin(115200);
  nh.getHardware()->setBaud(115200);
  left_leg_upper.attach(33);
  left_leg_middle.attach(25);
  left_foot.attach(26);
  left_leg_rotation.attach(32);
  right_leg_upper.attach(21);
  right_leg_middle.attach(19);
  right_foot.attach(17);
  right_leg_rotation.attach(16);
  
  left_leg_upper.write(90);
  delay(50);
  left_leg_middle.write(90);
  delay(50);
  left_foot.write(90);
  delay(50);
  left_leg_rotation.write(90);
  delay(50);
  right_leg_upper.write(90);
  delay(50);
  right_leg_middle.write(90);
  delay(50);
  right_foot.write(90);
  delay(50);
  right_leg_rotation.write(90);
  delay(50);

  // Initialize ROS node
  nh.initNode();
  nh.subscribe(sub);
}

void loop() {
  // Handle ROS callbacks
  nh.spinOnce();
  delay(1);
}
