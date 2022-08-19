from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox
from os import path
from sys import argv
from datamanager import database
from additem import additem
from msgboxes import msgbox

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "GUI/staff.ui"))


class staffwin(QMainWindow, FORM_CLASS):
	def __init__(self, parent=None):
		super(staffwin, self).__init__(parent)
		self.setupUi(self)
		self.cr = database()
		# self.buttonman()
		self.filltable()
		self.addwin = additem()
		self.msbox = msgbox()
		self.editeditems = []
		self.buttonman()

	def buttonman(self):
		self.search_bt.clicked.connect(self.search)
		self.reset_table_bt.clicked.connect(self.filltable)
		self.save_bt.clicked.connect(self.save)
		self.staff_table.itemChanged.connect(self.updatedb)

	def filltable(self):
		self.staff_table.setRowCount(0)
		items = self.cr.executeall("SELECT * FROM staff")
		for item in range(len(items)):
			self.staff_table.insertRow(item)
			self.staff_table.setItem(item, 0, QTableWidgetItem(items[item][1]))
			self.staff_table.setItem(item, 1, QTableWidgetItem(str(items[item][2])))
			self.staff_table.setItem(item, 2, QTableWidgetItem(str(items[item][3])))
			self.staff_table.setItem(item, 3, QTableWidgetItem(str(items[item][4])))
			self.staff_table.setItem(item, 4, QTableWidgetItem(str(items[item][5])))
			self.staff_table.setItem(item, 5, QTableWidgetItem(str(items[item][6])))

	def search(self):
		workername = self.worker_search.text()
		itemdata = self.cr.executeone(f"SELECT * FROM staff WHERE name = '{workername}'")
		self.staff_table.setRowCount(0)
		self.staff_table.insertRow(0)
		self.staff_table.setItem(0, 0, QTableWidgetItem(itemdata[1]))
		self.staff_table.setItem(0, 1, QTableWidgetItem(str(itemdata[2])))
		self.staff_table.setItem(0, 2, QTableWidgetItem(str(itemdata[3])))
		self.staff_table.setItem(0, 3, QTableWidgetItem(str(itemdata[4])))
		self.staff_table.setItem(0, 4, QTableWidgetItem(str(itemdata[5])))
		self.staff_table.setItem(0, 5, QTableWidgetItem(str(itemdata[6])))
	def addwind(self):
		self.addwin.show()

	def updatedb(self, item):
		try:
			itembarcode = self.staff_table.item(int(item.row()), 1)
			if item.column() == 0:
				self.editeditems.append(
					f"UPDATE staff SET name = '{item.text()}' WHERE phone = '{str(itembarcode.text())}'")

			elif item.column() == 1:
				itembarcode = self.staff_table.item(int(item.row()), 0)
				self.editeditems.append(
					f"UPDATE staff SET phone = '{item.text()}' WHERE name = '{str(itembarcode.text())}'")

			elif item.column() == 2:
				self.editeditems.append(
					f"UPDATE staff SET address = '{item.text()}' WHERE phone = '{str(itembarcode.text())}'")

			elif item.column() == 3:
				self.editeditems.append(
					f"UPDATE staff SET job = '{item.text()}' WHERE phone = '{str(itembarcode.text())}'")
			elif item.column() == 4:
				self.editeditems.append(
					f"UPDATE staff SET salary = '{item.text()}' WHERE phone = '{str(itembarcode.text())}'")
			elif item.column() == 5:
				self.editeditems.append(
					f"UPDATE staff SET birth_date = '{item.text()}' WHERE phone = '{str(itembarcode.text())}'")
		except:
			pass

	def save(self):
		def yup():
			for i in self.editeditems:
				self.cr.execut(i)
			self.cr.commit()
		msg = self.msbox.infomessagebox(
			"Are You Sure That You Want To Update The Database")
		yesbtn = msg.addButton("Yes", QMessageBox.YesRole)
		nobtn = msg.addButton("No", QMessageBox.NoRole)
		yesbtn.clicked.connect(yup)
		retval = msg.exec_()


if __name__ == "__main__":
	app = QApplication(argv)
	MainWindow = QMainWindow()
	window = staffwin()
	window.show()
	exit(app.exec_())
