# Imported Python Transfer Function
#
import numpy as np
from gazebo_msgs.srv import SetModelState
import rospy
rospy.wait_for_service("/gazebo/set_model_state")
service_proxy = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState, persistent=True)
@nrp.MapVariable("target_freq", initial_value=0.3)
@nrp.MapVariable("target_ampl", initial_value=0.3)
@nrp.MapVariable("target_center", initial_value={'x': 0, 'y': 2.42, 'z': 1.2})
@nrp.MapVariable("set_model_state_srv", initial_value=service_proxy)
@nrp.MapCSVRecorder("recorder_image", filename="target_position.csv", headers=["time", "x"])
@nrp.MapCSVRecorder("clock", filename="clock.csv", headers=["time", "clock"])
@nrp.Robot2Neuron() # dummy R2N
def move_target(t, target_freq, target_ampl, target_center, set_model_state_srv, recorder_image, clock):
    dt = 0.02
    ms_msg =  gazebo_msgs.msg.ModelState()
    frequency = target_freq.value
    amplitude = target_ampl.value
    center = target_center.value
    ms_msg.model_name = 'Target'
    # set orientation RYP axes
    ms_msg.pose.orientation.x = 0
    ms_msg.pose.orientation.y = 1
    ms_msg.pose.orientation.z = 1
    # reference frame
    ms_msg.reference_frame = 'world'
    #pose
    ms_msg.pose.position.x = \
        center['x'] + np.sin(t * frequency * 2 * np.pi) * (float(amplitude) / 2)
    ms_msg.pose.position.y = center['y']
    ms_msg.pose.position.z = center['z']
    #scale
    ms_msg.scale.x = ms_msg.scale.y = ms_msg.scale.z = 1.0
    #call service
    response = set_model_state_srv.value(ms_msg)
    #check response
    if not response.success:
        clientLogger.info(response.status_message)
    # record position
    recorder_image.record_entry(t, ms_msg.pose.position.x)
    # record clock
    if t % (1/frequency) < dt:
        clock.record_entry(t, 1)
    else:
        clock.record_entry(t, 0)
    

#

