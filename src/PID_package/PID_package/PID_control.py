import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from std_srvs.srv import SetBool


class PIDControl(Node):

    def __init__(self):
        super().__init__('pid_control')
        self.publisher_ = self.create_publisher(Float32, 'control_input', 10)

        # Subscriptions — incoming messages are std_msgs/Float32
        self.subscription_vel = self.create_subscription(Float32, 'velocity', self.handle__velocity, 10)
        self.subscription_pos = self.create_subscription(Float32, 'position', self.handle__position, 10)
        self.subscription_desired = self.create_subscription(Float32, 'desired', self.handle__desired, 10)
        self.subscription_error = self.create_subscription(Float32, 'error', self.handle__error, 10)

        # Wait for controller_ready service and notify dynamics that controller is up
        self.cli = self.create_client(SetBool, 'controller_ready')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Graph: Waiting for dynamics to start')
        req = SetBool.Request()
        req.data = True
        self.cli.call_async(req)

        # store numeric values as plain floats; use Float32 only for published message
        self.vel = 0.0
        self.pos = 0.0
        self.des = 0.0
        self.err = 0.0
        self.err_total = 0.0
        self.prev_err = 0.0
        self.accel = 0.0

    def handle__velocity(self, msg: Float32):
        # msg is std_msgs/Float32
        self.vel = msg

    def handle__position(self, msg: Float32):
        self.pos = float(msg.data)

    def handle__desired(self, msg: Float32):
        self.des = float(msg.data)

    def handle__error(self, msg: Float32):
        # Trigger PID computation on error updates
        self.err = msg.data
        self.calc_accel(self.err)

    def calc_accel(self, now_err):
        # PID coefficients
        kp = 1.0
        ki = 0.001
        kd = 1.6

        # integral term
        self.err_total += now_err

        # derivative term (based on previous error)
        derivative = -self.vel.data  # negative velocity as derivative of position error

        # compute PID
        accel = kp * now_err + ki * self.err_total + kd * derivative

        # update previous error for next derivative calculation
        
        

        # publish as Float32 message
        out_msg = Float32()
        out_msg.data = accel
        self.publisher_.publish(out_msg)
        self.get_logger().info(f'current error: {now_err}, Previous Error: {self.prev_err}, Derivative: {derivative}')
        self.prev_err = now_err

def main(args=None):
    rclpy.init(args=args)
    node = PIDControl()

    rclpy.spin(node)
    


if __name__ == '__main__':
    main()