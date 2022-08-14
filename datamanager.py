from sqlite3 import connect
class database():
	def __init__(self, parent=None):
		super(database,self).__init__(parent)
		self.databaseconnect("DB/database.db")
	def databaseconnect(self,dbpath):
		global cr,db
		db = connect(dbpath)
		cr = db.cursor()
		return cr
	def itemdatawithbarcode(self,barcode):
		cr.execute(f"SELECT * FROM goods WHERE barcode = '{barcode}'")
		dataitem = cr.fetchone()
		return dataitem
	def executeall(self,sql):
		cr.execute(sql)
		dataitem = cr.fetchall()
		return dataitem
	def executeone(self,sql):
		cr.execute(sql)
		dataitem = cr.fetchone()
		return dataitem
	def execut(self,sql):
		cr.execute(sql)
		db.commit()
	def getallitemsname(self):
		cr.execute("SELECT item FROM goods")
		items = cr.fetchall()
		return items
	def itemdatawithname(self,name):
		cr.execute(f"SELECT * FROM goods WHERE item = '{name}'")
		dataitem = cr.fetchone()
		return dataitem