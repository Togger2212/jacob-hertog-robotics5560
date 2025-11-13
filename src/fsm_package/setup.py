from setuptools import find_packages, setup

package_name = 'fsm_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml','launch/fsm_launch.py']),
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
        'console_scripts': [ 'mode_switcher = fsm_package.mode_switcher:main',
                             'auto_move = fsm_package.auto_move:main',
                             'emergency_stop = fsm_package.emergency_stop:main',
                             'obstacle_stop = fsm_package.obstacle_stop:main',
                             'turtle_controller = fsm_package.turtle_controller:main'
        ],
    },
)
