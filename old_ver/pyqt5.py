import sys
#from PyQt5.QtWidgets import QApplication, QWidget,QPushButton,QColorDialog,QDialog,QLabel
#from PyQt5.QtGui import QIcon
#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QObject, pyqtSignal, QThread

import threading
import lcm
from exlcm import example_t


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "PyQt5 simple window - pythonspot.com"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.msg = example_t()
        self.msg.mode = 0
        self.msg.LU_mode = 0
        self.lc=lcm.LCM()
        self.initUI()
        self.showMaximized() 
        
    def comentout(self,coment):
        self.coment= str(coment)
        # print("result:"+self.coment)
    
    ###############------------3Dマウスの値をうけてボタンの色を変化させる-----------############
    def changeColor3dmouse(self,data):
        # print("mode:"+str(mode))
        self.msg = example_t.decode(data)
        # self.labelA.setText(str(self.msg.mode)) 
        print(str(self.msg.LU_mode))
        if self.msg.mode==0:
            self.btn1.setStyleSheet('QPushButton {background-color: #00ff00}')
            self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')

        elif self.msg.mode==0:
            self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn2.setStyleSheet('QPushButton {background-color: #00ff00}')
            self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')
 
        elif self.msg.mode==2:
            self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn3.setStyleSheet('QPushButton {background-color: #00ff00}')

        if self.msg.LU_mode ==2:
            self.LU_btn1.setStyleSheet('QPushButton {background-color: #0000FF}')
            self.LU_btn2.setStyleSheet('QPushButton {background-color: #fff}')
            self.LU_btn3.setStyleSheet('QPushButton {background-color: #fff}')

        elif self.msg.LU_mode ==1:
            self.LU_btn1.setStyleSheet('QPushButton {background-color: #fff}')
            self.LU_btn2.setStyleSheet('QPushButton {background-color: #0000ff}')
            self.LU_btn3.setStyleSheet('QPushButton {background-color: #fff}')
 
        elif self.msg.LU_mode ==0:
            self.LU_btn1.setStyleSheet('QPushButton {background-color: #fff}')
            self.LU_btn2.setStyleSheet('QPushButton {background-color: #fff}')
            self.LU_btn3.setStyleSheet('QPushButton {background-color: #0000ff}')

#################--------タッチパネルでの操作で色が変化する------###################
    def changeColor(self):
        source=self.sender()
        #msg=example_t()

        if source.text()=="移動":
            self.msg.mode = 0
            # self.labelA.setText(str(self.msg.mode)) 
            self.btn1.setStyleSheet('QPushButton {background-color: #00ff00}')
            self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')

        elif source.text()=="リフトアップ＆": 
            self.msg.mode = 1
            # self.labelA.setText(str(self.msg.mode)) 
            self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn2.setStyleSheet('QPushButton {background-color: #00ff00}')
            self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')
 
        elif source.text()=="アーム操作": 
            self.msg.mode = 2
            # self.labelA.setText(str(self.msg.mode)) 
            self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn3.setStyleSheet('QPushButton {background-color: #00ff00}')

        #############---------リフトアップチェンジカラー------------#######################
        if source.text()=="Lift UP":
            self.msg.LU_mode = 2
            self.msg.mode = 1
            # self.lc.publish("EXAMPLE",self.msg.encode())
            self.LU_btn1.setStyleSheet('QPushButton {background-color: #0000FF}')
            self.LU_btn2.setStyleSheet('QPushButton {background-color: #fff}')
            self.LU_btn3.setStyleSheet('QPushButton {background-color: #fff}')

        elif source.text()=="Center": 
            self.msg.LU_mode = 1
            self.msg.mode =1
            # self.lc.publish("EXAMPLE",self.msg.encode())
            self.LU_btn1.setStyleSheet('QPushButton {background-color: #fff}')
            self.LU_btn2.setStyleSheet('QPushButton {background-color: #0000ff}')
            self.LU_btn3.setStyleSheet('QPushButton {background-color: #fff}')
 
        elif source.text()=="Lift Down": 
            self.msg.LU_mode = 0
            self.msg.mode =1
            # self.lc.publish("EXAMPLE",self.msg.encode())
            self.LU_btn1.setStyleSheet('QPushButton {background-color: #fff}')
            self.LU_btn2.setStyleSheet('QPushButton {background-color: #fff}')
            self.LU_btn3.setStyleSheet('QPushButton {background-color: #0000ff}')


        self.lc.publish("EXAMPLE",self.msg.encode())
        # self.labelA.setText(str(self.msg.mode)) 

###################--------ボタンや配置の初期化-----------#####################
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        
        self.btn1 = QPushButton('移動', self)
        self.btn1.setFont(QFont('Arial', 20)) 
        #self.btn1.setCheckable(True)
        self.btn1.setToolTip("This is an example button")
        self.btn1.resize(240,480)
        self.btn1.move(50,50)
        self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
        self.btn1.clicked.connect(self.on_click)
        self.btn1.clicked.connect(self.changeColor)
    
        self.btn2 = QPushButton('リフトアップ＆', self)
        self.btn2.setFont(QFont('Arial', 20)) 
        #self.btn2.setCheckable(True)
        self.btn2.setToolTip("This is an example button")
        self.btn2.resize(240,480)
        self.btn2.move(300,50)
        self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
        self.btn2.clicked.connect(self.on_click)
        self.btn2.clicked.connect(self.changeColor)

        self.btn3 = QPushButton('アーム操作', self)
        self.btn3.setFont(QFont('Arial', 20)) 
        #self.btn3.setCheckable(True)
        self.btn3.setToolTip("This is an example button")
        self.btn3.resize(240,480)
        self.btn3.move(550,50)
        self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')
        self.btn3.clicked.connect(self.on_click)
        self.btn3.clicked.connect(self.changeColor)

        ################-----リフトアップボタン-----##############################
        self.LU_btn1 = QPushButton('Lift UP', self)
        self.LU_btn1.setFont(QFont('Arial', 20)) 
        self.LU_btn1.setToolTip("This is an example button")
        self.LU_btn1.resize(240,120)
        self.LU_btn1.move(800,50)
        self.LU_btn1.clicked.connect(self.changeColor)

        self.LU_btn2 = QPushButton('Center', self)
        self.LU_btn2.setFont(QFont('Arial', 20)) 
        self.LU_btn2.setToolTip("This is an example button")
        self.LU_btn2.resize(240,120)
        self.LU_btn2.move(800,170)
        self.LU_btn2.clicked.connect(self.changeColor)

        self.LU_btn3 = QPushButton('Lift Down', self)
        self.LU_btn3.setFont(QFont('Arial', 20)) 
        self.LU_btn3.setToolTip("This is an example button")
        self.LU_btn3.resize(240,120)
        self.LU_btn3.move(800,290)
        self.LU_btn3.clicked.connect(self.changeColor)

        self.labelA = QLabel("リモートセンタ",self)
        self.labelA.move(325,320)
        self.labelA.setFont(QFont('Arial', 20)) 
        self.labelA.adjustSize()  


        self.show()


        #self.lc = lcm.LCM()
        lcm_handler =  LcmHandler()
        lcm_handler._signal.connect(self.changeColor3dmouse)  
        subscription = self.lc.subscribe("EXAMPLE", lcm_handler.my_handler)
        ## kakikae
        thread1 = threading.Thread(target=subscribe_handler, args=(self.lc.handle,))
        thread1.setDaemon(True)
        thread1.start()
        self.lc.publish("EXAMPLE",self.msg.encode())



    @pyqtSlot()
    def on_click(self):
        pass
        # print("PyQt5 button click")


class LcmHandler(QObject):
    _signal = pyqtSignal(bytes)

    def my_handler(self,channel, data):
        msg = example_t.decode(data)
        # print("Received message on channel \"%s\"" % str(channel))
        self._signal.emit(bytes(data))

def subscribe_handler(handle):
    while True:
        handle()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
