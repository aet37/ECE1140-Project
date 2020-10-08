
import os
from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
#import Request.hpp


# GLOBALS

sw1val = 0
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('C:/Users/natta/AppData/Local/Programs/Python/Python38-32/Scripts/SW_Track_Controller_UI.ui', self)
  
     
        self.button = self.findChild(QtWidgets.QPushButton, 'switch1_button') # Find the button
        self.button.clicked.connect(self.switch1)
        
        self.table=self.findChild(QtWidgets.QTableWidget, 'switch_table')

        self.label = self.findChild(QtWidgets.QLabel, 'switch1_label')

       
       # self.button2 = self.findChild(QtWidgets.QPushButton, 'logout_button') # Find the button
       # self.button2.clicked.connect(self.logout)

        self.show()
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        asd = QTableWidgetItem()
        asdf = QTableWidgetItem()
        asdfg = QTableWidgetItem()

        asd.setText("In-Block")
        
        self.table.setRowCount(10)
        self.table.setColumnCount(3)
        asd.setText("Switch")
        self.table.setHorizontalHeaderItem(0,asd)
        asdf.setText("In-Block")
        self.table.setHorizontalHeaderItem(1,asdf)
        asdfg.setText("Out-Block")
        self.table.setHorizontalHeaderItem(2,asdfg)
      

      
        self.table.setItem(0, 0, asd)
       

    
    

    def switch1(self):

        #send signal to server to switch switch 1


        #garbage
        global sw1val
        
        if(sw1val==1):
            
            # This is executed when the button is pressed
           self.switch1_label.setText("0")
           sw1val = 0

        if(sw1val==0):
            self.switch1_label.setText("1")
            sw1val = 1



            
   #
   # def logout(self):
   #     # This is executed when the button is pressed
   #     app.exit()

  
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()