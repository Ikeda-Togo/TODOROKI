import time
import serial
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import blv_test_lib
client = serial.Serial("/dev/ttyXRUSB0", 115200, timeout=0.1, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE) # COMポートは自分の奴を入れる
#client = serial.Serial("/dev/ttyACM0", 115200, timeout=10, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE) # COMポートは自分の奴を入れる

motor1 = blv_test_lib.blv_motor(client,2)
#motor1.set_speed_and_go(100,1,0)
# motor1.set_speed_and_go(200,0,1)

motor1.set_speed(int(100))
motor1.go(0,1)
print("go:1000")
time.sleep(5)

motor1.set_speed(1000)
motor1.go(0,1)
print("go:100")
time.sleep(5)
#time.sleep(3)

motor1.set_speed_and_go(0,0,0)
