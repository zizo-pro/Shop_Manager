from PySide2.QtWidgets import QMessageBox

class msgbox():
	def __init__(self,parent=None):
		self.msg = QMessageBox()
		# super(msgbox,self).__init__(parent)
	def criticalmessagebox(self, text):
		self.msg.setIcon(QMessageBox.Critical)
		self.msg.setText(text)
		return self.msg
	def infomessagebox(self,text):
		self.msg = QMessageBox()
		self.msg.setIcon(QMessageBox.Information)
		self.msg.setText(text)
		return self.msg
