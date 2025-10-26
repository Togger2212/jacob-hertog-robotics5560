import rclpy
from rclpy.node import Node
import math
from std_msgs.msg import Float32
from turtlesim.msg import Pose
from odometry_helper_msg.msg import DistWheel




class DistanceUpdate(Node):

    def __init__(self):
        super().__init__('minimal_pubsub')
        self.pose = Pose()
        self.publisher_ = self.create_publisher(Pose, 'pose', 10)
        self.subscription = self.create_subscription(DistWheel, 'dist_wheel', self.callback, 10)
        self.subscription  # prevent unused variable warning
    

        

    def callback(self, msg):
        left_distance = msg.dist_wheel_left
        right_distance = msg.dist_wheel_right
        delta_s = (right_distance + left_distance) / 2.0
        delta_theta = (right_distance - left_distance) / .1  # assuming wheel_base of .05 meters
        self.pose.theta += delta_theta
        delta_x = delta_s * math.cos(self.pose.theta + delta_theta / 2.0)
        delta_y = delta_s * math.sin(self.pose.theta + delta_theta / 2.0)
        self.pose.x += delta_x
        self.pose.y += delta_y
        self.publisher_.publish(self.pose)
        
        
        


def main(args=None):
    rclpy.init(args=args)

    distance_update = DistanceUpdate()

    rclpy.spin(distance_update)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    distance_update.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()