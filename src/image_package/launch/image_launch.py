from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Publish a packaged image (acts like a camera)
        

        # Run the color detector node
        Node(
            package='image_package',
            executable='color_detect',
            name='color_detect'
            
        ),

        # Launch image_view and remap its 'image' subscription to the
        # color detector's publishing topic so you can visualize results.
        Node(
            package='image_view',
            executable='image_view',
            name='image_view',
            output='screen'
            #remappings=[('image', '/camera/color_detected')],
        ),
    ])