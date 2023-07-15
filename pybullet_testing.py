import pybullet
import pybullet_data

pybullet.connect(pybullet.GUI)
pybullet.resetSimulation()

def add_robot(self):
    self.robot_urdf_path = self.bullet_data_path



pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
plane = pybullet.loadURDF("plane.urdf")

pybullet.setAdditionalSearchPath("C:\\Users\\stefa\\OneDrive - Universidad del Valle de Guatemala\\UVG\\Tesis\\kuka_experimental")
robot = pybullet.loadURDF("\\kuka_kr6_support\\urdf\\kr6r700sixx.xacro")

pybullet.setGravity(0,0,-9.81)
pybullet.setTimeStep(0.0001)
pybullet.setRealTimeSimulation(1)
# pybullet.setJointMotorControlArray(
#     robot, range(6), pybullet.POSITION_CONTROL,
#     targetPositions=[0.1] * 6)
# 
# for _ in range(10000):
#     pybullet.stepSimulation()
#
