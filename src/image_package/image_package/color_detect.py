import rclpy 
from rclpy.node import Node
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class ColorDetect(Node):
    def __init__(self):
        super().__init__('color_detect')
        self.declare_parameter('color', 'blue')
        self.color = self.get_parameter('color').get_parameter_value().string_value
        self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(Image, 'color_detected', 10)
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        self.color = self.get_parameter('color').get_parameter_value().string_value
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        if self.color == 'red':
        # Define range for red color detection
            lower = (0, 100, 100)
            upper = (10, 255, 255)

        #Define range for blue color detection
        elif self.color == 'blue':
            lower = (100, 150, 100)
            upper = (140, 255, 255)    

        #Define range for pink color detection
        elif self.color == 'pink':
            lower = (140, 70, 100)
            upper = (170, 255, 255)

        elif self.color == 'green':
            lower = (40, 70, 70)
            upper = (80, 255, 255)

        elif self.color == 'yellow':
            lower = (20, 100, 100)
            upper = (40, 255, 255)

        # Create masks for red color
        mask1 = cv2.inRange(hsv_image, lower, upper)
    

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        # 2) morphological open (remove small objects)
        mask_open = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel, iterations=4)

        # 3) morphological close (fill small holes)
        mask_clean = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel, iterations=4)


        # Apply mask to original image
        detected_image = cv2.bitwise_and(cv_image, cv_image, mask=mask_clean)

        # Convert back to ROS Image message and publish
        red_detected_msg = self.bridge.cv2_to_imgmsg(detected_image, encoding='bgr8')
        self.publisher_.publish(red_detected_msg)

def main(args=None):
    rclpy.init(args=args)
    color_detect = ColorDetect()
    rclpy.spin(color_detect)
    color_detect.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()