import b3mCtrl
import time

if __name__ == '__main__':
    aaa = b3mCtrl.B3mClass()
    aaa.begin("/dev/ttyUSB0",1500000)
    idx = [4,5,6,7,8,9]
    print (aaa.setTrajectoryType(255,"EVEN"))
    print (aaa.setMode(255,"POSITION"))
    
    for id in idx:
        # print (aaa.setTrajectoryType(255,"EVEN"))

        input()
        print (aaa.positionCmd(id,0,2))
        # input()
        # print (aaa.positionCmd(id,0,2))
    
    print("enter FREE MODE")
    input()
    print (aaa.setMode(255,"FREE"))
