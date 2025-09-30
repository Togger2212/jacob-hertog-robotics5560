import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist



class TurtleSwim(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.last_state = 0
        self.total_state = 0
        self.state = 'forward'
        self.vel = Twist()

    def timer_callback(self):
        if self.total_state >= 2400:
            self.stop()
        if self.state =='forward':
            if(self.last_state > 500):
                self.state = 'turn'
                self.last_state = 0
            else:
                self.move_forward()
                

        else:
            if(self.last_state > 100):
                self.state = 'forward'
                self.last_state = 0
            else:
                self.rotate()

        self.last_state+=1
        self.total_state +=1
        self.publisher_.publish(self.vel)

        

    def move_forward(self):
        self.vel.angular.z = 0.0
        self.vel.linear.x = 1.0
        
        



    def rotate(self):
        self.vel.linear.x = 0.0
        self.vel.angular.z = 3.14159/2.0

    def stop(self):
        self.vel = Twist()
        rclpy.shutdown()
        
    


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = TurtleSwim()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()