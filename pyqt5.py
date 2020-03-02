import sys
#from PyQt5.QtWidgets import QApplication, QWidget,QPushButton,QColorDialog,QDialog,QLabel
#from PyQt5.QtGui import QIcon
#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "PyQt5 simple window - pythonspot.com"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def changeColor(self):
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
        self.yeah.clicked.connect(self.makeWindow)
        self.show()
   

    def makeWindow(self):
        # サブウィンドウの作成
        subWindow = SubWindow()
        # サブウィンドウの表示
        subWindow.show()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
