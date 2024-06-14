#!/bin/bash

# Function to check if roscore is running
check() {
    rostopic list > /dev/null 2>&1
    return $?
}

# Clean log
yes | rosclean purge

# ------------ Open FIRST TERMINAL with tmux ------------
tmux new-session -d -s roscore_session bash -c "
    export ROS_MASTER_URI=http://$(hostname -I | awk '{print $1}'):11311;
    export ROS_IP=$(hostname -I | awk '{print $1}');
    roscore;
    exec bash
"

# ------------ Current TERMINAL ------------
export ROS_MASTER_URI=http://$(hostname -I | awk '{print $1}'):11311
export ROS_IP=$(hostname -I | awk '{print $1}')
cd ~/datn_navbot_pi
source devel/setup.bash
rosrun navstack_pub app.py
