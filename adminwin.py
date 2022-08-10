from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QMainWindow,QApplication
from os import path
from sys import argv

FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"GUI/admin.ui"))

class adminwin(QMainWindow,FORM_CLASS):
	def __init__(self, parent=None):
		super(adminwin,self).__init__(parent)
		self.setupUi(self)
		self.admin_bt.clicked.connect(self.button)
	def button(self):
		self.admin_bt.setStyleSheet("background-color: grey")


if __name__ == "__main__":
	app = QApplication(argv)
	MainWindow = QMainWindow()
	window = adminwin()
	window.show()
	exit(app.exec_())
