// used libs: ESP32Servo , ros_lib/rosserial

#include <ros.h>
#include <std_msgs/String.h>
#include <ESP32Servo.h>  
#include <WiFi.h>

const char* ssid = "";
const char* password = "";

ros::NodeHandle nh;
Servo servo1;  //test

void commandCallback(const std_msgs::String &msg);

ros::Subscriber<std_msgs::String> sub("motion_command", &commandCallback);

void setup() {   
    Serial.begin(115200); 

    //connect to wifi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi!");
    Serial.println(WiFi.localIP()); // hnhtag el esp32's IP da b3den

    //test
    servo1.attach(18,500,2400); 

    nh.initNode();
    nh.subscribe(sub);
}

void loop() {
    nh.spinOnce();  //handle incoming mesages
    delay(10);
}

void commandCallback(const std_msgs::String &msg) {
    String command = msg.data; 

    //test
    if (command =="MOVE_SERVO") {
        servo1.write(90);  
    } else if (command=="RESET_SERVO") {
        servo1.write(0);   
    }
}
