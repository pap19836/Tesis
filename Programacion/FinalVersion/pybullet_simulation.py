#!C:\Users\stefa\OneDrive - Universidad del Valle de Guatemala\UVG\Tesis\Programacion\tesis_env\Scripts\python.exe"
import pybullet
import pybullet_data
from numpy import rad2deg
# IP Socket Config
import socket
import json
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from time import time
def pb():
    global servoValues
    global joints_info
    global activeConnection
    global realCoreo
    global uploadCoreo
    global vm, pm
    activeConnection = False
    uploadCoreo = False
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ip = '192.168.7.177'
    port = 8091

    # Connect to simulation
    pybullet.connect(pybullet.GUI, options="--width=960--height=1080")
    pybullet.resetSimulation()
    pybullet.configureDebugVisualizer(pybullet.COV_ENABLE_GUI,0)
    pybullet.resetDebugVisualizerCamera(cameraDistance=0.5,
                                        cameraYaw=45,
                                        cameraPitch=-30,
                                        cameraTargetPosition=[0,0,0.25])
    # Set plane in simulation
    pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
    plane = pybullet.loadURDF("plane.urdf")

    # Load robot URDF
    robot = pybullet.loadURDF("Programacion/FinalVersion/robonova/robot.urdf",
                              [0,0,0.32],useFixedBase=1)

    # Get Robot info and Initialize servos
    
    numJoints = pybullet.getNumJoints(robot)
    joints_info = []
    joint_name = []
    for i in range(numJoints):
        x = pybullet.getJointInfo(robot,i)
        joints_info.append(x)
    joint_number = list(range(numJoints))
    joint_dict = {}
    coreo_dict = {}
    for i in joint_number:
        joint_dict[joints_info[i][1].decode("utf-8")] = None
        coreo_dict[joints_info[i][1].decode("utf-8")] = {}
    # Initialize Simulation
    pybullet.setGravity(0,0,-9.81)
    pybullet.setTimeStep(0.0001)
    pybullet.setRealTimeSimulation(1)
    maxForce = [0.0 for n in servoValues]
    #global old_servo_values
    old_servo_values = [1000]
    connected = False

    # Run Simulation
    pybullet.setJointMotorControlArray(robot,joint_number,
                                       pybullet.POSITION_CONTROL,
                                       servoValues, maxForce)
    # Simulation image
    w = 360
    h = 270
    ch = 4
    
    pm = pybullet.computeProjectionMatrixFOV(fov=90, 
                aspect=w/h, nearVal=0.1, farVal=10)

    while True:
        vm = pybullet.computeViewMatrixFromYawPitchRoll(
                        distance=0.50,
                        roll=0,
                        pitch=-30,
                        yaw=45,
                        cameraTargetPosition=[0,0,0.25],
                        upAxisIndex=2)
        pybullet.stepSimulation()
        pybullet.setJointMotorControlArray(robot,joint_number,
                                           pybullet.POSITION_CONTROL,
                                           servoValues, maxForce)
        servo2 = []

        if activeConnection == True and connected == False:
            s.connect((ip,port))
            connected = True

        for i in range(numJoints):
            x = servoValues[i]
            servo2.append(x)
        if (old_servo_values != servo2) & activeConnection == True:
            n = 0
            for key in joint_dict.keys():
                joint_dict[key] = rad2deg(servoValues[n])+90
                n = n+1
            joint_dict['uploadCoreo'] = False
            old_servo_values = servo2
            data_json = json.dumps(joint_dict)
            joint_dict.pop("uploadCoreo")
            try:
                s.sendall(bytes(data_json, "utf-8"))
            except OSError:
                pass
            print(data_json)
        if(uploadCoreo):
            for key in coreo_dict.keys():
                coreo_dict[key].clear()
            realCoreo = np.array(realCoreo).T.tolist()
            n = 0
            for key in coreo_dict.keys():
                coreo_dict[key] = [rad2deg(float(x))+90 for x in realCoreo[n]]
                n = n+1
            coreo_dict['uploadCoreo'] = uploadCoreo
            data_json = json.dumps(coreo_dict)
            coreo_dict.pop('uploadCoreo')
            s.sendall(bytes(data_json, "utf-8"))
            uploadCoreo = False
            print(data_json)