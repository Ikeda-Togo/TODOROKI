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
        self.lc=lcm.LCM()
        self.initUI()
        self.showMaximized() 
        
    def comentout(self,coment):
        self.coment= str(coment)
        # print("result:"+self.coment)
    
    def changeColor3dmouse(self,mode):
        # print("mode:"+str(mode))

        if mode==0:
            self.btn1.setStyleSheet('QPushButton {background-color: #00ff00}')
            self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')

        elif mode==1:
            self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn2.setStyleSheet('QPushButton {background-color: #00ff00}')
            self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')
 
        elif mode==2:
            self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn3.setStyleSheet('QPushButton {background-color: #00ff00}')

    def changeColor(self):
        source=self.sender()
        msg=example_t()

        if source.text()=="移動":
            msg.mode = 0
            self.labelA.setText(str(msg.mode)) 
            self.lc.publish("EXAMPLE",msg.encode())
            self.btn1.setStyleSheet('QPushButton {background-color: #00ff00}')
            self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')

        elif source.text()=="リフトアップ": 
            msg.mode = 1
            self.labelA.setText(str(msg.mode)) 
            self.lc.publish("EXAMPLE",msg.encode())
            self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn2.setStyleSheet('QPushButton {background-color: #00ff00}')
            self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')
 
        elif source.text()=="アーム操作": 
            msg.mode = 2
            self.labelA.setText(str(msg.mode)) 
            self.lc.publish("EXAMPLE",msg.encode())
            self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn3.setStyleSheet('QPushButton {background-color: #00ff00}')

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        
        self.btn1 = QPushButton('移動', self)
        self.btn1.setFont(QFont('Arial', 20)) 
        #self.btn1.setCheckable(True)
        self.btn1.setToolTip("This is an example button")
        # self.btn1.resize(120,240)
        self.btn1.resize(240,480)
        self.btn1.move(50,50)
        self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
        self.btn1.clicked.connect(self.on_click)
        self.btn1.clicked.connect(self.changeColor)
    
        self.btn2 = QPushButton('リフトアップ', self)
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


        self.LU_btn1 = QPushButton('Lift UP', self)
        self.LU_btn1.setFont(QFont('Arial', 20)) 
        self.LU_btn1.setToolTip("This is an example button")
        self.LU_btn1.resize(240,120)
        self.LU_btn1.move(800,50)

        self.LU_btn2 = QPushButton('Center', self)
        self.LU_btn2.setFont(QFont('Arial', 20)) 
        self.LU_btn2.setToolTip("This is an example button")
        self.LU_btn2.resize(240,120)
        self.LU_btn2.move(800,170)

        self.LU_btn3 = QPushButton('Lift Down', self)
        self.LU_btn3.setFont(QFont('Arial', 20)) 
        self.LU_btn3.setToolTip("This is an example button")
        self.LU_btn3.resize(240,120)
        self.LU_btn3.move(800,290)

        self.labelA = QLabel(self)
        self.labelA.move(800, 410)      

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
    _signal = pyqtSignal(int)

    def my_handler(self,channel, data):
        msg = example_t.decode(data)

        # print("Received message on channel \"%s\"" % str(channel))
        # print("   mode   = %s" % str(msg.mode))
        self._signal.emit(int(msg.mode))
        #print(msg.name)
        #print("")

def subscribe_handler(handle):
    while True:
        handle()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
