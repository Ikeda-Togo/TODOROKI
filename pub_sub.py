import time
import threading
import lcm
from exlcm import example_t
def my_handler(channel, data):
    msg = example_t.decode(data)
    
    print("Received message on channel \"%s\"" % channel)
    print("   mode   = %s" % str(msg.mode))
    '''
    print("   position    = %s" % str(msg.position))
    print("   orientation = %s" % str(msg.orientation))
    print("   ranges: %s" % str(msg.ranges))
    print("   name        = '%s'" % msg.name)
    print("   enabled     = %s" % str(msg.enabled))
    '''
    #print(msg.name)
    #print("")

def subscribe_handler(handle):
    while True:
        handle()

msg = example_t()
msg.mode = 0
msg.position = (1, 2, 3)
msg.orientation = (1, 0, 0, 0)
msg.ranges = range(15)
msg.num_ranges = len(msg.ranges)
msg.name = "example string"
msg.enabled = True

lc = lcm.LCM()
subscription = lc.subscribe("EXAMPLE", my_handler)
thread1 = threading.Thread(target=subscribe_handler, args=(lc.handle,))
thread1.start()
print("EXAMPLEチャンネルを読んでTAMAGOチャンネルに送る")
try:
    while True:
        #print("hi")
        msg.mode =int(input("number only type:"))
        lc.publish("EXAMPLE", msg.encode())
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
