# Imported Python Transfer Function
#
from sensor_msgs.msg import JointState
@nrp.MapVariable("eye_position", initial_value=None, scope=nrp.GLOBAL)
@nrp.MapRobotSubscriber("joints", Topic("/icub/joints", JointState))
@nrp.MapCSVRecorder("recorder_eye", filename="eye_angle.csv", headers=["time", "eye angle"])
@nrp.Robot2Neuron()
def set_eyepos(t, eye_position, joints, recorder_eye):
    joints = joints.value
    if joints is not None:
        eye_position.value = joints.position[joints.name.index('eye_version')]
        recorder_eye.record_entry(t, joints.position[joints.name.index('eye_version')])
#

