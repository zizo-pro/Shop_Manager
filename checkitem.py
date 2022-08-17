from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import  QMainWindow, QApplication
from os import path
from sys import argv
from datamanager import database
from get_item_data import getitemdata
from msgboxes import msgbox

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "GUI/check.ui"))


class cashierapp(QMainWindow, FORM_CLASS):
	def __init__(self, parent=None):
		super(cashierapp, self).__init__(parent)
		self.setupUi(self)
		self.dataitem = getitemdata()
		self.msgbox = msgbox()
		self.cr = database
		self.check_bt.clicked.connect(self.checkitems)
	
	def checkitems(self):
		barcodeit = self.code_input.text()
		dataofitem = self.cr.itemdatawithbarcode(self,barcodeit)
		self.msgbox.infomessagebox(f"Item: {dataofitem[0]}\nPrice: {dataofitem[1]}").exec_()
		self.code_input.setText("")

if __name__ == "__main__":
	app = QApplication(argv)
	MainWindow = QMainWindow()
	window = cashierapp()
	window.show()
	exit(app.exec_())
