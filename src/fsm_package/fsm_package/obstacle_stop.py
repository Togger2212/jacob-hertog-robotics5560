from std_srvs.srv import SetBool
import rclpy
from rclpy.node import Node
import math
from std_msgs.msg import Bool
from turtlesim.msg import Pose


class ObstacleStop(Node):
    
    def __init__(self):
        super().__init__('obstacle_stop')
        self.subscription = self.create_subscription(Pose, '/turtlesim1/turtle1/pose', self.listener_callback, 10)
        self.publisher_ = self.create_publisher(Bool, 'obstacle_stop', 10)
        self.obstacle_detected = False
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg: Pose):
        x_pos = msg.x  
        y_pos = msg.y
        # Group the bounds check to avoid operator-precedence bugs
        out_of_bounds = (
            x_pos < 1.0 or x_pos > 10.0 or
            y_pos < 1.0 or y_pos > 10.0
        )
        if out_of_bounds and not self.obstacle_detected:
            self.get_logger().info('Obstacle detected! Stopping turtle. Control takeover required.')
            self.obstacle_detected = True
            self.stop_turtle()
        elif out_of_bounds and self.obstacle_detected:
            # already in stop state; nothing to do
            return
        else:
            self.obstacle_detected = False
            self.stop_turtle()


    def stop_turtle(self):
        msg = Bool()
        msg.data = self.obstacle_detected
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    ObStop = ObstacleStop()

    rclpy.spin(ObStop)

    ObStop.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

   
