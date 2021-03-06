import numpy as np
@nrp.MapVariable("eye_vel", scope=nrp.GLOBAL)
@nrp.MapVariable("isSaccade", initial_value=0, scope=nrp.GLOBAL)
@nrp.MapVariable("DCN_output", initial_value=0, scope=nrp.GLOBAL)
@nrp.MapVariable("indexx", initial_value=0)
@nrp.MapVariable("bufferr", initial_value=np.zeros(5))
@nrp.MapSpikeSink("positive_dcn", nrp.brain.dcn_p, nrp.population_rate)
@nrp.MapSpikeSink("negative_dcn", nrp.brain.dcn_n, nrp.population_rate)
@nrp.MapCSVRecorder("recorder_DCN", filename="DCN_output.csv", headers=["time", "positive", "negative"])
def  (t, eye_vel, isSaccade, DCN_output, positive_dcn, negative_dcn, indexx, bufferr, recorder_DCN):
    if eye_vel.value is None:
        return 0.0
    command = positive_dcn.rate - negative_dcn.rate 
    bufferr.value[indexx.value] = command
    indexx.value = indexx.value + 1
    if indexx.value == 5:
        indexx.value = 0
    mean_comm = np.mean(bufferr.value)
    gain = 0.009
    ret = gain * mean_comm
    recorder_DCN.record_entry(t, positive_dcn.rate, negative_dcn.rate)
    DCN_output.value = ret
