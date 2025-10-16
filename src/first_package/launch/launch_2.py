from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.actions import ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('first_package'),
                    'turtle_launch.py'
                ])
            ])
        ),
        Node(
            package='first_package',
            namespace='turtlesim1',
            executable='distance_turtle',
            name='distance_turtle'
        ),
        ExecuteProcess(
            cmd=[
                'ros2',
                'topic',
                'echo',
                'distance',
                'std_msgs/Float32'
            ],
            shell=True,
            output='screen'
        )
    ])