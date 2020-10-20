#!/usr/bin/env python
#coding: utf-8

import b3mCtrl
import time



if __name__ == '__main__':
    aaa = b3mCtrl.B3mClass()
    aaa.begin("/dev/ttyUSB0",1500000)
    
    # idx= [0,1,3]
    idx= [0]
    center=0

    for id in idx:
        print("id = ",str(id))
        run =1
        while run:
            hoge = aaa.setRam(id, 0,"PositionCenterOffset")
                
            if(hoge[0] != False):
                print("hoge = ",hoge)
                run=0
            if(hoge is not False):
                #print(id)
                pass
        run =1
        while run:
            hoge2 = aaa.getRam(id,"CurrentPosition")

            if(hoge2[0] != False):
                if hoge2[0]>18000:
                    center=hoge2[0]-36000
                elif hoge2[0]<-18000:
                    center=hoge2[0]+36000
                else :
                    center=hoge2[0]
                print("hoge2 = ",hoge2[0])
                print("center = ",center)
                run=0
            if(hoge2 is not False):
                #print(id)
                pass

        run=1
        while run:
            hoge = aaa.setRam(id, center,"PositionCenterOffset")
                
            if(hoge[0] != False):
                print("hoge = ",hoge)
                run=0
            if(hoge is not False):
                #print(id)
                pass

        run=1
        while run:
            hoge2 = aaa.getRam(id,"CurrentPosition")

            if(hoge2[0] != False):
                print("hoge2 = ",hoge2[0])
                run=0
            if(hoge2 is not False):
                #print(id)
                pass

        print (aaa.setTrajectoryType(id,"EVEN"))
        print (aaa.setMode(id,"POSITION"))
        print (aaa.positionCmd(id,9000,2))
        time.sleep(3)
        print (aaa.positionCmd(id,0,2))
        time.sleep(2)
        print (aaa.setMode(id,"FREE"))
            
