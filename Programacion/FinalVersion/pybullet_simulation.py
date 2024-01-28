#!C:\Users\stefa\OneDrive - Universidad del Valle de Guatemala\UVG\Tesis\Programacion\tesis_env\Scripts\python.exe"
import pybullet
import pybullet_data
from numpy import rad2deg
# IP Socket Config
import socket
import json
import numpy as np
from time import time
def pb():
    global servoValues
    global joints_info
    global activeConnection
    global realCoreo
    global uploadCoreo
    global playRealCoreo
    global controlFlag
    global coreoExists
    global vm, pm
    global checkConnectionThread
    global connected
    global repeatCB
    global numJoints, servo2, old_servo_values
    repeatCB = False
    oldRepeatStatus = False
    controlFlag = True
    activeConnection = False
    uploadCoreo = False
    playRealCoreo = False
    coreoExists = False
    connected = False
    ip = '192.168.107.177'
    port = 8091
    def checkConnectionFnc(ip, port):
        global connected
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((ip,port))
            #global connected
            connected = True
            #print(connected)
            sock.close()
        except TimeoutError:
            #global connected
            connected = False
            #print(connected)
        global checkConnectionThread
        del(checkConnectionThread)
    # checkConnectionThread = threading.Timer(5,checkConnectionFnc, args=(ip,port))
    # checkConnectionThread.start()
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
    plane = pybullet.loadURDF("plane/plane.urdf")

    # Load robot URDF
    robot = pybullet.loadURDF("robonova//robot.urdf",
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
    play_dict = {}
    repeat_dict = {}
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
    vm = pybullet.computeViewMatrixFromYawPitchRoll(
                        distance=0.50,
                        roll=0,
                        pitch=-30,
                        yaw=45,
                        cameraTargetPosition=[0,0,0.25],
                        upAxisIndex=2)
    while True:
        # if not("checkConnectionThread" in globals()):
        #     checkConnectionThread = threading.Timer(5,checkConnectionFnc, args=(ip,port))
        #     checkConnectionThread.start()
        pybullet.stepSimulation()
        pybullet.setJointMotorControlArray(robot,joint_number,
                                           pybullet.POSITION_CONTROL,
                                           servoValues, maxForce)
        servo2 = []

        if activeConnection == True and connected == False:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                s.settimeout(3)
                s.connect((ip,port))
                s.settimeout(None)
                connected = True
                print("Robonova Connected")
            except TimeoutError:
                connected = False
                del(s)
                print("Timeout")
        # if ("s" in locals()):
        #     try:
        #         s.settimeout(2)
        #         data = s.recv(4)
        #         s.settimeout(None)
        #         #print(data)
        #     except OSError as err:
        #         del(s)
        #         connected = False
        #         print(err)

        for i in range(numJoints):
            x = servoValues[i]
            servo2.append(x)
        if ((old_servo_values != servo2) & (activeConnection == True))\
            & (playRealCoreo!= True) & (controlFlag) & (connected):
            n = 0
            for key in joint_dict.keys():
                joint_dict[key] = round(rad2deg(servoValues[n])+90,2)
                n = n+1
            joint_dict["playCoreo"] = False
            joint_dict['uploadCoreo'] = False
            
            old_servo_values = servo2
            data_json = json.dumps(joint_dict)
            joint_dict.pop("uploadCoreo")
            joint_dict.pop("playCoreo")
            try:
                s.sendall(bytes(data_json+"\n", "utf-8"))
            except OSError as err:
                connected = False
                print(err)
            
        if playRealCoreo:
            play_dict["playCoreo"] = True
            data_json = json.dumps(play_dict)
            try:
                s.sendall(bytes(data_json+"\n", "utf-8"))
            except OSError as err:
                connected = False
                print(err)
            playRealCoreo = False

        if (repeatCB != oldRepeatStatus) and (connected):
            oldRepeatStatus = repeatCB
            play_dict["repeat"] = repeatCB
            data_json = json.dumps(play_dict)
            try:
                s.sendall(bytes(data_json+"\n", "utf-8"))
            except OSError as err:
                connected = False
                print(err)
        if(uploadCoreo):
            for key in coreo_dict.keys():
                coreo_dict[key].clear()
            realCoreo = np.array(realCoreo).T.tolist()
            n = 0
            for key in coreo_dict.keys():
                coreo_dict[key] = [round(rad2deg(float(x))+90,2) for x in realCoreo[n]]
                n = n+1
                coreoLen = len(coreo_dict[key])
            coreo_dict['uploadCoreo'] = uploadCoreo
            coreo_dict["coreoLen"] = coreoLen
            data_json = json.dumps(coreo_dict)
            coreo_dict.pop('uploadCoreo')
            coreo_dict.pop("coreoLen")

            print("Data stored successfully!")
            try:
                s.sendall(bytes(data_json+"\n", "utf-8"))
            except OSError as err:
                connected = False
                print(err)
            coreoExists = True
            uploadCoreo = False
            print(data_json)