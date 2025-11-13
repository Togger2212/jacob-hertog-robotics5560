from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='fsm_package',
            executable='auto_move',
            name='auto_move'
        ),
       
        Node(
            package='turtlesim',
            namespace='turtlesim1',
            executable='turtlesim_node',
            name='turtlesim_node'
        ),
        
        Node(
            package='fsm_package',
            executable='emergency_stop',
            name='emergency_stop'
        ) ,
        
         Node(
            package='fsm_package',
            executable='obstacle_stop',
            name='obstacle_stop'
        )
       
       
                 
        
        
    ])