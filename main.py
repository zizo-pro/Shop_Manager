from ast import main
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMainWindow,QApplication
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
from os import path
from sys import argv
from sqlite3 import connect

FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"GUI/login.ui"))

class mainapp(QMainWindow,FORM_CLASS):
	def __init__(self, parent=None):
		super(mainapp,self).__init__(parent)
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.databaseMan()

		self.login_bt.clicked.connect(self.login)
	
	def databaseMan(self):
		self.db = connect("DB/database.db")
		self.cr = self.db.cursor()
	
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
