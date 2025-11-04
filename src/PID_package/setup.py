from setuptools import find_packages, setup

package_name = 'PID_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml', 'launch/controller_launch.py']),
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
        'console_scripts': ['PID_control = PID_package.PID_control:main'
        ],
    },
)
