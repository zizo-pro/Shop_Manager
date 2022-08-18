from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QMainWindow,QApplication
from os import path
from sys import argv
from datamanager import database
from cashier import cashierapp
from adminwin import adminwin
from checkitem import checkitem
from storage import storagewin
FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"GUI/login.ui"))

class mainapp(QMainWindow,FORM_CLASS):
	def __init__(self, parent=None):
		super(mainapp,self).__init__(parent)
		self.cr = database.databaseconnect(self,"DB/database.db")
		self.setupUi(self)
		self.login_bt.clicked.connect(self.login)
		self.users = {
			"1111" : adminwin(),
			"1112" : cashierapp(),
			"1113" : checkitem(),
			"1114" : storagewin(),
		}

	def login(self):
		username = self.username_input.text()
		password = self.password_input.text()
		self.cr.execute("SELECT * FROM users")
		data = self.cr.fetchall()
		windowid = ""
		for i in data:
			if username == str(i[1]) and password == str(i[2]):
				windowid = str(i[0])
				break
		else:
			print("nope thats not you")
		if windowid !="":
			windowtoopen = self.users.get(windowid)
			windowtoopen.show()

if __name__ == "__main__":
	app = QApplication(argv)
	MainWindow = QMainWindow()
	window = mainapp()
	window.show()
	exit(app.exec_())
