#pull in main library
import pyvisa
import numpy as np
from struct import unpack
import pylab

rm = pyvisa.ResourceManager()

tekMDO = rm.open_resource('TCPIP::192.168.1.177::INSTR')

print(tekMDO.query('*IDN?'))


def recordWave (strt, fnsh):
    tekMDO.write('DATA:SOU CH1')
    #Transfer 500 data points
    tekMDO.write('DATA:START ' + str(strt))
    tekMDO.write('DATA:STOP ' + str(fnsh))
    tekMDO.write('DATA:WIDTH 1')
    #Data:ENCdg Specifics coding format 
    tekMDO.write('DATA:ENC RPB')

    ymult = float(tekMDO.query('WFMPRE:YMULT?'))
    yzero = float(tekMDO.query('WFMPRE:YZERO?'))
    yoff = float(tekMDO.query('WFMPRE:YOFF?'))
    xincr = float(tekMDO.query('WFMPRE:XINCR?'))

    tekMDO.write('CURVE?')
    data = tekMDO.read_raw()
    headerlen = 2 + int(data[1])
    header = data[:headerlen]
    ADC_wave = data[headerlen:-1]
    ADC_wave = np.array(unpack('%sB' % len(ADC_wave), ADC_wave))
    Volts = (ADC_wave - yoff) * ymult + yzero
    Time = np.arange(0, xincr * len(Volts), xincr)
