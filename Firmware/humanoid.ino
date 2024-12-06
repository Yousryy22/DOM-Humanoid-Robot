#include <ros.h>
#include <std_msgs/String.h>
#include <ESP32Servo.h>
#include <WiFi.h>

const char* ssid = "";
const char* password = "";

ros::NodeHandle nh;

// Servo objects for the robot's limbs (arms and legs)
Servo arm1, arm2;  // Arm servos
Servo leg1, leg2;  // Leg servos

bool isMoving = false;  // Flag to ensure one movement happens at a time

void commandCallback(const std_msgs::String &msg);

ros::Subscriber<std_msgs::String> sub("motion_command", &commandCallback);

// Movement functions
void moveForward();
void moveRight();
void moveLeft();
void stopMovement();

void setup() {
    Serial.begin(115200); 

    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi!");
    Serial.println(WiFi.localIP()); // Display ESP32's IP address

    // Attach servos to GPIO pins
    arm1.attach(18, 500, 2400);  // Arm1 (shoulder)
    arm2.attach(19, 500, 2400);  // Arm2 (elbow)
    leg1.attach(21, 500, 2400);  // Leg1 (hip)
    leg2.attach(22, 500, 2400);  // Leg2 (knee)

    nh.initNode();
    nh.subscribe(sub);
}

void loop() {
    nh.spinOnce();  // Handle incoming messages
    delay(10);
}

void commandCallback(const std_msgs::String &msg) {
    String command = msg.data; 

    if (isMoving) {
        Serial.println("Already moving, please wait...");
        return;  // Ignore new commands if movement is already in progress
    }

    // Handle incoming commands and execute corresponding actions
    if (command == "MOVE_FORWARD") {
        isMoving = true;  // Set flag to indicate movement is happening
        moveForward();
    } else if (command == "MOVE_RIGHT") {
        isMoving = true;
        moveRight();
    } else if (command == "MOVE_LEFT") {
        isMoving = true;
        moveLeft();
    } else if (command == "STOP") {
        isMoving = true;
        stopMovement();
    }
}

// Example movement functions

void moveForward() {
    // Arms and legs move in sync to simulate forward motion
    arm1.write(45);  // Move arm1 forward (shoulder)
    arm2.write(135); // Move arm2 forward (elbow)
    leg1.write(60);  // Move leg1 forward (hip)
    leg2.write(120); // Move leg2 forward (knee)
    delay(1000);     // Wait for 1 second to complete movement
    stopMovement();  // Stop after moving forward
}

void moveRight() {
    // Arms and legs move to simulate turning right
    arm1.write(90);  // Keep arm1 neutral
    arm2.write(90);  // Keep arm2 neutral
    leg1.write(120); // Move leg1 right (hip)
    leg2.write(90);  // Keep leg2 neutral
    delay(1000);     // Wait for 1 second to complete movement
    stopMovement();  // Stop after turning right
}

void moveLeft() {
    // Arms and legs move to simulate turning left
    arm1.write(90);  // Keep arm1 neutral
    arm2.write(90);  // Keep arm2 neutral
    leg1.write(60);  // Move leg1 left (hip)
    leg2.write(90);  // Keep leg2 neutral
    delay(1000);     // Wait for 1 second to complete movement
    stopMovement();  // Stop after turning left
}

void stopMovement() {
    // Reset all servos to neutral position (standing position)
    arm1.write(90);  // Reset arm1
    arm2.write(90);  // Reset arm2
    leg1.write(90);  // Reset leg1
    leg2.write(90);  // Reset leg2
    delay(500);      // Wait to stop
    isMoving = false; // Reset the flag to allow new commands
    Serial.println("Movement stopped.");
}
