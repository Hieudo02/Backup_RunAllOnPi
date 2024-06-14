#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int16
<<<<<<< HEAD
=======
import time
>>>>>>> Upload all file run on pi

def publish_ticks():
    rospy.init_node('ticks_publisher', anonymous=True)
    pub_right_ticks = rospy.Publisher('right_ticks', Int16, queue_size=10)
    pub_left_ticks = rospy.Publisher('left_ticks', Int16, queue_size=10)
    rate = rospy.Rate(50)  # 50 Hz
    
<<<<<<< HEAD
    right_ticks = 0
    left_ticks = 0

    while not rospy.is_shutdown():
        right_ticks += 5
        left_ticks += 10
        # if right_ticks > 500: right_ticks = 0
        # if left_ticks > 500: left_ticks = 0

        # right_ticks = 100
        # left_ticks = 68

        pub_right_ticks.publish(right_ticks)
        pub_left_ticks.publish(left_ticks)
=======
    right_ticks = 10
    left_ticks = 10

    while not rospy.is_shutdown():
        if right_ticks > 10000: right_ticks = 0
        else: right_ticks += 50
        
        if left_ticks > 10000: left_ticks = 0
        else: left_ticks += 40

        pub_right_ticks.publish(right_ticks)
        pub_left_ticks.publish(left_ticks)
        time.sleep(0.05) # Add a delay of 0.05 second
>>>>>>> Upload all file run on pi

        rospy.loginfo("Published right ticks: %d, left ticks: %d", right_ticks, left_ticks)
        rate.sleep()

<<<<<<< HEAD
=======

>>>>>>> Upload all file run on pi
if __name__ == '__main__':
    try:
        publish_ticks()
    except rospy.ROSInterruptException:
        pass
