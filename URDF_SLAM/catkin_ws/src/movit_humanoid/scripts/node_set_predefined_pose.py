#! /usr/bin/env python3

#Include the necessary libraries 
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import actionlib
from math import pi

class MyRobot:

    # Default Constructor
    def __init__(self, Group_Name):

        #Initialize the moveit_commander and rospy node
        self._commander = moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('node_set_redefined_pose', anonymous=True)

        
        #Instantiate a RobotCommander object. This object is the outer-level interface to the robot
        self._robot = moveit_commander.RobotCommander()
        #Instantiate a PlanningSceneInterface object. This object is an interface to the world surrounding the robot.
        self._scene = moveit_commander.PlanningSceneInterface()
        
        #define the movegoup for the robotic 
        #Replace this value with your robots planning group name that you had set in Movit Setup Assistant
        self._planning_group = Group_Name
        #Instantiate a MoveGroupCommander Object. This Object is an interface to the one group of joints. this interface can be used to plan and execute the motions on the robotic arm
        self._group = moveit_commander.MoveGroupCommander(self._planning_group)
        
        #We create a DisplayTrajectory publisher which is used later to publish trajectories for RViz to visualize
        self._display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)

        #Create action client for the Execute Trajectory action server
        self._exectute_trajectory_client = actionlib.SimpleActionClient('execute_trajectory', moveit_msgs.msg.ExecuteTrajectoryAction)
        self._exectute_trajectory_client.wait_for_server()

        #Get the planning frame, end effector link and the robot group names
        self._planning_frame = self._group.get_planning_frame()
        self._eef_link = self._group.get_end_effector_link()
        self._group_names = self._robot.get_group_names()

        #print the info
        #here the '\033[95m' represents the standard colour "LightMagenta" in terminals. For details, refer: https://pkg.go.dev/github.com/whitedevops/colors
        #The '\033[0m' is added at the end of string to reset the terminal colours to default
        rospy.loginfo('\033[95m' + "Planning Group: {}".format(self._planning_frame) + '\033[0m')
        rospy.loginfo('\033[95m' + "End Effector Link: {}".format(self._eef_link) + '\033[0m')
        rospy.loginfo('\033[95m' + "Group Names: {}".format(self._group_names) + '\033[0m')
        rospy.loginfo('\033[95m' + " >>> MyRobot initialization is done." + '\033[0m')

    def set_pose(self, arg_pose_name):
        rospy.loginfo('\033[32m' + "Going to Pose: {}".format(arg_pose_name) + '\033[0m')
        # Set the predefined position as the named joint configuration as the goal to plan for the move group.
        self._group.set_named_target(arg_pose_name)
        
        # Plan to the desired joint-space goal using the default planner
        plan = self._group.plan() 
        
        # Check if the plan is valid
        if plan is not None and len(plan.joint_trajectory.points) > 0:
            # Execute the planned trajectory
            self._group.execute(plan, wait=True)
        else:
            rospy.logerr("Failed to plan trajectory for pose: {}".format(arg_pose_name))
        
        # Print the current pose
        rospy.loginfo('\033[32m' + "Now at Pose: {}".format(arg_pose_name) + '\033[0m')
    

    # Class Destructor
    def __del__(self):
        #When the actions are finished, shut down the moveit commander
        moveit_commander.roscpp_shutdown()
        rospy.loginfo('\033[95m' + "Object of class MyRobot Deleted." + '\033[0m')


def main():

    #Create a new arm object from the MyRobot class
    left_leg = MyRobot("left_leg")
    right_leg =  MyRobot("right_leg")
    left_arm =  MyRobot("left_arm")
    right_arm =  MyRobot("right_arm")
    
    rospy.sleep(2000)

    #Here, we will repeat the cycle of setting to various positions, simulating the pick and place action
    while not rospy.is_shutdown():
        #call the function to set the position to "zero_pose"
        left_leg.set_pose("left_leg_rest")
        right_leg.set_pose("right_leg_rest")
        left_arm.set_pose("left_arm_rest")
        right_arm.set_pose("right_arm_rest")
        #Wait for 2 seconds
        rospy.sleep(2)

        #Walk Forward step 1
        left_leg.set_pose("left_leg_rest")
        right_leg.set_pose("right_leg_up")
        left_arm.set_pose("left_arm_up")
        right_arm.set_pose("right_arm_rest")
        #Wait for 2 seconds
        rospy.sleep(2)

        #Walk Forward step 2
        left_leg.set_pose("left_leg_up")
        right_leg.set_pose("right_leg_rest")
        left_arm.set_pose("left_arm_rest")
        right_arm.set_pose("right_arm_up")
        #Wait for 2 seconds
        rospy.sleep(2)


if __name__ == '__main__':
    main()
