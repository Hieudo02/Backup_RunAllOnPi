#!/usr/bin/env python3

import rospy
<<<<<<< HEAD
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped

def move_to_goal(x, y, z, w, point_number):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.z = z
    goal.target_pose.pose.orientation.w = w

    client.send_goal(goal)
    rospy.loginfo("Send point {} successfully".format(point_number))
    client.wait_for_result()
    rospy.loginfo("Done point {}".format(point_number))

if __name__ == '__main__':
    rospy.init_node('auto_nav')
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    # waypoints = [(0, 2, 0, 1), (3, 4, 0, 1), (5, 6, 0, 1)]  # Danh sách các điểm (x, y, z, w)
    waypoints = [(0.5, 0.5, 0, 1)]  # Danh sách các điểm (x, y, z, w)

    for idx, point in enumerate(waypoints, start=1):
        move_to_goal(point[0], point[1], point[2], point[3], idx)
    
    rospy.loginfo("All points reached")
    rospy.spin()
=======
from geometry_msgs.msg import PoseStamped

def main():
    rospy.init_node('goal_publisher')
    goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)

    goal = PoseStamped()
    goal.header.frame_id = "map"  
    goal.header.stamp = rospy.Time.now()
    goal.header.seq = 1
    goal.pose.position.x = 1 
    goal.pose.position.y = 2  
    goal.pose.position.z = 0.0  
    goal.pose.orientation.x = 0.0
    goal.pose.orientation.y = 0.0
    goal.pose.orientation.z = 0.0
    goal.pose.orientation.w = 1.0  # w = 1 represents no rotation

    goal_pub.publish(goal)

    rospy.loginfo("Published goal: x = %f, y = %f", goal.pose.position.x, goal.pose.position.y)

    rospy.sleep(1)
    rospy.spin()

if __name__ == '__main__':
    main()

'''
#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped

goals = []

def main():
    rospy.init_node('goal_publisher')
    goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
    rospy.sleep(1)
    for i in range(5):
        goal = PoseStamped()
        goal.header.frame_id = "map"  
        goal.pose.position.x = i 
        goal.pose.position.y = i * 2  
        goal.pose.position.z = 0.0  
        goal.pose.orientation.x = 0.0
        goal.pose.orientation.y = 0.0
        goal.pose.orientation.z = 0.0
        goal.pose.orientation.w = 1.0  # w = 1 represents no rotation
        goals.append(goal)

    seq_num = 0
    for i in range(len(goals)):
        if rospy.is_shutdown():
            break

        goals[i].header.stamp = rospy.Time.now()
        goals[i].header.seq = seq_num
        seq_num += 1
        goal_pub.publish(goals[i])

        rospy.loginfo("Published goal %d: x = %f, y = %f", i, goals[i].pose.position.x, goals[i].pose.position.y)

        rospy.sleep(1)

if __name__ == '__main__':
    main()

'''
>>>>>>> Upload all file run on pi
