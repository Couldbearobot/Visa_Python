#pull in main library
#from record waveform example
import pyvisa
import numpy as np
from struct import unpack
import pylab
#from timer example
import sched, time
from math import log10, floor
def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))

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

#from Timer example
#generate timestamp for beginning reading
t_then = 0
t_now = 0
diff = 0
t_total = 0

s = sched.scheduler(time.time, time.sleep)

def print_time():
    global t_now, t_then, diff, t_total
    t_now = time.time()
    #print ("From t_now", t_now)
    #print ("From t_then" , t_then)
    diff = t_now - t_then
    
    if diff != t_now:
        #print ("Diff = ", t_now - t_then)
        t_total += round_to_1(diff)
    t_then = t_now
    print('\n')

count = 0

while count <= 5:
    s.enter(2, 1, print_time, ())
    s.run()
    print("Total Time: ", t_total)
    print("Time Printed")
    count = count + 1

print("Completed")

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



    
