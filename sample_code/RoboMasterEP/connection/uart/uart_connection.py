import serial

ser = serial.Serial()

# uart config baudrate 115200, bytesize 8, stopbit 1, prity None, timeout 0.2s
ser.port = 'COM3'
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.stopbits = serial.STOPBITS_ONE
ser.parity = serial.PARITY_NONE
ser.timeout = 0.2

# open uart
ser.open()

ser.write('command'.encode('utf-8'))
print('send data to ser.  : command')
recv = ser.read()
print('recv data from ser.: %s'%recv)


ser.write('version'.encode('utf-8'))
print('send data to ser.  : version ?')
recv = ser.read()
print('recv data from ser.: %s'%recv)

ser.write('quit'.encode('utf-8'))
print('send data to ser.  : quit')
recv = ser.read()
print('recv data from ser.: %s'%recv)

ser.close()
