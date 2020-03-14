#pull in main library
import pyvisa
import numpy as np
from struct import unpack
import pylab


rm = pyvisa.ResourceManager()

tekMDO = rm.open_resource('TCPIP::192.168.1.177::INSTR')

print(tekMDO.query('*IDN?'))
#see source material(SSM) pg 250
#DATa:SOUrce Specifies source waveform to be transfered from oscilliscope using CURve? command
#valid waveform sources
#DATa:SOUrce
#{CH1|CH2|CH3|CH4|MATH|REF1|REF2|REF3|REF4|D0|D1|D2|D3
#|D4|D5|D6|D7|D8|D9|D10|D11|D12|D13|D14|D15|DIGital
#|RF_AMPlitude|RF_FREQuency|RF_PHASe|RF_NORMal|RF_AVErage|
#RF_MAXHold|RF_MINHold}
tekMDO.write('DATA:SOU CH1')

#Transfer 500 data points
tekMDO.write('DATA:START 1')
tekMDO.write('DATA:STOP 500')

#SSM: 253
#Specifies width: bytes per point, for a waveform data when using CURve?
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

pylab.plot(Time, Volts)
pylab.show()

print('Done')



