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
        self.lc=lcm.LCM()
        self.initUI()
        
    def comentout(self,coment):
        self.coment= str(coment)
        print("result:"+self.coment)
    
    def changeColor3dmouse(self,mode):
        print("mode:"+str(mode))

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

        if source.text()=="button1":
            msg.mode = 0
            self.lc.publish("EXAMPLE",msg.encode())
            self.btn1.setStyleSheet('QPushButton {background-color: #00ff00}')
            self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')

        elif source.text()=="button2": 
            msg.mode = 1
            self.lc.publish("EXAMPLE",msg.encode())
            self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn2.setStyleSheet('QPushButton {background-color: #00ff00}')
            self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')
 
        elif source.text()=="button3": 
            msg.mode = 2
            self.lc.publish("EXAMPLE",msg.encode())
            self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn3.setStyleSheet('QPushButton {background-color: #00ff00}')

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        
        self.btn1 = QPushButton('button1', self)
        self.btn1.setCheckable(True)
        self.btn1.setToolTip("This is an example button")
        self.btn1.resize(120,240)
        self.btn1.move(130,70)
        self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
        self.btn1.clicked.connect(self.on_click)
        self.btn1.clicked.connect(self.changeColor)
    
        self.btn2 = QPushButton('button2', self)
        self.btn2.setCheckable(True)
        self.btn2.setToolTip("This is an example button")
        self.btn2.resize(120,240)
        self.btn2.move(260,70)
        self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
        self.btn2.clicked.connect(self.on_click)
        self.btn2.clicked.connect(self.changeColor)

        self.btn3 = QPushButton('button3', self)
        self.btn3.setCheckable(True)
        self.btn3.setToolTip("This is an example button")
        self.btn3.resize(120,240)
        self.btn3.move(390,70)
        self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')
        self.btn3.clicked.connect(self.on_click)
        self.btn3.clicked.connect(self.changeColor)

        self.show()

        #self.lc = lcm.LCM()
        lcm_handler =  LcmHandler()
        lcm_handler._signal.connect(self.changeColor3dmouse)
        subscription = self.lc.subscribe("EXAMPLE", lcm_handler.my_handler)
        ## kakikae
        thread1 = threading.Thread(target=subscribe_handler, args=(self.lc.handle,))
        thread1.start()



    @pyqtSlot()
    def on_click(self):
        print("PyQt5 button click")


class LcmHandler(QObject):
    _signal = pyqtSignal(int)

    def my_handler(self,channel, data):
        msg = example_t.decode(data)

        print("Received message on channel \"%s\"" % str(channel))
        print("   mode   = %s" % str(msg.mode))
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