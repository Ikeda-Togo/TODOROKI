#!/usr/bin/env python
#coding: utf-8

import b3mCtrl
import time



if __name__ == '__main__':
    aaa = b3mCtrl.B3mClass()
    aaa.begin("/dev/ttyUSB0",1500000)
    
    # idx= [0]
    idx= [4,5,6,7,8,9]
    center=0
    input()

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

        run=1
        while run:
            save = aaa.saveCmd(id)
            
            if(save[0] != False):
                print("save RAM to ROM ",save)
                run=0
            if(save is not False):
                pass


    input()
    print (aaa.setTrajectoryType(255,"EVEN"))
    print (aaa.setMode(255,"POSITION"))
    print("calib comp")

    for id in idx:
        print("id = ",str(id))
        input()
        print (aaa.positionCmd(id,3000,2))
        input()
        print (aaa.positionCmd(id,0,2))
    
    print("enter FREE MODE")
    input()
    print (aaa.setMode(255,"FREE"))
            

