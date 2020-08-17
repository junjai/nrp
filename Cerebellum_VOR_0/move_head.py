import numpy as np
@nrp.MapRobotPublisher('head_rotation', Topic('/icub/neck_yaw/pos', std_msgs.msg.Float64))
@nrp.MapCSVRecorder("recorder_neck", filename="neck_angle.csv", headers=["time", "Neck Angle"])
@nrp.MapCSVRecorder("trial_clock", filename="clock.csv", headers=["time", "trial"])
def move_head (t, head_rotation, recorder_neck, trial_clock):
    dt = 0.02
    frequency = 1.0
    HR = 30.0 * (np.pi / 180.0) * np.sin(2. * np.pi * frequency * t)
    head_rotation.send_message(std_msgs.msg.Float64(HR))
    recorder_neck.record_entry(t, HR)

    # record clock
    if t % (1/frequency) < dt:
        trial_clock.record_entry(t, 1)
    else:
        trial_clock.record_entry(t, 0)
    
