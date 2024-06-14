#!/bin/bash
    
# Get current system time in seconds and nanoseconds
current_time=$(date +%s)
current_nano=$(date +%N)

echo "sendGoal file is running...Received x: $1, y: $2"

cd ~/datn_navbot_pi
source devel/setup.bash

# "-1" means send 1 time and stop (break), if not i'll wait util hit ctrl-c
rostopic pub -1 /move_base_simple/goal geometry_msgs/PoseStamped \
    "{
        header: {
            seq: 1,
            stamp: {
                secs: $current_time,
                nsecs: $current_nano
            },
            frame_id: 'map'
        },
        pose: {
            position: {
                x: $1,
                y: $2,
                z: 0.0
            },
            orientation: {
                x: 0.0,
                y: 0.0,
                z: 0.0,
                w: 1.0
            }
        }
    }"
