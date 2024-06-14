#!/bin/bash

# Function to check if roscore is running
check() {
    rostopic list > /dev/null 2>&1
    return $?
}

# Clean log
yes | rosclean purge

# ------------ First tmux session ------------
# tmux new-session -d -s teleop_session bash -c "
#     export ROS_MASTER_URI=http://$(hostname -I | awk '{print $1}'):11311;
#     export ROS_IP=$(hostname -I | awk '{print $1}');
#     cd ~/datn_navbot_pi;
#     source devel/setup.bash;
#     rosrun navstack_pub custom_teleop_twist_keyboard.py;
#     exec bash
# "
# Wait for teleop to start
# echo "Waiting for teleop to fully start..."
# until check; do
#     sleep 1
# done
# echo "teleop is active."

# ------------ Second tmux session ------------
# tmux new-session -d -s load_map_session bash -c "
#     cd ~/datn_navbot_pi/;
#     source devel/setup.bash;
#     roslaunch navstack_pub load_map.launch map_name:=$1;
#     exec bash
# "
# Wait for load map
#echo "Waiting for loading map..."
#until check; do
    #sleep 1
#done
#echo "map loaded."
               
# ------------ Third tmux session ------------
tmux new-session -d -s navbot_session bash -c "
    cd ~/datn_navbot_pi/;
    source devel/setup.bash;
    roslaunch navstack_pub navbot.launch map_name:=$1;
    exec bash
"               



