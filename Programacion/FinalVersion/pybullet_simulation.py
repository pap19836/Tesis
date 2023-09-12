#!C:\Users\stefa\OneDrive - Universidad del Valle de Guatemala\UVG\Tesis\Programacion\tesis_env\Scripts\python.exe"
import pybullet
import pybullet_data
from numpy import rad2deg, deg2rad
# IP Socket Config
import socket
import json


def pb():
    global servoValues
    global joints_info
    global activeConnection
    activeConnection = False
    s = socket.socket()
    ip = '192.168.122.177'
    port = 8091

    # Connect to simulation
    pybullet.connect(pybullet.GUI)
    pybullet.resetSimulation()
    pybullet.configureDebugVisualizer(pybullet.COV_ENABLE_GUI,0)
    pybullet.resetDebugVisualizerCamera( cameraDistance=0.8, cameraYaw=45, cameraPitch=-30, cameraTargetPosition=[0,0,0.25])
    # Set plane in simulation
    pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
    plane = pybullet.loadURDF("plane.urdf")

    # Load robot URDF
    robot = pybullet.loadURDF("Programacion/FinalVersion/robonova/robot.urdf",[0,0,0.32],useFixedBase=1)

    # Get Robot info and Initialize servos
    numJoints = pybullet.getNumJoints(robot)
    joints_info = []
    
    for i in range(numJoints):
        x = pybullet.getJointInfo(robot,i)
        joints_info.append(x)
    joint_number = list(range(numJoints))
    joint_dict = {}
    for i in joint_number:
        joint_dict[joints_info[i][1].decode("utf-8")] = None
    # Initialize Simulation
    pybullet.setGravity(0,0,-9.81)
    pybullet.setTimeStep(0.0001)
    pybullet.setRealTimeSimulation(1)
    maxForce = [0.0 for n in servoValues]
    #global old_servo_values
    old_servo_values = [1000]
    connected = False
    # Run Simulation
    pybullet.setJointMotorControlArray(robot,joint_number,pybullet.POSITION_CONTROL, servoValues, maxForce)
    while True:
        pybullet.stepSimulation()
        pybullet.setJointMotorControlArray(robot,joint_number,pybullet.POSITION_CONTROL, servoValues, maxForce)
        servo2 = []

        if activeConnection == True and connected == False:
            s.connect((ip,port))
            connected = True

        for i in range(numJoints):
            x = servoValues[i]
            servo2.append(x)
        if (old_servo_values != servo2) & activeConnection == True:
            joint_dict.update({'LeftShoulder1':int(rad2deg(servoValues[0])+90),
            'LeftShoulder2':int(rad2deg(servoValues[1]))+90,
            'RightShoulder1':int(rad2deg(servoValues[2]))+90,
            'RightShoulder2':int(rad2deg(servoValues[3]))+90,
            'LeftWaist':int(rad2deg(servoValues[4]))+90,
            'LeftHip1':int(rad2deg(servoValues[5]))+90,
            'LeftHip2':int(rad2deg(servoValues[6]))+90,
            'LeftKnee':int(rad2deg(servoValues[7]))+90,
            'LeftAnkle1':int(rad2deg(servoValues[8]))+90, 
            'LeftAnkle2':int(rad2deg(servoValues[9]))+90,
            'RightWaist':int(rad2deg(servoValues[10]))+90,
            'RightHip1':int(rad2deg(servoValues[11]))+90,
            'RightHip2':int(rad2deg(servoValues[12]))+90,
            'RightKnee':int(rad2deg(servoValues[13]))+90,
            'RightAnkle1':int(rad2deg(servoValues[14]))+90,
            'RightAnkle2':int(rad2deg(servoValues[15]))+90})
            old_servo_values = servo2
            data_json = json.dumps(joint_dict)
            s.sendall(bytes(data_json, "utf-8"))
            print(str(joint_dict))