import yaml
# import io

YAML_FILENAME = "params.yaml"
ROOM_NUMBER = 0
LAUNCH_FILNAME = "room_"+str(ROOM_NUMBER)+".launch"
LAUNCH_FILE_STRING = """
<?xml version="1.0"?>
<launch>

	<arg name="rviz"                   	default="false" />
	<arg name="rviz_cfg"          		default="$(find aruco_tf)/launch/aruco.rviz" />
	<arg name="use_urdf" 			default="false"/>

	<!-- For TFs use one time URDF or continuos TFs topics -->
	<group if="$(arg use_urdf)">
	 <param name="robot_description"  textfile="$(find structure_core)/launch/Structure.urdf" />
	<node name="robot_state_publisher" pkg="robot_state_publisher"
	    type="robot_state_publisher" />   
	</group>

	<group unless="$(arg use_urdf)">
	    <!--                                                       name            x      y    z q q q                        -->
		<node pkg ="tf" type="static_transform_publisher" name="aruco_102" args="-{0}  -{1}  {2} 0 0 0 room_link aruco_102 50" />
		<node pkg ="tf" type="static_transform_publisher" name="aruco_103" args="-{3}  -{4}  {5} 0 0 0 room_link aruco_103 50" />
		<node pkg ="tf" type="static_transform_publisher" name="aruco_104" args="-{6}  -{7}  {8} 0 0 0 room_link aruco_104 50" />
		<!-- node pkg ="tf" type="static_transform_publisher" name="cam_weighted" args="0 0 0 0 0 0 0 room_link cam_weighted 50" /> -->
		<!--                                                        name                 x                     y                   z                   qx                  qy                  qz                  qw                                  -->
	</group> 


	<!-- Visualization RVIZ -->
	<node if="$(arg rviz)" pkg="rviz" type="rviz" name="rviz" args="-d $(arg rviz_cfg)"/>

	</launch>"""

#{9}  {10}  {11} {12} {13} {14} {15}

def main():
    launch_file = open(LAUNCH_FILNAME,"w")
    # Read YAML file
    with open(YAML_FILENAME, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    launch_file_string_formated = LAUNCH_FILE_STRING.format(
        data_loaded["locations"]["qr102"]["x"],
        data_loaded["locations"]["qr102"]["y"],
        data_loaded["locations"]["qr102"]["z"],
        data_loaded["locations"]["qr103"]["x"],
        data_loaded["locations"]["qr103"]["y"],
        data_loaded["locations"]["qr103"]["z"],
        data_loaded["locations"]["qr104"]["x"],
        data_loaded["locations"]["qr104"]["y"],
        data_loaded["locations"]["qr104"]["z"]
    )
    launch_file.write(launch_file_string_formated)
    launch_file.close()
    



if __name__ == "__main__":
    main()