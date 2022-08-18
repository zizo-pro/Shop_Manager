from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QMainWindow,QApplication
from os import path
from sys import argv
from datamanager import database


FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"GUI/additem.ui"))

class additem(QMainWindow, FORM_CLASS):
	def __init__(self, parent=None):
		super(additem, self).__init__(parent)
		self.setupUi(self)
		self.cr = database()
		self.add_bt.clicked.connect(self.add)

	def add(self):
		item = self.item_input.text()
		price = self.price_input.text()
		amount = self.amount_input.text()
		barcode = self.barcode_input.text()
		self.cr.execut(f"INSERT INTO goods VALUES ('{item}','{price}','{amount}','{barcode}')")
		self.item_input.setText("")
		self.price_input.setText("")
		self.amount_input.setText("")
		self.barcode_input.setText("")


if __name__ == "__main__":
	app = QApplication(argv)
	MainWindow = QMainWindow()
	window = additem()
	window.show()
	exit(app.exec_())
