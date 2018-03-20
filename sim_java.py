import time


import matplotlib.pyplot as plt
import numpy as np

from Configuration import Configuration
from MotorUnitPool import MotorUnitPool
from InterneuronPool import InterneuronPool
from NeuralTract import NeuralTract
from SynapsesFactory import SynapsesFactory

def simulator():

    conf = Configuration('confjava.rmto')

    pools = dict()
    pools[0] = MotorUnitPool(conf, 'SOL')
    pools[1] = InterneuronPool(conf, 'RC', 'ext')

    Syn = SynapsesFactory(conf, pools)

    t = np.arange(0.0, conf.simDuration_ms, conf.timeStep_ms)

    RC_mV = np.zeros_like(t)
    MN_mV = np.zeros_like(t)

    tic = time.clock()
    for i in xrange(0, len(t)):
        pools[0].iInjected[1] = 10
        pools[0].atualizeMotorUnitPool(t[i]) # MN pool
        pools[2].atualizePool(t[i]) # RC synaptic Noise
        pools[1].atualizeInterneuronPool(t[i]) # RC pool
        RC_mV[i] = pools[1].unit[0].v_mV[0] 
        MN_mV[i] = pools[0].unit[0].v_mV[1] 
    toc = time.clock()
    print str(toc - tic) + ' seconds'

    pools[0].listSpikes()

    plt.figure()
    plt.plot(t, MN_mV, '-')
    
    plt.figure()
    plt.plot(pools[0].poolSomaSpikes[:, 0],
        pools[0].poolSomaSpikes[:, 1]+1, '.')

    plt.figure()
    plt.plot(t, RC_mV, '-')
    
if __name__ == '__main__':

    np.__config__.show()
    simulator()
    plt.show()
