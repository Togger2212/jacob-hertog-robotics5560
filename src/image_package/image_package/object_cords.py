import rclpy 
from rclpy.node import Node
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped
from rcl_interfaces.msg import ParameterDescriptor, ParameterType

class ObjectDetect(Node):
    def __init__(self):
        super().__init__('object_cords')
        
        # Declare parameters with descriptions for better usability
        param_descriptor = ParameterDescriptor(
            type=ParameterType.PARAMETER_INTEGER,
            description='Minimum contour area to consider as an object (pixels^2).'
        )
        self.declare_parameter('min_area', 200, param_descriptor)
        
        self.subscription = self.create_subscription(
            Image,
            'color_detected',
            self.listener_callback,
            10)
        self.publication = self.create_publisher(PointStamped, 'object_position', 10)
        self.bridge = CvBridge()
       

    def listener_callback(self, msg):
        # Retrieve the parameter value dynamically within the callback if desired, 
        # or once in init and just read self.min_area
        min_area = self.get_parameter('min_area').get_parameter_value().integer_value

        try:
            # Convert ROS Image -> numpy array. 
            
            cv_image = self.bridge.imgmsg_to_cv2(msg)
        except Exception as e:
            self.get_logger().error(f"CvBridge Error: {e}")
            return

        # Determine if the input is a BGR image or a single-channel mask
        if len(cv_image.shape) == 3:
            # Assume BGR input, convert to grayscale then binary mask
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        elif len(cv_image.shape) == 2:
            # Already a single-channel image/mask
            mask = cv_image
        else:
            self.get_logger().warn("Input image has unexpected number of channels/shape.")
            return

        # Find contours 
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            self.get_logger().debug('No contours found.')
            return

        # Filter contours by minimum area
        filtered_contours = [c for c in contours if cv2.contourArea(c) >= min_area]

        if not filtered_contours:
            self.get_logger().debug('No contours found above min_area threshold.')
            return

        # Choose the largest remaining contour
        c = max(filtered_contours, key=cv2.contourArea)
        area = cv2.contourArea(c)

        M = cv2.moments(c)
        if M["m00"] == 0:
            # Log this as debug since it's likely a filtered/degenerate contour case
            self.get_logger().debug('Contour has zero valid moment (degenerate).')
            return

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # Bounding box calculation (optional, keeping your original code)
        x, y, w, h = cv2.boundingRect(c)
        
        self.get_logger().info(f'Object centroid (px): ({cX}, {cY}), bbox: x={x},y={y},w={w},h={h}, area={area:.1f}')

        # Publish as PointStamped (pixel coords, header from input msg)
        ps = PointStamped()
        ps.header = msg.header  # Use the header from the input Image message
        ps.point.x = float(cX)
        ps.point.y = float(cY)
        ps.point.z = float(area)  # Area is often useful here

        self.publication.publish(ps)

# The main function remains unchanged and is correct
def main(args=None):
    rclpy.init(args=args)
    object_detect = ObjectDetect()
    rclpy.spin(object_detect)
    object_detect.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
