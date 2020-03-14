#pull in main library
import pyvisa
import numpy as np
from struct import unpack
import pylab
import sched, time


rm = pyvisa.ResourceManager()

tekMDO = rm.open_resource('TCPIP::192.168.1.177::INSTR')

#execute to show connection has been made
print(tekMDO.query('*IDN?'))

#Variables for holding Volts and Time
Volts = 0
Time = 0

#Function to call for recording waveform of expanding size
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
    return;

#generate timestamp for beginning reading
#call recordWave(1,500)
#store recording in text file
#plot and show if reading == 1 ? maybe?


#pylab plotting
#py lab plotting very similar to matlab scripting language,ArithmeticError use '-r'
#in plot to define red plotting line
#pylab.plot(Time, Volts)
#pylab.xlim(start, finish)
#pylab.ylim(zero, lim)
#pylab.xlabel('X Label')
#pylab.ylabel('Y Label')
#pylab.title('Title')



    
