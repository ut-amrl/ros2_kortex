# Copyright (c) 2023 PickNik, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_move_group_launch


def launch_setup(context, *args, **kwargs):
    use_sensors_3d = LaunchConfiguration("use_sensors_3d")
    moveit_config_builder = (
        MoveItConfigsBuilder(
            "gen3", package_name="kinova_gen3_7dof_robotiq_2f_85_moveit_config"
        )
    )
    sensors_enabled = use_sensors_3d.perform(context) == "true"
    if sensors_enabled:
        moveit_config_builder = moveit_config_builder.sensors_3d(
            file_path="config/sensors_3d_enabled.yaml"
        )
    moveit_config = moveit_config_builder.to_moveit_configs()

    return generate_move_group_launch(moveit_config)


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument(
            "use_sensors_3d",
            default_value="true",
            description="Enable MoveIt 3D sensors input (point cloud -> octomap).",
        )
    ]
    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])
