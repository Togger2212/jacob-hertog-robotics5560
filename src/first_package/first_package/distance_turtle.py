import rclpy
from rclpy.node import Node
import math
from std_msgs.msg import Float32
from turtlesim.msg import Pose



class TurtleDistance(Node):

    def __init__(self):
        super().__init__('minimal_pubsub')
        self.pose = Pose()
        self.start_set = False
        self.totald = 0.0
        self.publisher_ = self.create_publisher(Float32, 'distance', 10)
        self.subscription = self.create_subscription(Pose, 'turtle1/pose', self.timer_callback, 10)
        self.subscription  # prevent unused variable warning
    

        

    def timer_callback(self, msg):
        if not self.start_set:
            self.pose.x = msg.x
            self.pose.y = msg.y
            self.start_set = True
            return
        inputx = msg.x
        inputy = msg.y
        self.totald += math.sqrt((inputx - self.pose.x)**2 + (inputy - self.pose.y)**2)
        self.pose.x = inputx
        self.pose.y = inputy
        self.publisher_.publish(Float32(data=self.totald))
        
        
        


def main(args=None):
    rclpy.init(args=args)

    turtle_distance = TurtleDistance()

    rclpy.spin(turtle_distance)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    turtle_distance.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()