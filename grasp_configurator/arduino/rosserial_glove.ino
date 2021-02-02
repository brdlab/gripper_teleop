// ROS node for wearable microcontroller to control 
// LED output

// Author : Snehal Jain

#include <ros.h>
#include <std_msgs/UInt16.h>

unsigned char LED2=2;
unsigned char LED3=3;
unsigned char LED4=4;
unsigned char LED5=5;

ros::NodeHandle nh;

int l = 0;

void level_cb(const std_msgs::UInt16& led_msg)
{
  l = led_msg.data;
  switch (l) 
 {
  case 0:                // Upon recieeving integer 0
    digitalWrite(LED2,LOW);
    digitalWrite(LED3,LOW);
    digitalWrite(LED4,LOW);
    digitalWrite(LED5,LOW);
    break;
  case 1:                // Upon recieeving integer 1
    digitalWrite(LED2,HIGH);
    digitalWrite(LED3,LOW);
    digitalWrite(LED4,LOW);
    digitalWrite(LED5,LOW);
    break;
  case 2:                // Upon recieeving integer 2
    digitalWrite(LED2,HIGH);
    digitalWrite(LED3,HIGH);
    digitalWrite(LED4,LOW);
    digitalWrite(LED5,LOW);
    break;
  case 3:                  // Upon recieeving integer 3
     digitalWrite(LED2,HIGH);
    digitalWrite(LED3,HIGH);
    digitalWrite(LED4,HIGH);
    digitalWrite(LED5,LOW);
    break;
  case 4:                  // Upon recieeving integer 4
    digitalWrite(LED2,HIGH);
    digitalWrite(LED3,HIGH);
    digitalWrite(LED4,HIGH);
    digitalWrite(LED5,HIGH);
    break;
  }
}

ros::Subscriber<std_msgs::UInt16> level("led_level", level_cb);

void setup() {
  // put your setup code here, to run once:
  pinMode(13,OUTPUT);
  pinMode(LED2,OUTPUT);
  pinMode(LED3,OUTPUT);
  pinMode(LED4,OUTPUT);
  pinMode(LED5,OUTPUT);
  digitalWrite(13, HIGH);
  nh.initNode();
  nh.subscribe(level);
}

void loop() {
  // put your main code here, to run repeatedly:
  nh.spinOnce();
  delay(10);
}
