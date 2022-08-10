from sqlite3 import connect
class database():
	def __init__(self, parent=None):
		super(database,self).__init__(parent)
	def databaseconnect(self,dbpath):
		self.db = connect(dbpath)
		self.cr = self.db.cursor()
		return self.cr