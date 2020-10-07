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
        self.stacked_widget.setCurrentIndex(0);
        self.block1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.block2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.block3.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.block4.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.block5.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.block6.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(6))
        self.block7.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(7))
        self.block8.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(8))
        self.block9.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(9))
        self.block10.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(10))
        self.block11.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(11))
        self.block12.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(12))
        self.block13.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(13))
        self.block14.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(14))
        self.block15.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(15))

        self.logout_button = self.findChild(QtWidgets.QPushButton, 'logout_button') # Find the button
        self.logout_button.clicked.connect(self.logout)

        self.logout_button1 = self.findChild(QtWidgets.QPushButton, 'logout_button1') # Find the button
        self.logout_button1.clicked.connect(self.logout)

        self.logout_button2 = self.findChild(QtWidgets.QPushButton, 'logout_button2') # Find the button
        self.logout_button2.clicked.connect(self.logout)

        self.logout_button3 = self.findChild(QtWidgets.QPushButton, 'logout_button3') # Find the button
        self.logout_button3.clicked.connect(self.logout)

        self.logout_button4 = self.findChild(QtWidgets.QPushButton, 'logout_button4') # Find the button
        self.logout_button4.clicked.connect(self.logout)

        self.logout_button5 = self.findChild(QtWidgets.QPushButton, 'logout_button5') # Find the button
        self.logout_button5.clicked.connect(self.logout)

        self.logout_button6 = self.findChild(QtWidgets.QPushButton, 'logout_button6') # Find the button
        self.logout_button6.clicked.connect(self.logout)

        self.logout_button7 = self.findChild(QtWidgets.QPushButton, 'logout_button7') # Find the button
        self.logout_button7.clicked.connect(self.logout)

        self.logout_button8 = self.findChild(QtWidgets.QPushButton, 'logout_button8') # Find the button
        self.logout_button8.clicked.connect(self.logout)

        self.logout_button9 = self.findChild(QtWidgets.QPushButton, 'logout_button9') # Find the button
        self.logout_button9.clicked.connect(self.logout)

        self.logout_button10 = self.findChild(QtWidgets.QPushButton, 'logout_button10') # Find the button
        self.logout_button10.clicked.connect(self.logout)

        self.logout_button11 = self.findChild(QtWidgets.QPushButton, 'logout_button11') # Find the button
        self.logout_button11.clicked.connect(self.logout)

        self.logout_button12 = self.findChild(QtWidgets.QPushButton, 'logout_button12') # Find the button
        self.logout_button12.clicked.connect(self.logout)

        self.logout_button13 = self.findChild(QtWidgets.QPushButton, 'logout_button13') # Find the button
        self.logout_button13.clicked.connect(self.logout)

        self.logout_button14 = self.findChild(QtWidgets.QPushButton, 'logout_button14') # Find the button
        self.logout_button14.clicked.connect(self.logout)

        self.logout_button15 = self.findChild(QtWidgets.QPushButton, 'logout_button15') # Find the button
        self.logout_button15.clicked.connect(self.logout)



        self.heater_button_1 = self.findChild(QtWidgets.QPushButton, 'heater_button_1')
        self.heater_button_1.clicked.connect(self.heater1)

        self.heater_button_2.clicked.connect(self.heater2)
        self.heater_button_2 = self.findChild(QtWidgets.QPushButton, 'heater_button_2')

        self.heater_button_3.clicked.connect(self.heater3)
        self.heater_button_3 = self.findChild(QtWidgets.QPushButton, 'heater_button_3')


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
    
        self.heater_button_1 = self.findChild(QtWidgets.QPushButton, 'heater_button_1')
        self.heater_button_2 = self.findChild(QtWidgets.QPushButton, 'heater_button_2')
        self.heater_button_3 = self.findChild(QtWidgets.QPushButton, 'heater_button_3')


        h_index1 = 0
        h_index2 = 0
        h_index3 = 0
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
        self.block1.setEnabled(True)
        #n_pages = len(self.stacked_widget)
        self.block2.setEnabled(True)
        self.block3.setEnabled(True)

    def heater1(self, h_index1):
        h_index1 = h_index1 + 1;
        if (h_index1 % 2 == 0):
            self.heater_button_1.setText('On')
            self.heater_button_1.setStyleSheet("background-color : green")
        else:
            self.heater_button_1.setText('Off')
            self.heater_button_1.setStyleSheet("background-color : rgb(255,0,0)")

    def heater2(self, h_index2):
        h_index2 = h_index2 + 1;
        if (h_index2 % 2 == 0):
            self.heater_button_2.setText('On')
            self.heater_button_2.setStyleSheet("background-color : green")
        else:
            self.heater_button_2.setText('Off')
            self.heater_button_2.setStyleSheet("background-color : rgb(255,0,0)")

    def heater3(self, h_index3):
        h_index3 = h_index3 + 1;
        if (h_index3 % 2 == 0):
            self.heater_button_3.setText('On')
            self.heater_button_3.setStyleSheet("background-color : green")
        else:
            self.heater_button_3.setText('Off')
            self.heater_button_3.setStyleSheet("background-color : rgb(255,0,0)")                     

    #def insert_page(self, widget, index=-1):
        #self.stacked_widget.insertWidget(index, widget)
        #self.set_button_state(self.stacked_widget.currentIndex())

    def logout(self):
        # This is executed when the button is pressed
        app.exit()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()