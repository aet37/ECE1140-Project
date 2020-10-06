import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QStackedWidget
import sys


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('C:/Users/Evan/OneDrive/Documents/Github/ECE1140-Project/src/TrackModel/Map_Page.ui', self)
        self.initUI()
        self.stacked_widget.currentChanged.connect(self.set_button_state)
        self.block1.clicked.connect(self.page1)
        self.block2.clicked.connect(self.page2)
        self.block3.clicked.connect(self.page3)
        self.block4.clicked.connect(self.page4)
        self.block5.clicked.connect(self.page5)
        self.block6.clicked.connect(self.page6)
        self.block7.clicked.connect(self.page7)
        self.block8.clicked.connect(self.page8)
        self.block9.clicked.connect(self.page9)
        self.block10.clicked.connect(self.page10)
        self.block11.clicked.connect(self.page11)
        self.block12.clicked.connect(self.page12)
        self.block13.clicked.connect(self.page13)
        self.block14.clicked.connect(self.page14)
        self.block15.clicked.connect(self.page15)

        #self.submit_in = self.findChild(QtWidgets.QPushButton, 'submit_in') # Find the button
        #self.button = self.findChild(QtWidgets.QPushButton, 'train_button_1') # Find the button
        #self.button.clicked.connect(self.train1)
        #self.button = self.findChild(QtWidgets.QPushButton, 'train_button_2') # Find the button
        #self.button.clicked.connect(self.train2)
        #self.button = self.findChild(QtWidgets.QPushButton, 'train_button_3') # Find the button
        #self.button.clicked.connect(self.train3)
        #self.button = self.findChild(QtWidgets.QPushButton, 'train_button_4') # Find the button
        #self.button.clicked.connect(self.train4)

        self.logout_button = self.findChild(QtWidgets.QPushButton, 'logout_button') # Find the button
        self.logout_button.clicked.connect(self.logout)

        self.show()

    def initUI(self):
        self.block1 = self.findChild(QtWidgets.QPushButton, 'pushButton_1')
        self.block2 = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.block3 = self.findChild(QtWidgets.QPushButton, 'pushButton_3')
        self.block4 = self.findChild(QtWidgets.QPushButton, 'pushButton_4')
        self.block5 = self.findChild(QtWidgets.QPushButton, 'pushButton_5')
        self.block6 = self.findChild(QtWidgets.QPushButton, 'pushButton_6')
        self.block7 = self.findChild(QtWidgets.QPushButton, 'pushButton_7')
        self.block8 = self.findChild(QtWidgets.QPushButton, 'pushButton_8')
        self.block9 = self.findChild(QtWidgets.QPushButton, 'pushButton_9')
        self.block10 = self.findChild(QtWidgets.QPushButton, 'pushButton_10')
        self.block11 = self.findChild(QtWidgets.QPushButton, 'pushButton_11')
        self.block12 = self.findChild(QtWidgets.QPushButton, 'pushButton_12')
        self.block13 = self.findChild(QtWidgets.QPushButton, 'pushButton_13')
        self.block14 = self.findChild(QtWidgets.QPushButton, 'pushButton_14')
        self.block15 = self.findChild(QtWidgets.QPushButton, 'pushButton_15')
        self.stacked_widget = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget')
    
    def page0(self):
        #new_index = self.stacked_widget.currentIndex()-1
        #if new_index >= 0:
        self.stacked_widget.setCurrentIndex(0)

    def page1(self):
        #new_index = self.stacked_widget.currentIndex()+1
        #if new_index < len(self.stacked_widget):
        self.stacked_widget.setCurrentIndex(1)

    def page2(self):
        self.stacked_widget.setCurrentIndex(2)

    def page3(self):
        self.stacked_widget.setCurrentIndex(3)

    def page4(self):
        self.stacked_widget.setCurrentIndex(4)

    def page5(self):
        self.stacked_widget.setCurrentIndex(5)

    def page6(self):
        self.stacked_widget.setCurrentIndex(6)

    def page7(self):
        self.stacked_widget.setCurrentIndex(7)

    def page8(self):
        self.stacked_widget.setCurrentIndex(8)

    def page9(self):
        self.stacked_widget.setCurrentIndex(9)

    def page10(self):
        self.stacked_widget.setCurrentIndex(10)

    def page11(self):
        self.stacked_widget.setCurrentIndex(11) 

    def page12(self):
        self.stacked_widget.setCurrentIndex(12)

    def page13(self):
        self.stacked_widget.setCurrentIndex(13)                                       

    def page14(self):
        self.stacked_widget.setCurrentIndex(14)

    def page15(self):
        self.stacked_widget.setCurrentIndex(15)

    def set_button_state(self, index):
        self.block1.setEnabled(index > 0)
        n_pages = len(self.stacked_widget)
        self.block2.setEnabled( index % n_pages < n_pages - 1)

    #def insert_page(self, widget, index=-1):
        #self.stacked_widget.insertWidget(index, widget)
        #self.set_button_state(self.stacked_widget.currentIndex())

    def logout(self):
        # This is executed when the button is pressed
        app.exit()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()