from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QMainWindow,QApplication
from os import path
from sys import argv
from cashier import cashierapp
from checkitem import checkitem

FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"GUI/admin.ui"))

class adminwin(QMainWindow,FORM_CLASS):
	def __init__(self, parent=None):
		super(adminwin,self).__init__(parent)
		self.setupUi(self)
		self.cashier = cashierapp()
		self.checkitem = checkitem()
		self.cashier_bt.clicked.connect(self.cashierwin)
		self.check_bt.clicked.connect(self.checkwin)
	def cashierwin(self):
		self.cashier.show()
	def checkwin(self):
		self.checkitem.show()
if __name__ == "__main__":
	app = QApplication(argv)
	MainWindow = QMainWindow()
	window = adminwin()
	window.show()
	exit(app.exec_())
