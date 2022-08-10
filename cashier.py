from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QMainWindow,QApplication,QTableWidgetItem
from os import path
from sys import argv
from datamanager import database
from get_item_data import getitemdata

FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"GUI/cashier.ui"))

class mainapp(QMainWindow,FORM_CLASS):
	def __init__(self, parent=None):
		super(mainapp,self).__init__(parent)
		self.setupUi(self)
		self.dataitem = getitemdata()
		self.add_bt.clicked.connect(self.tarek)
		self.dataitem.add_bt.clicked.connect(self.wally)
	def tarek(self):
		self.dataitem.show()
	def wally(self):
		barcode = self.dataitem.barcode_input.text()
		itemdata = getitemdata.getitem(self,barcode=barcode)
		print(itemdata)
		rowPosition = self.cashier_table.rowCount() 
		self.cashier_table.insertRow(rowPosition)
		self.cashier_table.setItem(rowPosition,0,QTableWidgetItem(str(itemdata[0])))
		self.cashier_table.setItem(rowPosition,1,QTableWidgetItem("zioz"))
		self.cashier_table.setItem(rowPosition,2,QTableWidgetItem(str(itemdata[1])))





if __name__ == "__main__":
	app = QApplication(argv)
	MainWindow = QMainWindow()
	window = mainapp()
	window.show()
	exit(app.exec_())


