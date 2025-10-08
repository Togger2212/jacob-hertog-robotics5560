from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='first_package',
            namespace='turtlesim1',
            executable='move_turtle',
            name='move_turtle'
        ),
        Node(
            package='first_package',
            namespace='turtlesim1',
            executable='distance_turtle',
            name='distance_turtle'
        ),
        Node(
            package='turtlesim',
            namespace='turtlesim1',
            executable='turtlesim_node',
            name='turtlesim_node'
        ),
        Node(
            package='turtlesim',
            namespace='turtlesim1',
            executable='turtle_teleop_key',
            name='teleop_twist_key')
    ])