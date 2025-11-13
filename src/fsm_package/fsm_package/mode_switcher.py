import rclpy
from rclpy.node import Node
import math
from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool
from std_msgs.msg import Bool
import sys, select, tty, termios # For handling keyboard input without curses



class ModeSwitch(Node):

    def __init__(self):
        super().__init__('mode_switch')
    # publish to the turtlesim namespace so the command reaches the turtlesim node
    # turtlesim is launched in the 'turtlesim1' namespace in your launch file,
    # so publish to the absolute topic under that namespace.
        self.publisher_ = self.create_publisher(Twist, '/turtlesim1/turtle1/cmd_vel', 10)
        self.subscription1 = self.create_subscription(Twist, 'turtle1/cmd_vel_tele', self.tele_handle, 10)
        self.subscription2 = self.create_subscription(Twist, 'turtle1/cmd_vel_auto', self.auto_handle, 10)
        self.subscription3 = self.create_subscription(Bool, 'obstacle_stop', self.stop_handle, 10)
        self.mode = 'teleop'  # default mode
        self.message = Twist()
        self.flip = False
        self.timer = self.create_timer(0.05, self.callback)
        self.get_logger().info('Press "o" for Auto Mode, "e" for Teleop Mode, "p" for Emergency Stop')
        self.cli = self.create_client(SetBool, 'emergency_stop')
        # Save terminal settings only when stdin is a TTY. When launched
        # via ros2 launch there is no controlling TTY and termios.tcgetattr
        # would raise an exception.
        if sys.stdin.isatty():
            try:
                self.settings = termios.tcgetattr(sys.stdin)
            except Exception:
                self.settings = None
        else:
            self.settings = None

        # one-shot revert timer for leaving stop mode (optional)
        self._revert_timer = None

    def stop_handle(self, msg):
        if msg.data:
            # Enter stop mode and publish zero velocities immediately
            self.mode = 'stop'
            self.message = Twist()
            self.publisher_.publish(self.message)

    
    def tele_handle(self, msg):
        if self.mode == 'teleop':
            self.message = msg
            

    def auto_handle(self, msg):
        if self.mode == 'auto':
            self.message = msg
            
        

    def get_key(self):
        # If not a TTY (launched by ros2 launch) just do a short select and return ''
        if not sys.stdin.isatty() or self.settings is None:
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                try:
                    return sys.stdin.read(1)
                except Exception:
                    return ''
            return ''

        try:
            tty.setraw(sys.stdin.fileno())
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                key = sys.stdin.read(1)
            else:
                key = ''
        finally:
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
            except Exception:
                pass
        return key




    def callback(self):
        # Determine mode based on which topic the message came from
        

        key = self.get_key()
        if self.mode != 'em_stop':
            if key == 'e':
                self.mode = 'teleop'
                self.get_logger().info('Teleop Mode toggled')
            elif key == 'o':
                self.mode = 'auto'
                self.get_logger().info('Auto Mode toggled')
            elif key == 'p':
                self.send_emergency_stop()
            elif key == 'q':
                self.get_logger().info('Exiting program.')
                rclpy.shutdown()
                return
                
            
        else:
            if key == 'p':
                self.send_emergency_stop()
        

        # publish the current motion command
        self.publisher_.publish(self.message)
        # service callbacks while we loop reading keys
    
            
    def send_emergency_stop(self):
        """Initiates the service call without blocking the node."""
        if not self.cli.wait_for_service(timeout_sec=0.1):
            self.get_logger().warn('Emergency Stop service not available.')
            return

        req = SetBool.Request()
        req.data = not self.flip
        
        # --- KEY CHANGE: Call asynchronously and add a DONE CALLBACK ---
        future = self.cli.call_async(req)
        future.add_done_callback(self.em_stop_response_callback)
        # The function immediately returns here, allowing the node to continue spinning/reading keys

    def em_stop_response_callback(self, future):
        """Processes the result of the service call once it is complete."""
        try:
            result = future.result()
            if result is not None and result.success:
                # Update mode and flip state upon successful service handling
                    self.get_logger().info('Emergency stop latched ON. To Unlatch press "p" again.')
                    self.message =Twist()
                    self.mode = 'em_stop' 
               
                # Only update the local flip variable if the service successfully responded
                    self.flip = not self.flip 
            else:
                self.mode = 'teleop'
                self.get_logger().info('Emergency stop latched OFF. Mode set to Teleop')
                self.flip = not self.flip 
                
        except Exception as e:
            self.get_logger().error(f'Service call failed entirely: {e}')
       
        
        
        


def main(args=None):
    rclpy.init(args=args)

    mode_switch = ModeSwitch()
    
    rclpy.spin(mode_switch)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    mode_switch.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()