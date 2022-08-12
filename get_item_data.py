from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QMainWindow, QApplication
from os import path
from sys import argv
from datamanager import database

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "GUI/getitem_data.ui"))


class getitemdata(QMainWindow, FORM_CLASS):
	def __init__(self, parent=None):
		super(getitemdata, self).__init__(parent)
		self.setupUi(self)
		self.cr = database.databaseconnect(self,"DB/database.db")

	def getitem(self,barcode):
		# self.cr = database.databaseconnect(self,"DB/database.db")
		self.cr.execute(f"SELECT * FROM goods WHERE barcode = '{barcode}'")
		dataitem = self.cr.fetchone()
		return dataitem



if __name__ == "__main__":
	app = QApplication(argv)
	MainWindow = QMainWindow()
	window = getitemdata()
	window.show()
	exit(app.exec_())
