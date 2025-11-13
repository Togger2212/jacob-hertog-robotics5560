import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, select, tty, termios # For handling keyboard input without curses

class TurtleTeleop(Node):
    def __init__(self):
        super().__init__('turtle_teleop_py')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel_tele', 10)
        self.get_logger().info('Reading from keyboard')
        self.get_logger().info('---------------------------')
        self.get_logger().info('Use WASD keys to move the turtle.')
    # periodic timer to read keyboard and publish current command
        self.timer = self.create_timer(0.05, self.run_teleop)
        self.twist = Twist()
        # cancellable one-shot timer used to reset velocities after a short duration
        self._stop_timer = None
        # duration (seconds) a keypress keeps the velocity before auto-zero
        self._keypress_duration = 0.5
            # Save terminal settings only when stdin is a TTY (interactive run).
            # When launched via ros2 launch there is no controlling TTY and
            # termios.tcgetattr will raise "Inappropriate ioctl for device".
        if sys.stdin.isatty():
            try:
                self.settings = termios.tcgetattr(sys.stdin)
            except Exception:
                self.settings = None
        else:
            self.settings = None

    def get_key(self):
        # If we don't have terminal settings (non-interactive), return empty
        if not sys.stdin.isatty() or self.settings is None:
            # still perform a short select so callers can loop without blocking
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                try:
                    return sys.stdin.read(1)
                except Exception:
                    return ''
            return ''

        # interactive TTY: use raw mode to read single keypress
        try:
            tty.setraw(sys.stdin.fileno())
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                key = sys.stdin.read(1)
            else:
                key = ''
        finally:
            # Restore terminal settings if we saved them earlier
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
            except Exception:
                pass
        return key

    def run_teleop(self):
        
        key = self.get_key()
        # support arrow sequences and letters
        if key == 'w':
            self.twist.linear.x = 1.5; self.twist.angular.z = 0.0
            self._start_stop_timer()
        elif key == 's':
            self.twist.linear.x = -1.5; self.twist.angular.z = 0.0
            self._start_stop_timer()
        elif  key == 'd':
            self.twist.linear.x = 0.0; self.twist.angular.z = -1.5
            self._start_stop_timer()
        elif key == 'a':
            self.twist.linear.x = 0.0; self.twist.angular.z = 1.5
            self._start_stop_timer()
        elif key == 'q':
            # exit teleop
            self.get_logger().info('Exiting teleop.')
            rclpy.shutdown()
            return
        
        # publish current twist; if a stop timer exists it will zero later
        self.publisher_.publish(self.twist)

    def _start_stop_timer(self):
        """Start or restart a one-shot timer that will zero velocities after
        self._keypress_duration seconds. Cancels any existing timer so rapid
        key presses extend the motion window.
        """
        # cancel previous timer if present
        try:
            if self._stop_timer is not None:
                self._stop_timer.cancel()
        except Exception:
            pass

        # create a repeating timer but cancel it in the callback to behave
        # like a one-shot timer
        self._stop_timer = self.create_timer(self._keypress_duration, self._stop_twist)

    def _stop_twist(self):
        # zero velocities and publish immediately, then cancel the timer
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        try:
            self.publisher_.publish(self.twist)
        except Exception:
            pass
        try:
            if self._stop_timer is not None:
                self._stop_timer.cancel()
        except Exception:
            pass
        self._stop_timer = None
            
        

def main(args=None):
    rclpy.init(args=args)
    teleop_node = TurtleTeleop()
    rclpy.spin(teleop_node)
    teleop_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()