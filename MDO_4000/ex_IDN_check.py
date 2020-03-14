#pull in main library
import pyvisa

rm = pyvisa.ResourceManager()

my_instr = rm.open_resource('TCPIP::192.168.1.177::INSTR')
print(my_instr.query('*IDN?'))

