'''
Acquire a RF waveform from a MDO and plot it.


python 2.7 (http://www.python.org/)
pyvisa 1.3 (http://pypi.python.org/pypi/PyVISA/1.3)
Numpy 1.6.1 (http://sourceforge.net/projects/numpy/)
'''
import visa
import numpy as np
import pyvisa
from struct import unpack


def GetCurve(scope):
    temp = scope.timeout
    scope.timeout = 20
    scope.query('CURVE?')
    data = scope.read_raw()
    scope.timeout = temp
    headerlen = 2 + int(data[1])
    header = data[:headerlen]
    wave = data[headerlen:-1]
    return header, wave

rm = pyvisa.ResourceManager()
scope = rm.open_resource('TCPIP::192.168.1.177::INSTR')
print(scope.query('*IDN?'))

scope.query('DATA:SOU RF_NORMAL')
datalen = int(scope.query('wfmpre:nr_pt?'))
start = float(scope.query('rf:start?'))
stop = float(scope.query('rf:stop?'))
scope.write('DATA:ENC SFP')
header, datac = GetCurve(scope)

#each point is a floating point value, 4 bytes per point
datac = unpack('%sf' % datalen,datac)
step = (stop - start) / (len(datac)-1)
x = np.arange(start, stop + step, step)
y = np.array(datac)
y = 10 * np.log10(y/.001)



pyvisa.plot(x,y)
pyvisa.xlim(start, stop)
pyvisa.show()
