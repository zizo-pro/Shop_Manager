from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QMainWindow,QApplication,QTableWidgetItem,QMessageBox
from os import path
from sys import argv
from datamanager import database
from additem import additem
from msgboxes import msgbox

FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"GUI/storage.ui"))


class storagewin(QMainWindow, FORM_CLASS):
	def __init__(self, parent=None):
		super(storagewin, self).__init__(parent)
		self.setupUi(self)
		self.cr = database()
		self.buttonman()
		self.filltable()
		self.addwin = additem()
		self.msbox = msgbox()
		self.editeditems = []

	def buttonman(self):
		self.storage_table.itemChanged.connect(self.updatedb)
		self.search_bt.clicked.connect(self.search)
		self.reset_table_bt.clicked.connect(self.filltable)
		self.save_bt.clicked.connect(self.save)
		self.additem_bt.clicked.connect(self.addwind)

	def filltable(self):
		self.storage_table.setRowCount(0)
		items = self.cr.executeall("SELECT * FROM goods")
		for item in range(len(items)):
			self.storage_table.insertRow(item)
			self.storage_table.setItem(item,0,QTableWidgetItem(items[item][0]))
			self.storage_table.setItem(item,1,QTableWidgetItem(str(items[item][1])))
			self.storage_table.setItem(item,2,QTableWidgetItem(str(items[item][2])))
			self.storage_table.setItem(item,3,QTableWidgetItem(str(items[item][3])))
	def search(self):
		itembarcode = self.barcode_search.text()
		itemdata = self.cr.itemdatawithbarcode(itembarcode)
		self.storage_table.setRowCount(0)
		self.storage_table.insertRow(0)
		self.storage_table.setItem(0,0,QTableWidgetItem(itemdata[0]))
		self.storage_table.setItem(0,1,QTableWidgetItem(str(itemdata[1])))
		self.storage_table.setItem(0,2,QTableWidgetItem(str(itemdata[2])))
		self.storage_table.setItem(0, 3, QTableWidgetItem(str(itemdata[3])))
	def addwind(self):
		self.addwin.show()

	def updatedb(self,item):
		try:
			itembarcode = self.storage_table.item(int(item.row()),3)
			if item.column() == 0:
				self.editeditems.append(f"UPDATE goods SET item = '{item.text()}' WHERE barcode = '{str(itembarcode.text())}'")
			
			elif item.column() == 1:
				self.editeditems.append(f"UPDATE goods SET price = '{item.text()}' WHERE barcode = '{str(itembarcode.text())}'")
			
			elif item.column() == 2:
				self.editeditems.append(f"UPDATE goods SET amount = '{item.text()}' WHERE barcode = '{str(itembarcode.text())}'")
			
			elif item.column() == 3:
				itembarcode = self.storage_table.item(int(item.row()),0)
				self.editeditems.append(f"UPDATE goods SET barcode = '{item.text()}' WHERE item = '{str(itembarcode.text())}'")
		except:
			pass

	def save(self):
		def yup():
			for i in self.editeditems:
				self.cr.execut(i)
			self.cr.commit()
		msg = self.msbox.infomessagebox("Are You Sure That You Want To Update The Database")
		yesbtn = msg.addButton("Yes",QMessageBox.YesRole)
		nobtn = msg.addButton("No",QMessageBox.NoRole)
		yesbtn.clicked.connect(yup)
		retval = msg.exec_()



if __name__ == "__main__":
	app = QApplication(argv)
	MainWindow = QMainWindow()
	window = storagewin()
	window.show()
	exit(app.exec_())
