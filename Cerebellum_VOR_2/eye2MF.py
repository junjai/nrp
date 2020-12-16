import numpy as np
@nrp.MapVariable("eye_position", scope=nrp.GLOBAL)

@nrp.MapSpikeSource("MF_pos", nrp.map_neurons(range(100), lambda i: nrp.brain.mf[i]), nrp.poisson, delay=1.0)
@nrp.Robot2Neuron()
def eye2MF (t, eye_position, MF_pos):
    if eye_position.value is not None:
        def PD_gaussian(x, mu, sigma):
            y = 1/(sigma * np.sqrt(2 * np.pi)) *np.exp( - (x - mu)**2 / (2 * sigma**2) )
            return y
        m = np.linspace(-0.5, 0.2, 6)[1:-1]
        sd = 0.05
        max_fr = 200 / PD_gaussian(0, 0, sd) 
        MF_pos.rate = max_fr * PD_gaussian(eye_position.value, np.linspace(-1, 1, 100), sd)
    #    MF_pos1.rate = max_fr * PD_gaussian(eye_position.value, m[0], sd) 
    #    MF_pos2.rate = max_fr * PD_gaussian(eye_position.value, m[1], sd)  
        #clientLogger.info('mf: ', MF_pos)
        #clientLogger.info('eyepos: ', eye_position.value)
        #clientLogger.info('rate: ',MF_pos1.rate, MF_pos2.rate, MF_pos3.rate, MF_pos4.rate)
