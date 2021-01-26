# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

import threading
import lcm
from exlcm import example_t

#####################################  LCM      #########################################################

######publishされたら動く############
def my_handler(channel, data):
    global msg
    msg = example_t.decode(data)
    msg.R_list=list(msg.R_list)
    
def subscribe_handler(handle):
    while True:
        handle()

msg =  example_t()
lc = lcm.LCM()
subscription = lc.subscribe("EXAMPLE", my_handler)

########handleをwhileでぶん回すのをサブスレッドで行う############
thread1 = threading.Thread(target=subscribe_handler, args=(lc.handle,))
thread1.setDaemon(True)
thread1.start()

###########################################################################################################

(w,h) = (400,400)   # 画面サイズ
(x,y) = (w/2, h/2)
pygame.init()       # pygame初期化
pygame.display.set_mode((w, h), 0, 32)  # 画面設定
screen = pygame.display.get_surface()

key_flag = 0

while (1):
    # キーイベント処理(キャラクタ画像の移動)

    pressed_key = pygame.key.get_pressed()
    if pressed_key[K_LEFT]:
        msg.R_list[2]=-1
        key_flag = 0
        lc.publish("EXAMPLE",msg.encode())

        # x-=1
    elif pressed_key[K_RIGHT]:
        msg.R_list[2]=1
        key_flag = 0
        lc.publish("EXAMPLE",msg.encode())
        # x+=1
    elif pressed_key[K_UP]:
        msg.R_list[0]=1
        key_flag = 0
        lc.publish("EXAMPLE",msg.encode())
        # y-=1
    elif pressed_key[K_DOWN]:
        msg.R_list[0]=-1
        key_flag = 0
        lc.publish("EXAMPLE",msg.encode())
        # y+=1
    elif key_flag == 0 :
        msg.R_list[0],msg.R_list[1],msg.R_list[2]= 0, 0, 0
        key_flag = 1
        lc.publish("EXAMPLE",msg.encode())
    else :
        pass

    # pygame.display.update()     # 画面更新
    # pygame.time.wait(30)        # 更新時間間隔
    # screen.fill((0, 20, 0, 0))  # 画面の背景色
    # # 円を描画
    # pygame.draw.circle(screen, (0, 200, 0), (int(x), int(y)), 5)
    # イベント処理
    for event in pygame.event.get():
        # 画面の閉じるボタンを押したとき
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # キーを押したとき
        if event.type == KEYDOWN:
            # ESCキーなら終了
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
