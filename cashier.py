from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QWidget,QVBoxLayout,QMainWindow,QApplication,QTableWidgetItem,QMessageBox
from PySide2.QtCore import Qt 
from os import path
from sys import argv
from datamanager import database
from get_item_data import getitemdata
from serchable_combobox import ExtendedComboBox

FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"GUI/cashier.ui"))

class cashierapp(QMainWindow,FORM_CLASS):
	def __init__(self, parent=None):
		super(cashierapp,self).__init__(parent)
		self.setupUi(self)
		self.curr_purchase = []
		self.cr = database
		self.dataitem = getitemdata()
		self.combobox = ExtendedComboBox(self)
		self.buttonman()
		self.comboboxsetup()

	def buttonman(self):
		self.add_bt.clicked.connect(self.addtotable)
		self.cashier_table.itemChanged.connect(self.change)
		self.check_bt.clicked.connect(self.check)
		self.confirm_bt.clicked.connect(self.confirm)
	
	def comboboxsetup(self):
		self.combobox.setGeometry(20,60,170,24)
		stringlis = self.cr.getallitemsname(self)
		stringlist = []
		for i in stringlis:
			stringlist.append(i[0])
		self.combobox.addItems(stringlist)
		self.combobox.setCurrentText("")

	def addtotable(self):
		if self.barcode_input.text() == "":
			barcode = self.combobox.currentText()
			itemdata = self.cr.itemdatawithname(self,barcode)
		else:
			barcode = self.barcode_input.text()
			itemdata = self.cr.itemdatawithbarcode(self, barcode=barcode)
		rowPosition = self.cashier_table.rowCount()
		curr_totalpric = self.totalprice_lb.text()
		ss = curr_totalpric.find("$")
		curr_totalprice = curr_totalpric[:ss]
		if itemdata[0] in self.curr_purchase:
			indx = self.curr_purchase.index(str(itemdata[0]))
			count = self.cashier_table.item(int(indx),1)
			total_price = self.cashier_table.item(int(indx),3)
			try :
				self.cashier_table.setItem(int(indx),1,QTableWidgetItem(str(int(count.text())+1)))
				self.cashier_table.setItem(int(indx),3,QTableWidgetItem(str(int(total_price.text())+int(itemdata[1]))))
			except RuntimeError:
				pass
		else:
			self.cashier_table.insertRow(rowPosition)
			self.cashier_table.setItem(rowPosition,0,self.createitem(str(itemdata[0])))
			self.cashier_table.setItem(rowPosition,1,QTableWidgetItem(str(1)))
			self.cashier_table.setItem(rowPosition,2,self.createitem(str(itemdata[1])))
			self.cashier_table.setItem(rowPosition, 3, self.createitem(str(itemdata[1])))
			self.curr_purchase.append(str(itemdata[0]))
		self.totalprice_lb.setText(f"{int(curr_totalprice)+int(itemdata[1])}$")
		self.barcode_input.setText("")
		self.combobox.setCurrentText("")

	def createitem(self,var):
		item = QTableWidgetItem()
		item.setText(str(var))
		item.setFlags(Qt.ItemIsEnabled)
		return item
	def change(self , item):
		if str(item.column()) == "1":
			prc = self.cashier_table.item(int(item.row()),2)
			tprc = self.cashier_table.item(int(item.row()),3)
			curr_totalpric = self.totalprice_lb.text()
			ss = curr_totalpric.find("$")
			if prc ==None:
				pass
			else:
				new_ttpc = int(prc.text())*int(item.text())
				if int(new_ttpc) > 0:
					currtprc = int(curr_totalpric[:ss]) - int(tprc.text())
					self.totalprice_lb.setText(f"{int(new_ttpc) + int(currtprc)}$")
					self.cashier_table.setItem(int(item.row()),3,QTableWidgetItem(str(new_ttpc)))
				elif int(new_ttpc) == 0:
					self.curr_purchase.pop(int(item.row()))
					self.totalprice_lb.setText(f"{int(curr_totalpric[:ss]) - int(tprc.text())}$")
					self.cashier_table.removeRow(int(item.row()))

	def check(self):
		if self.barcode_input.text() == "":
			brcode = self.combobox.currentText()
			dataofitem = self.cr.itemdatawithname(self,brcode)
		else:
			brcode = self.barcode_input.text()
			dataofitem = self.cr.itemdatawithbarcode(self,brcode)
		msg= QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText(f"Item: {dataofitem[0]}\nPrice: {dataofitem[1]}")
		addbtn = msg.addButton("Add",QMessageBox.YesRole)
		addbtn.clicked.connect(self.addtotable)
		retval = msg.exec_()
		self.barcode_input.setText("")
		self.combobox.setCurrentText("")

	def confirm(self):
		items = []
		for row in range(self.cashier_table.rowCount()):
			item = self.cashier_table.item(int(row),0)
			thistup = []
			count = self.cashier_table.item(int(row),1)
			totalprice = self.cashier_table.item(int(row),3)
			product = self.cr.itemdatawithname(self,item.text())
			curr_prod_amount = product[2]
			new_prod_amount = int(curr_prod_amount) - int(count.text())
			if row+1 == self.cashier_table.rowCount():
				items.append(f"{str(item.text())},{count.text()},{totalprice.text()},{str(product[3])}")
			else:
				items.append(f"{str(item.text())},{count.text()},{totalprice.text()},{str(product[3])} - ")
			self.cr.execut(self,f"UPDATE goods SET amount = '{new_prod_amount}' WHERE barcode = '{product[3]}'")
		curr_totalpric = self.totalprice_lb.text()
		ss = curr_totalpric.find("$")
		lol = str(' '.join(items))
		self.cr.execut(self,f"INSERT INTO fatora (items,total) VALUES ('{lol}','{curr_totalpric[:ss]}')")

if __name__ == "__main__":
	app = QApplication(argv)
	MainWindow = QMainWindow()
	window = cashierapp()
	window.show()
	exit(app.exec_())


