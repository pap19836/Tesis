import pybullet
import pybullet_data
import math
from numpy import rad2deg
# IP Socket Config
import socket
from time import sleep
import json
s = socket.socket()
ip = '192.168.122.32'
port = 8091
s.connect((ip,port))

# Connect to simulation
pybullet.connect(pybullet.GUI)
pybullet.resetSimulation()

# Set plane in simulation
pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
plane = pybullet.loadURDF("plane.urdf")


# Load robot URDF
robot = pybullet.loadURDF("Programacion/FinalVersion/robonova/robot.urdf",[0,0,0.3],useFixedBase=1)

# Get Robot info and set sliders
position, orientation = pybullet.getBasePositionAndOrientation(robot)
numJoints = pybullet.getNumJoints(robot)
joints_info = []
slider_parameters = []
for i in range(numJoints):
    x = pybullet.getJointInfo(robot,i)
    joints_info.append(x)
    y = pybullet.addUserDebugParameter(' '+str(joints_info[i][1], 'utf-8'),joints_info[i][8],joints_info[i][9], 0)
    slider_parameters.append(y)
joint_number = list(range(numJoints))

joint_dict = {}
for i in joint_number:
   joint_dict[joints_info[i][1].decode("utf-8")] = None
# Initialize Simulation
pybullet.setGravity(0,0,-9.81)
pybullet.setTimeStep(0.0001)
pybullet.setRealTimeSimulation(1)
old_slider_values = 0
# Run Simulation
while True:
    pybullet.stepSimulation()
    slider_values = []
    for i in range(numJoints):
        x = pybullet.readUserDebugParameter(i)
        slider_values.append(x)
    pybullet.setJointMotorControlArray(robot,joint_number,pybullet.POSITION_CONTROL, slider_values)
    if slider_values != old_slider_values:
        old_slider_values = slider_values
        joint_dict.update({'LeftShoulder1':rad2deg(slider_values[0]),
        'LeftShoulder2':rad2deg(slider_values[1]),
        'RightShoulder1':rad2deg(slider_values[2]),
        'RightShoulder2':rad2deg(slider_values[3]),
        'LeftWaist':rad2deg(slider_values[4]),
        'LeftHip1':rad2deg(slider_values[5]),
        'LeftHip2':rad2deg(slider_values[6]),
        'LeftKnee':rad2deg(slider_values[7]),
        'LeftAnkle1':rad2deg(slider_values[8]),
        'LeftAnkle2':rad2deg(slider_values[9]),
        'RightWaist':rad2deg(slider_values[10]),
        'RightHip1':rad2deg(slider_values[11]),
        'RightHip2':rad2deg(slider_values[12]),
        'RightKnee':rad2deg(slider_values[13]),
        'RightAnkle1':rad2deg(slider_values[14]),
        'RightAnkle2':rad2deg(slider_values[15])})

        data_json = json.dumps(joint_dict)
    
    
        s.sendall(bytes(data_json, "utf-8"))
        print('split'+str(rad2deg(slider_values)))
