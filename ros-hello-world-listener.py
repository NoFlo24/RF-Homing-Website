from __future__ import print_function
from flask import Flask, render_template, request
from flask import send_file
import roslibpy
import time
import threading
import yaml
import os
import json
from remap_listener_PC import remap_listener_PC
from CommandSender import CommandSender
from zipfile import ZipFile

sender = CommandSender()
remap_listener = remap_listener_PC()
latest_remap_header = None
latest_remap_payload = None
latest_remap_time = None
#Establishes the connection to ROS2 on a server
client=roslibpy.Ros(host='localhost', port=9090)
client.run()

#listens to data published to a topic
payload_status=roslibpy.Topic(client, '/workflow', 'std_msgs/msg/String')
payload_text=''

commands_sent=roslibpy.Topic(client, '/ground_station_commands', 'std_msgs/msg/UInt8')
commands_text=''

remap_messages=''

yaml_text=None
def update_yaml():
global yaml_text
#For testing the functionality of changing the configure.yaml file: 
# -Use the path of /home/arlw/Desktop/rfhoming/payload_colcon_ws/configure.yaml
# -If you comfortable enough to modify the configure.yaml file from the website,
# modify the directory to /home/arlw/Desktop/rfhoming/payload_colcon_ws/src/rfhoming2/rfhoming2/Lib/configure.yaml
with open('/home/arlw/Desktop/rfhoming/payload_colcon_ws/configure.yaml') as f:
data = yaml.load(f, Loader=yaml.FullLoader)
yaml_text=data
yaml_text['sim_target_latlonalt']=','.join([str(item) for item in yaml_text['sim_target_latlonalt']])
yaml_text['altius_IDs']=','.join([str(id) for id in yaml_text['altius_IDs']])
return yaml_text
# This function allows user to change value associated with a key in the yaml file
def set_state(key,state):
#Reads the current yaml file
with open('/home/arlw/Desktop/rfhoming/payload_colcon_ws/configure.yaml') as f:
doc = yaml.load(f, Loader=yaml.FullLoader)
#Changes the value associated with a key based on the user input
doc[f'{key}'] = state
#Writes the chnages to the yaml file based on the user input
with open('/home/arlw/Desktop/rfhoming/payload_colcon_ws/configure.yaml', 'w') as f:
yaml.dump(doc, f, sort_keys=False)

def print_payload_status(message):
global payload_text
t=time.localtime()
current_time=time.strftime("%H:%M:%S", t)
print(f'{current_time}:{message["data"]}\n')
#Appends to string, and displays on the website with proper line breaks for each new timestamp
payload_text+=(f'{current_time}:{message["data"]}\n')

def print_commands_sent(message):
global commands_text
t=time.localtime()
current_time=time.strftime("%H:%M:%S", t)
print(f'{current_time}:{message["data"]}\n')
#Makes it so that the command sent being displayed is not the number but the actual status the user wants to change it to
if(message['data']==100):
message['data']='BOOTUP'
elif(message['data']==103):
message['data']='FLYING'
elif(message['data']==104):
message['data']='LANDING'
elif(message['data']==105):
message['data']='CLEANUP'
elif(message['data']==106):
message['data']='SHUTDOWN'
elif(message['data']==200):
message['data']='WIFI_OFF'
elif(message['data']==201):
message['data']='WIFI_ON'
elif(message['data']==202):
message['data']='AZEL_SIM'
elif(message['data']==203):
message['data']='AZEL_REAL'
elif(message['data']==204):
message['data']='SIM_ON'
elif(message['data']==205):
message['data']='SIM_OFF'
elif(message['data']==206):
message['data']='RAW_DUMP'
#Appends to string, and displays on the website with proper line breaks for each new command being sent
commands_text+=(f'{current_time}:{message["data"]}\n')

def remap_func():
#The remap messages are displayed over UDP in the same way the original application did
#It does not subscribe to a topic like the payload timestamps and commands being sent do
global latest_remap_header
global latest_remap_payload
global latest_remap_time
global remap_messages
while(True):
head, pay = remap_listener.listen()
if(not head is None):
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
lastr ="{:.2f}".format(pay['lat_lon_alt'][0])
lostr = "{:.2f}".format(pay['lat_lon_alt'][1])
altstr = "{:.2f}".format(pay['lat_lon_alt'][2])
rstr ="{:.2f}".format(pay['euler'][0])
pstr = "{:.2f}".format(pay['euler'][1])
ystr = "{:.2f}".format(pay['euler'][2])
#Appends to remap_messages string which displays on the webpage with proper line breaks for each new timestamp that is added
remap_messages+= f"{current_time}: {lastr}, {lostr}, {altstr}\n"
remap_messages+=f" {rstr}, {pstr}, {ystr}\n"

latest_remap_header = head
latest_remap_payload = pay
latest_remap_time = time.perf_counter()
payload_status.subscribe(print_payload_status)

#The remap messages displayed on the website communicate over UDP, and do not listen to a topic
remap_thread = threading.Thread(target=remap_func)
remap_thread.start()
commands_sent.subscribe(print_commands_sent)

app=Flask(__name__)
@app.route('/')
def home():
return render_template('home.html')

@app.route('/payload.html')
def payload():
return render_template('payload.html', acknow=commands_text, connection=payload_text)

@app.route('/payload.html',methods=['POST','GET'])
def sendcommand():
if request.method=='POST':
select = request.form.get('payload_status')
sender.send_int_command(int(select))
return render_template('payload.html', acknow=commands_text, connection=payload_text)

@app.route('/remap.html')
def remap():
return render_template('remap.html', remaptext=remap_messages)

@app.route('/configureyaml.html')
def configyaml():
#ensures that the yaml file is properly updated on the webpage
return render_template('configureyaml.html',yamltext=update_yaml())

@app.route('/configureyaml.html', methods=['POST','GET'])
def inputyaml():
#This updates the value found on the yaml file itself as well as the web page based on what the user inputs on the web page
if request.method=='POST':
for i,v in update_yaml().items():
if(f'{i}'=='altius_IDs' or f'{i}'=='sim_target_latlonalt'):
v=request.form.get(f'{i}',type=str)
v=v.split(',')
res = [eval(i) for i in v]
set_state(f'{i}',res)
elif(type(v)==str):
v=request.form.get(f'{i}', type=str)
set_state(f'{i}',v)
elif(type(v)==int):
v=request.form.get(f'{i}', type=int)
set_state(f'{i}',v)
elif(type(v)==float):
v=request.form.get(f'{i}', type=float)
set_state(f'{i}',v)
return render_template('configureyaml.html',yamltext=update_yaml())

#Only navigate to the Download Outputs screen if you already have your outputs and have stopped the test_launch.py file 
#because otherwise you'll just download an empty zip folder
@app.route('/download.html')
def upload_file():
return render_template('download.html')
@app.route('/return-file/')
def database_download():
#sends the newly created zip file containing the LOG_00000.txt, SYS_00000.csv, STAT_00000.csv, MONO_00000.csv, MONO_00000_RAW.csv, and POSE_00000.csv files
with ZipFile('/home/arlw/Desktop/rfhoming/payload_colcon_ws/Zipped_file.zip', 'w') as zip_object:
# Traverse all files in directory
for folder_name, sub_folders, file_names in os.walk('/home/arlw/Desktop/rfhoming/payload_colcon_ws/src/rfhoming2/rfhoming2/Outputs'):
for filename in file_names:
# Create filepath of files in directory
file_path = os.path.join(folder_name, filename)
# Add files to zip file
zip_object.write(file_path, os.path.basename(file_path))

if os.path.exists('/home/arlw/Desktop/rfhoming/payload_colcon_ws/Zipped_file.zip'):
print("ZIP file created")
else:
print("ZIP file not created")
return send_file('/home/arlw/Desktop/rfhoming/payload_colcon_ws/Zipped_file.zip')

#hosts the website and displays it
if __name__=="__main__":
app.run(host="0.0.0.0", port=8080)
