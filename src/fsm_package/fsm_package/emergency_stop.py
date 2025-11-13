from std_srvs.srv import SetBool
import rclpy
from rclpy.node import Node
import math


class EmergencyStop(Node):
    def __init__(self):
        # use a clear node name for this service
        super().__init__('emergency_stop')
        self.service = self.create_service(SetBool, 'emergency_stop', self.listener_callback)

    def listener_callback(self, request, response):
        if request.data:
            self.get_logger().info('Emergency stop activated! Stopping turtle.')
            response.message = 'Turtle stopped due to emergency stop.'
            response.success = True
        else:
            self.get_logger().info('Emergency stop deactivated.')
            response.message = 'Turtle can resume movement.'
            response.success = False

        # Always return success=True to indicate the service handled the
        # request. The client (mode_switcher) uses the request value to
        # determine whether to enter/leave emergency stop mode.
        
        return response
        


def main(args=None):
    rclpy.init(args=args)

    ObStop = EmergencyStop()

    rclpy.spin(ObStop)

    ObStop.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

   