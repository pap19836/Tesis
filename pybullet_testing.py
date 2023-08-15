import pybullet
import pybullet_data
import math

# Connect to simulation
pybullet.connect(pybullet.GUI)
pybullet.resetSimulation()

# Set plane in simulation
pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
plane = pybullet.loadURDF("plane.urdf")


# Load robot URDF
#robot = pybullet.loadURDF("kuka_experimental/kuka_kr120_support/urdf/kr120r2500pro.urdf",[0,0,3],useFixedBase=1)
robot = pybullet.loadURDF("robonova/robot.urdf",[0,0,0.3],useFixedBase=1)

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

# Initialize Simulation
pybullet.setGravity(0,0,-9.81)
pybullet.setTimeStep(0.0001)
pybullet.setRealTimeSimulation(1)

# Run Simulation
while True:
    pybullet.stepSimulation()
    slider_values = []
    for i in range(numJoints):
        x = pybullet.readUserDebugParameter(i)
        slider_values.append(x)
    pybullet.setJointMotorControlArray(robot,joint_number,pybullet.POSITION_CONTROL, slider_values)