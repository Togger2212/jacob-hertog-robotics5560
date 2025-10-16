from setuptools import find_packages, setup

package_name = 'first_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, [
            'package.xml',
            'launch/turtle_launch.py',
            'launch/launch_2.py',
            'launch/launch_3.py',
        ]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='togger',
    maintainer_email='togger@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'move_turtle = first_package.move_turtle:main',
            'distance_turtle = first_package.distance_turtle:main',
            'conversion = first_package.conversion:main',
        ]
    },
)
