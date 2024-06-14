#!/usr/bin/env python3

from __future__ import print_function
import threading
import roslib
import rospy
from std_msgs.msg import String
import sys, select, termios, tty

msg = """
>> Moving around:
        w    
    a   s   d
>> q/e : increase/decrease max speeds by 10%                                                   

>( ͡° ͜ʖ ͡°)> Hieuneee
------------------------------------------------------------  
                   #*          *#                    
                  #-             =#                  
                 #:               ##                 
                ##                 #.                
                ##                ###                              
                 ###  ########:  ###                 
                  ####        .####                  
            ############## ##############            
         .##+      ######   #####=      ###          
        ##        ##  ##    ###  #        *#+        
        #         *#.  .#####   ##          #        
       #           ##:  #####  ##           ##       
       #             ## ##### ##             #       
                        #####                        
                       ######                                         
           ++      +####     ####       ++           
              #######           #######              
------------------------------------------------------------  
"""

moveBindings = {
    'a': (1.0, -1.0),  # Turn left
    'w': (1.0, 1.0),   # Move forward
    's': (-1.0, -1.0), # Move backward
    'd': (-1.0, 1.0),  # Turn right
}

speedBindings = {
    'q': 1.1,  # Increase speed by 10%
    'e': 0.9,  # Decrease speed by 10%
}

class PublishThread(threading.Thread):
    def __init__(self, rate):
        super(PublishThread, self).__init__()
        self.publisher = rospy.Publisher('manual_control', String, queue_size=1)
        self.v_l = 0.0
        self.v_r = 0.0
        self.condition = threading.Condition()
        self.done = False

        if rate != 0.0:
            self.timeout = 1.0 / rate
        else:
            self.timeout = None

        self.start()

    def wait_for_subscribers(self):
        i = 0
        while not rospy.is_shutdown() and self.publisher.get_num_connections() == 0:
            if i == 4:
                print("Waiting for subscriber to connect to {}".format(self.publisher.name))
            rospy.sleep(0.5)
            i += 1
            i = i % 5
        if rospy.is_shutdown():
            raise Exception("Got shutdown request before subscribers connected")

    def update(self, v_r, v_l, speed):
        self.condition.acquire()
        self.v_l = v_l * speed
        self.v_r = v_r * speed
        self.condition.notify()
        self.condition.release()

    def stop(self):
        self.done = True
        self.update(0, 0, 0)
        self.join()

    def run(self):
        while not self.done:
            self.condition.acquire()
            self.condition.wait(self.timeout)

            message = "{},{}".format(self.v_r, self.v_l)

            self.condition.release()

            self.publisher.publish(message)

        self.publisher.publish("0,0")


def getKey(key_timeout):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('custom_teleop_twist_keyboard')
    
    repeat = rospy.get_param("~repeat_rate", 0.0)
    key_timeout = rospy.get_param("~key_timeout", 0.0)
    if key_timeout == 0.0:
        key_timeout = None

    pub_thread = PublishThread(repeat)

    v_l = 0
    v_r = 0
    speed = 0.1
    status = 0

    try:
        pub_thread.wait_for_subscribers()
        pub_thread.update(v_r, v_l, speed)

        print(msg)
        print("Currently speed: {}".format(speed))

        while True:
            key = getKey(key_timeout)
            if key in moveBindings.keys():
                v_r, v_l = moveBindings[key]
                pub_thread.update(v_r, v_l, speed)
            elif key == ' ':
                # Stop the robot when space is pressed
                v_r, v_l = 0.0, 0.0
                pub_thread.update(v_r, v_l, speed)
            elif key in speedBindings.keys():
                speed *= speedBindings[key]
                print(msg)
                print("Currently speed: {}".format(speed))
            else:
                if key == '' and x == 0 and y == 0 and z == 0 and th == 0:
                    continue
                v_l = 0
                v_r = 0
                if key == '\x03':
                    break


    except Exception as e:
        print(e)

    finally:
        pub_thread.stop()

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)