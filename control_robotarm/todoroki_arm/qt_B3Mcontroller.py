#!/usr/bin/python3
# -*- coding: utf-8 -*-

import b3mCtrl
import time
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel


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

        self.lbl = QLabel(self)
        self.lbl.move(30, 60)

        self.inputText = QLineEdit(self)
        self.inputText.move(30, 20)
        self.inputText.textChanged[str].connect(self.onChanged)
        free_btn =QPushButton("FREE_MODE", self)
        free_btn.move(30, 80)


        # クリックされたらbuttonClickedの呼び出し
        btn1_add.clicked.connect(self.buttonClicked)            
        btn1_sub.clicked.connect(self.buttonClicked)            
        free_btn.clicked.connect(self.buttonClicked)            
        # btn2.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(300, 400, 290, 150)
        self.setWindowTitle('Event sender')
        self.show()

    def output(self):
        self.statusBar().showMessage(self.inputText.text())

    def onChanged(self, text):
        print(str(text))
        if text

        self.id = int(text)
        self.pos[self.id]=0
        # ラベルに入力されたテキストを挿入
        self.lbl.setText(text)
        # 入力されたテキストによって、ラベルの長さを調整
        self.lbl.adjustSize() 

    def buttonClicked(self):

        # ステータスバーへメッセージの表示
        sender = self.sender()

        # if sender.text() != "+" and sender.text() != "-":
        #     self.now_id = sender.text()
        #     time.sleep(0.01)

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
