import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class Conversion(Node):
    def __init__(self):
        super().__init__('conversion')
        # parameter: units (meters, feet, smoots)
        self.declare_parameter('units', 'meters')
        self.units = self.get_parameter('units').get_parameter_value().string_value
        

        # publishers/subscribers
        self.publisher_ = self.create_publisher(Float32, 'distance_converted', 10)
        self.subscription = self.create_subscription(
            Float32,
            'distance',
            self.distance_callback,
            10
        )
        self.subscription  # prevent unused variable warning

        self.get_logger().info(f'Conversion node started with units={self.units}')

    def distance_callback(self, msg: Float32):
        raw = msg.data
        # refresh units from parameter server in case it changed at runtime
        self.units = self.get_parameter('units').get_parameter_value().string_value
        converted = self.convert(raw)
        out = Float32()
        out.data = converted
        self.publisher_.publish(out)
        self.get_logger().info(f'{raw} meters -> {converted} ({self.units})')

    def convert(self, value_meters: float) -> float:
        # assume incoming distance is meters
        if self.units == 'meters':
            return value_meters
        if self.units == 'feet':
            return value_meters * 3.28084
        if self.units == 'smoots':
            # 1 smoot = 1.7018 meters (approx)
            return value_meters / 1.7018
        # default: no conversion, return to meters
        else:
            self.set_parameters([rclpy.parameter.Parameter('units', rclpy.Parameter.Type.STRING, 'meters')])
            return value_meters


def main(args=None):
    rclpy.init(args=args)
    node = Conversion()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()