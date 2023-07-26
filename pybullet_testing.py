import pybullet
import pybullet_data
import math

pybullet.connect(pybullet.GUI)
pybullet.resetSimulation()

def add_robot(self):
    self.robot_urdf_path = self.bullet_data_path



pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
plane = pybullet.loadURDF("plane.urdf")

#robot = pybullet.loadURDF("xpp/robots/xpp_hyq/urdf/biped.urdf")
robot = pybullet.loadURDF("kuka_experimental/kuka_kr120_support/urdf/kr120r2500pro.urdf",[0,0,3],useFixedBase=1)
position, orientation = pybullet.getBasePositionAndOrientation(robot)
numJoints = pybullet.getNumJoints(robot)

joints_info = []
for i in range(numJoints):
    x = pybullet.getJointInfo(robot,i)
    joints_info.append(x)
joint_number = list(range(numJoints))
pybullet.setGravity(0,0,-9.81)
pybullet.setTimeStep(0.0001)
pybullet.setRealTimeSimulation(1)
slider_parameters = []
for i in range(numJoints):
    x = pybullet.addUserDebugParameter(' '+str(joints_info[i][1], 'utf-8'),joints_info[i][8],joints_info[i][9], 0)
    slider_parameters.append(x)



#    robot, range(6), pybullet.POSITION_CONTROL,
#    targetPositions=[0.1] * 6)
while True:
    pybullet.stepSimulation()
    slider_values = []
    for i in range(numJoints):
        x = pybullet.readUserDebugParameter(i)
        slider_values.append(x)
    pybullet.setJointMotorControlArray(robot,joint_number,pybullet.POSITION_CONTROL, slider_values)