#!/bin/bash

export ROS_MASTER_URI=http://192.168.50.99:11311
export ROS_IP=$(hostname -I | awk '{print $1}')
cd ~/datn_navbot
source devel/setup.bash
rosrun rviz rviz -d $(rospack find navstack_pub)/navbot.rviz

