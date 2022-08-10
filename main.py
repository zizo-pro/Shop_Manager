from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QMainWindow,QApplication
from os import path
from sys import argv
from datamanager import database

FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"GUI/login.ui"))

class mainapp(QMainWindow,FORM_CLASS):
	def __init__(self, parent=None):
		super(mainapp,self).__init__(parent)
		self.setupUi(self)
		self.cr = database.databaseconnect(self,"DB/database.db")

		self.login_bt.clicked.connect(self.login)

	def login(self):
		username = self.username_input.text()
		password = self.password_input.text()
		self.cr.execute("SELECT * FROM users")
		data = self.cr.fetchall()
		for i in data:
			if username == str(i[1]) and password == str(i[2]):
				windowid = str(i[0])
				break
		else:
			print("nope thats not you")


if __name__ == "__main__":
	app = QApplication(argv)
	MainWindow = QMainWindow()
	window = mainapp()
	window.show()
	exit(app.exec_())
