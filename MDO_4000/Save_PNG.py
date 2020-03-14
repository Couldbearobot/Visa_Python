#pull in main library
import pyvisa

rm = pyvisa.ResourceManager()

tekMDO = rm.open_resource('TCPIP::192.168.1.177::INSTR')

print(tekMDO.query('*IDN?'))

tekMDO.write('SAVE:IMAG:FILEF PNG')

tekMDO.write('HARDCOPY START')
raw_data = tekMDO.read_raw()

fid = open('my_image.png', 'wb')
fid.write(raw_data)
fid.close()
print('Done')
