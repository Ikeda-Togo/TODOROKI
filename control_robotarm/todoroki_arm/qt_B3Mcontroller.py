#!/usr/bin/python3
# -*- coding: utf-8 -*-

import b3mCtrl
import time
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QComboBox, QMainWindow, QApplication)


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

        self.pos = [0] * 10

        self.aaa = b3mCtrl.B3mClass()
        self.aaa.begin("/dev/ttyUSB0",1500000)
        print (self.aaa.setTrajectoryType(255,"EVEN"))
        print (self.aaa.setMode(255,"POSITION"))
        # self.showMaximized() 

    def initUI(self):      

        btn1_add = QPushButton("+", self)
        btn1_add.move(140, 20)
        
        btn1_sub = QPushButton("-", self)
        btn1_sub.move(140, 80)

        free_btn =QPushButton("FREE_MODE", self)
        free_btn.move(140, 130)

        btn1_add.clicked.connect(self.buttonClicked)            
        btn1_sub.clicked.connect(self.buttonClicked)            
        free_btn.clicked.connect(self.buttonClicked) 

        # ラベル作成、初期の名前をUbuntuにする
        self.lbl = QLabel("Servo id", self)

        # QComboBoxオブジェクトの作成
        combo = QComboBox(self)
        # アイテムの名前設定
        for id in range(0,10):
            combo.addItem(str(id))

        combo.move(30, 20)
        self.lbl.move(30, 80)
        
        self.statusBar()

        # アイテムが選択されたらonActivated関数の呼び出し
        combo.activated[str].connect(self.onActivated)        

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QComboBox')
        self.show()


    def onActivated(self, text):
        self.id = int(text)
        # ラベルに選択されたアイテムの名前を設定
        self.lbl.setText(text)
        # ラベルの長さを調整
        self.lbl.adjustSize()  

   
    def buttonClicked(self):
        # ステータスバーへメッセージの表示
        sender = self.sender()

        if sender.text() == "+":
            self.pos[self.id] += 1000 
            if self.pos[self.id] >=32000:
                self.pos[self.id]=32000
            print (self.aaa.positionCmd(self.id, self.pos[self.id], 1))
        elif sender.text() == "-":
            self.pos[self.id] -= 1000 
            if self.pos[self.id] <=-32000:
                self.pos[self.id]=-32000
            print (self.aaa.positionCmd(self.id, self.pos[self.id], 1))

        if sender.text() == "FREE_MODE":
            print (self.aaa.setMode(255,"FREE"))

        else:
            pass
        self.statusBar().showMessage('id '+ str(self.id) + ' position is ' + str(self.pos[self.id]))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())