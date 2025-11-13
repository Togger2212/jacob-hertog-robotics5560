import rclpy
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import random


class TurtleSwim(Node):

    def __init__(self):
        super().__init__('auto_move')
        # publish intended auto commands; ModeSwitch listens on this topic
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel_auto', 10)

        # timer frequency (seconds)
        self.timer_period = 0.05
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        # state machine: 'forward' or 'turn'
        self.state = 'forward'
        self.state_counter = 0
        self.state_limit = self._random_duration()

        # current velocity message
        self.vel = Twist()


    def _random_duration(self):
        # duration in timer ticks (timer_period units)
        # choose between 0.5s and 3.0s
        secs = random.uniform(0.5, 3.0)
        return max(1, int(secs / self.timer_period))

    def _start_forward(self):
        # random forward speed
        lin = random.uniform(0.2, 1.0)
        self.vel.linear.x = lin
        self.vel.angular.z = 0.0
        self.state = 'forward'
        self.state_counter = 0
        self.state_limit = self._random_duration()
        

    def _start_turn(self):
        # random angular velocity (left or right)
        ang = random.uniform(-2.0, 2.0)
        # keep small forward component while turning occasionally
        fwd = random.choice([0.0, random.uniform(0.0, 0.3)])
        self.vel.linear.x = fwd
        self.vel.angular.z = ang
        self.state = 'turn'
        self.state_counter = 0
        self.state_limit = self._random_duration()
        

    def _stop(self):
        self.vel = Twist()
        self.publisher_.publish(self.vel)
        self.get_logger().info('auto_move stopped')

    def timer_callback(self):
        # If state duration expired, switch state
        if self.state_counter >= self.state_limit:
            if self.state == 'forward':
                self._start_turn()
            else:
                self._start_forward()

        # increment counter and publish
        self.state_counter += 1
        self.publisher_.publish(self.vel)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleSwim()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()