import sys
import usb.core
import usb.util
from time import gmtime, strftime
import time
import copy
import threading
#from PyQt5.QtWidgets import QApplication, QWidget,QPushButton,QColorDialog,QDialog,QLabel
#from PyQt5.QtGui import QIcon
#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QObject, pyqtSignal, QThread

class TestWorker1(QThread):
    _signal = pyqtSignal(int)

    def __init__(self):
        super(TestWorker1, self).__init__()

    def run(self):
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

        Mode = 0

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

        R_list = [0,0,0]
        old_R_list = 0

        Button_number = 0

        run=True
        while run:
            try:
                data = dev.read(ep_in.bEndpointAddress, ep_in.bLength, 0)
                if data[0] == 3:
                    if data[1]== 0:
                        print("push button : ", Button_number)
                        if Button_number == 1:
                            if Mode == 2:
                                Mode = 0
                            else:
                                Mode += 1
                            if Mode == 1:
                                RC_flag = 0
                        elif Button_number == 2:
                            if Mode == 0:
                                Mode = 2
                            else:
                                Mode -= 1
                            if Mode == 1:
                                RC_flag = 0
                        elif Button_number == 3:
                            break
                        print("Now Mode:",Mode)
                        self._signal.emit(Mode)

                        Button_number = 0

                    else:
                        Button_number = data[1]

                    '''
                    if data[1]== 0:
                        print("push button : ", Button_number)
                        Button_number = 0
                    else:
                        Button_number = data[1]
                    '''

            except KeyboardInterrupt:
                print("end")
                break
            except usb.core.USBError:
                print("USB error")
                break 
        usb.util.dispose_resources(dev)

        if reattach:
            dev.attach_kernel_driver(0)

class App(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 simple window - pythonspot.com"
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.i = 0
        self.initUI()

    def changeColor3dmouse(mode):
        

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
        print()
        source=self.sender()

        if source.text()=="button1":
            self.btn1.setStyleSheet('QPushButton {background-color: #00ff00}')
            self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')

        elif source.text()=="button2": 
            self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn2.setStyleSheet('QPushButton {background-color: #00ff00}')
            self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')
 
        elif source.text()=="button3": 
            self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
            self.btn3.setStyleSheet('QPushButton {background-color: #00ff00}')
  
    ''' 
    def button(self,title,number):
        self.btn = QPushButton(title, self)
        self.btn.setCheckable(True)
        self.btn.setToolTip("This is an example button")
        self.btn.resize(120,240)
        self.btn.move(130*number,70)
        self.btn.setStyleSheet('QPushButton {background-color: #ff0000}')
        self.btn.clicked.connect(self.on_click)
        self.btn.clicked.connect(self.changeColor)
    '''    

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

        self.yeah = QPushButton('yeah', self)
        self.yeah.setCheckable(True)
        self.yeah.setToolTip("This is an example button")
        self.yeah.resize(120,60)
        self.yeah.move(260,350)
        self.yeah.setStyleSheet('QPushButton {background-color: #AAAAAA}')
        self.yeah.clicked.connect(self.pushbutton1_clicked)
        self.show()

        print(self.i)
        self.pushbutton1_clicked

        if self.i == 1:
            print("Hello")
            self.getdata

        self.i=1
    
    def pushbutton1_clicked(self):
        self.Mode=0
        self.test_worker1 = TestWorker1()
        self.test_worker1._signal.connect(self.changeColor3dmouse)
        self.test_worker1.start()

    def makeWindow(self):
        # サブウィンドウの作成
        subWindow = SubWindow()
        # サブウィンドウの表示
        subWindow.show()

    def getdata(self):
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

        Mode = 0

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

        R_list = [0,0,0]
        old_R_list = 0

        Button_number = 0

        run=True
        while run:
            try:
                data = dev.read(ep_in.bEndpointAddress, ep_in.bLength, 0)
                if data[0] == 3:
                    if data[1]== 0:
                        print("push button : ", Button_number)
                        if Button_number == 1:
                            if Mode == 2:
                                Mode = 0
                            else:
                                Mode += 1
                            if Mode == 1:
                                RC_flag = 0
                        elif Button_number == 2:
                            if Mode == 0:
                                Mode = 2
                            else:
                                Mode -= 1
                            if Mode == 1:
                                RC_flag = 0
                        elif Button_number == 3:
                            break
                        print("Now Mode:",Mode)
                        if Mode == 0:
                            print("hello")
                            self.btn1.setStyleSheet('QPushButton {background-color: #00ff00}')
                            self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
                            self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')
                        elif Mode == 1:
                            self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
                            self.btn2.setStyleSheet('QPushButton {background-color: #00ff00}')
                            self.btn3.setStyleSheet('QPushButton {background-color: #AAAAAA}')
                        elif Mode == 2:
                            self.btn1.setStyleSheet('QPushButton {background-color: #AAAAAA}')
                            self.btn2.setStyleSheet('QPushButton {background-color: #AAAAAA}')
                            self.btn3.setStyleSheet('QPushButton {background-color: #00ff00}')
                        
                        self.show()

                        Button_number = 0

                    else:
                        Button_number = data[1]

                    '''
                    if data[1]== 0:
                        print("push button : ", Button_number)
                        Button_number = 0
                    else:
                        Button_number = data[1]
                    '''

            except KeyboardInterrupt:
                print("end")
                break
            except usb.core.USBError:
                print("USB error")
                break 
        usb.util.dispose_resources(dev)

        if reattach:
            dev.attach_kernel_driver(0)

    @pyqtSlot()
    def on_click(self):
        print("PyQt5 button click")

class SubWindow(QWidget):
    def __init__(self, parent=None):
        # こいつがサブウィンドウの実体？的な。ダイアログ
        self.w = QDialog(parent)
        label = QLabel()
        label.setText('Sub Window')
        layout = QHBoxLayout()
        layout.addWidget(label)
        self.w.setLayout(layout)

    def show(self):
        self.w.exec_()

def Play():
    app = QApplication(sys.argv)
    ex = App()
    print("hello")
    sys.exit(app.exec_())
def Play2():
    print("hello world")
    App.getdata

    
if __name__ == "__main__":
    th1 =threading.Thread(target=Play)
    th1.start()