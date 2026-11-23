import os
from ament_index_python.packages import get_package_share_directory
from launch import  LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node 


def generate_launch_description():
    pkg_share = get_package_share_directory('navforge')
    urdf_path = os.path.join(pkg_share,'urdf','example_bot.urdf')
    world_path = os.path.join(pkg_share,'worlds','test_world.sdf')
    pkg_share_parent = os.path.dirname(pkg_share)


    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'),'launch','gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_path}'}.items(),
    )



    robot_state_publisher = Node(
        package = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        parameters = [{
            'robot_description' : Command(['xacro ',urdf_path]),
            'use_sim_time': True,
        }],
    )

    

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'example_bot',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.5',
        ],
        output='screen',
)


    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
    ])