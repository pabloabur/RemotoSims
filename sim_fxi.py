# HULTBORN, PIERROT 1979b
# Intracellular recording from one RC
# RC impaled with microelectrodes and injected with depolirizing step currents of
# constant, but varied strength. Pulse duration of approximately 90ms in cat
# spinal cord.

import time


import matplotlib.pyplot as plt
import numpy as np

from Configuration import Configuration
from InterneuronPool import InterneuronPool
from SynapsesFactory import SynapsesFactory

def simulator():

    conf = Configuration('conffxi.rmto')

    pools = dict()
    pools[0] = InterneuronPool(conf, 'RC', 'ext')

    Syn = SynapsesFactory(conf, pools)

    t = np.arange(0.0, conf.simDuration_ms, conf.timeStep_ms)

    memb_mV = np.zeros_like(t)

    tic = time.clock()
    for i in xrange(0, len(t)):
        # t=step*i [ms]
        # Current in nA
        if i>400 and i<10000:
            pools[0].iInjected[0] = 20
        else:
            pools[0].iInjected[0] = 0
        pools[1].atualizePool(t[i])
        pools[0].atualizeInterneuronPool(t[i])
        memb_mV[i] = pools[0].v_mV[0] 
    toc = time.clock()
    print str(toc - tic) + ' seconds'

    pools[0].listSpikes()
    plt.figure()
    plt.plot(pools[0].poolSomaSpikes[:, 0],
         pools[0].poolSomaSpikes[:, 1] + 1, '.')

    instFiring = np.zeros([1, len(pools[0].poolSomaSpikes[:, 0])-1], dtype=float)
    for i in xrange(1, len(pools[0].poolSomaSpikes[:, 0])):
        instFiring[0][i-1] = 1/(pools[0].poolSomaSpikes[:, 0][i]-
                                pools[0].poolSomaSpikes[:, 0][i-1])
    plt.figure()
    plt.plot(instFiring[0], '.')

    plt.figure()
    plt.plot(t, memb_mV, '-')
    
if __name__ == '__main__':

    np.__config__.show()
    simulator()
    # Problems: previously it was an area, now I have to put length and diameter;
    # There are some parameters I cannot find
    # TODO no ISI shrinking. Find and change parameters and work it out
    # TODO position here too?
    plt.show()
