import usb.core
import usb.util
import sys
from time import gmtime, strftime
import time
import threading
import copy
import lcm
from exlcm import example_t

DED_ZONE = 120
Z_DED_ZONE = 250
DIFF_SIZE = 5
Z_DIFF_SIZE = 10

dev = usb.core.find(idVendor=0x46d, idProduct=0xc626)
if dev is None:
    raise ValueError('SpaceNavigator not found');
else:
    print('SpaceNavigator found')
    print(dev)

cfg = dev.get_active_configuration()
print('cfg is ', cfg)
intf = cfg[(0,0)]
print('intf is ', intf)
ep = usb.util.find_descriptor(intf, custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)
print('ep is ', ep)

reattach = False
if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)

ep_in = dev[0][(0,0)][0]
ep_out = dev[0][(0,0)][1]

print('')
print('Exit by pressing any button on the SpaceNavigator')
print('')

Z_push = 0
old_Z_push = 0

#######X,Y,Zの値###########
R_list = [0,0,0]
old_R_list = 0

Button_number = 0

Mode = 0


######publishされたら動く#########################
def my_handler(channel, data):
    msg = example_t.decode(data)
    
    print("Received message on channel \"%s\"" % channel)
    print("   mode   = %s" % str(msg.mode))
    print("   position    = %s" % str(msg.position))
    print("")
    print("number only type:")

    Mode = msg.mode

def subscribe_handler(handle):
    while True:
        handle()

msg = example_t()
lc = lcm.LCM()
subscription = lc.subscribe("EXAMPLE", my_handler)

########handleをwhileでぶん回すのをサブスレッドで行う############
thread1 = threading.Thread(target=subscribe_handler, args=(lc.handle,))
thread1.start()
print("EXAMPLEチャンネルを読んでTAMAGOチャンネルに送る")


run = True
while run:
    try:
        data = dev.read(ep_in.bEndpointAddress, ep_in.bLength, 0)

        #Z軸のプッシュ判定
        if data[0] == 1:
            old_Z_push = copy.deepcopy(Z_push)
            Z_push = data[5] + (data[6]*256)

            if data[6] > 127:
                Z_push -= 65536

            #デッドゾーンの処理
            if Z_push <= Z_DED_ZONE and Z_push >= -Z_DED_ZONE:
                Z_push = 0

            #感度の処理
            diff = abs(Z_push - old_Z_push)
            if diff > Z_DIFF_SIZE and sum(R_list) == 0:
                print("Push: ",Z_push)

        #回転の移動判定
        if data[0] == 2:
            old_R_list = copy.deepcopy(R_list)
            R_list[0] = data[1] + (data[2]*256)
            R_list[1] = data[3] + (data[4]*256)
            R_list[2] = data[5] + (data[6]*256)
            
            if data[2] > 127:
                R_list[0] -= 65536
            if data[4] > 127:
                R_list[1] -= 65536
            if data[6] > 127:
                R_list[2] -= 65536

            #デッドゾーンの処理
            for i in range(3):
                if R_list[i] <= DED_ZONE and R_list[i] >= -DED_ZONE :
                    R_list[i] = 0

            #感度の処理
            diff = abs(sum(R_list) - sum(old_R_list))
            if diff > DIFF_SIZE and abs(Z_push) < Z_DED_ZONE:
                print("R: ", R_list[0], R_list[1], R_list[2])

        #ボタンの判定(左が2,右が1,同時押しが3)
        if data[0] == 3:
            if data[1]== 0:
                msg.mode = Mode
                print("push button : ", Button_number)
                if Button_number == 1:
                    if msg.mode == 2:
                        msg.mode = 0
                    else:
                        msg.mode += 1
                    if msg.mode == 1:
                        RC_flag = 0
                elif Button_number == 2:
                    if msg.mode == 0:
                        msg.mode = 2
                    else:
                        msg.mode -= 1
                    if msg.mode == 1:
                        RC_flag = 0
                elif Button_number == 3:
                    pass
                print("Now Mode:",msg.mode)
                lc.publish("EXAMPLE", msg.encode())

                Button_number = 0

            else:
                Button_number = data[1]

    except KeyboardInterrupt:
        print("end")
        break

    except usb.core.USBError:
        print("USB error")
    

# end while
usb.util.dispose_resources(dev)

if reattach:
    dev.attach_kernel_driver(0)
