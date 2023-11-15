# RF-Homing-Website
To get the website running in the first place, 
1. -First, make sure you've ran the commands (don't include the (1) or (2) for either commands typed):
(1) source /opt/ros/humble/setup.bash
(2) source install/setup.bash
You need to run the command (don't include the (1)):
(1) ros2 launch rosbridge_server rosbridge_websocket_launch.xml 
in the linux terminal of this computer in the payload_colcon_ws directory

2. open another terminal in the linux command prompt and run the command (don't include the (1)):
(1) python3 ros-hello-world-listener.py 
in the same directory as the previous terminal opened which hosts the actual website
-You can copy and paste the address of 127.0.0.1:8080 (or the other address listed which is the ip address of the computer running the program) in the search bar on google to run on this computer. 

3. To run on another computer at the same time: 
-You need to replace 127.0.0.1 with the ip address of the computer that's running the ros-hello-world-listener.py file which for this computer is 10.1.7.196 (It could vary)
-To run on another computer, copy and paste 10.1.7.196:8080 into the address bar, or replace the ip address with whatever the ip address is of the computer that's hosting the website 
-You can determine the ip address of this computer in the linux terminal with the command ifconfig

4. You are now ready to access the home screen which currently has four options to choose from:
-Send commands to view payload status
-Display remap messages
-Configure yaml file
-Download output files

5. Send commands to view payload status screen:
(First, make sure you run the commands, 
(1) source /opt/ros/humble/setup.bash
(2) source install/setup.bash)
When you navigate to this screen if you want to see any sort of output, you have to open a separate linux terminal and run the command (don't include the (1)):
(1) ros2 launch rfhoming2 test_launch.py 
in the payload_colcon_ws directory
-Once you do that, the website will refresh every second to update with the output from the simulated payload status data that displays the timestamps along with the status of the drone such as 'BOOTUP' or 'FLYING' for example. 
-If you want to change the status to update to flying for instance, you choose an option from the drop down menu. If you do that, it will update the status to 'FLYING' in the payload status section
-It will also display in the commands sent section the exact time stamp when that command was sent to the website. 
-This works for all numerical commands that are listed in the previous README.md located in the Outputs folder.

6. Display remap messages screen:
There's no user input involved in this screen, to get output displayed you need to navigate to the Utils directory in its own linux terminal and run the command:
(1) python3 ReMAP_Dummy_Message_Sender.py
-Once you do that, after the page refreshes again the output/simulated values will be displayed
(Note: For both the send commands and remap message screen, if you want to stop the simulation from running, hit control C or control Z a few times until it's stopped completely)

7. Configure yaml file screen:
-This screen allows you to edit the configure.yaml file and its values associated with each key individually. All changes made on the website are also updated in the file itself. 
-The way that it works is that when you open this screen, there are text boxes for the values associated with the keys prepopulated with the current values found in the configure.yaml file.
-If you want to change them, you simply click the text box, and replace the text with whatever you type in.
-To change the value on the website itself and the file itself, you hit the configure yaml button which updates the value on the website, and the yaml file itself. -This is another html page with a refresh feature every 5 seconds to update the display based on the user input after they hit the submit button
-To adjust the time it takes for the page to refresh, change content = "5" found at the top of each html file to whatever amount of seconds you want to wait before the page refreshes again.

8. Download output files:
-If you want to properly download the Output files from the simulation which include the LOG_00000.txt, MONO_00000.csv, MONO_00000_RAW.csv, SYS_00000.csv, POSE_00000.csv, and STAT_00000.csv files, you have to ensure that you stop the simulation from the test launch.py file by hitting control c or control z a few times as was mentioned earlier in the README because that is when the output files are created.
-You also have to ensure that you do not navigate to this screen before or during the simulation being started, because the route to this page in the ros-hello-world-listener.py file calls a function that creates the output files from the simulation. This logically makes sense because you wouldn't download output files if you have no data anyways. 
-Once you click the download output files button, a zip file pops up at the bottom of your screen which is located in the downloads folder of any laptop that accesses this web page, and it contains the txt and csv files mentioned earlier.

List of commands if you want to empty space after testing the simulation data:
- sudo apt-get autoremove
- sudo apt-get autoclean
- sudo apt-get clean
- sudo journalctl --vacuum-time=3d
- sudo bash hello.sh
- rm -rf ~/.cache/thumbnails/*
- kill -9 $(ps -A | grep python | awk '{print $1}')
- You should also delete each txt and csv file found within the Desktop/rfhoming/payload_colcon_ws/src/rfhoming2/rfhoming2/Outputs folder before testing the web application again
(Note: a zip file is generated within the payload_colcon_ws file once you navigate to the download output screen from the home page, if you want to test the web application again, make sure to delete the newly created Zipped_file.zip located in the payload_colcon_ws directory)
