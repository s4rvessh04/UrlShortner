import sqlite3
import datetime


conn = sqlite3.connect('database.db')

c = conn.cursor()

conn.execute(""" CREATE TABLE IF NOT EXISTS database(
	    id INTEGER PRIMARY KEY AUTOINCREMENT,
	    url TEXT NOT NULL,
	    newurl TEXT NOT NULL,
		shorturl TEXT NOT NULL,
		date TEXT NOT NULL
		
	)""")


today = datetime.date.today()
timedelta = datetime.timedelta(days=1)
# yesterday = today - timedelta


class DataBase:
	def __init__(self, data):
		self.data = data

	def addData(self,data,newurl,keyurl):
		with conn:
			c.execute("INSERT INTO database(url,newurl,shorturl,date) VALUES(?,?,?,?)",(data,newurl,keyurl,today,))
			print('INSERTED')

	def viewData(self):
		with conn:
			rows = c.execute("SELECT * FROM database").fetchall()
			for row in rows:
				print(row)

	def deleteData(self): #deletes everything
		with conn:
			c.execute("DELETE FROM database")
		print('DELETED')


	def checkLinks(self,data):
		with conn:
			link = c.execute("SELECT url FROM database WHERE url = ?",(data,)).fetchone()[0]
			if link != None:
				return link

			else:return False

	def occupiedLinks(self,data):
		with conn:
		    sl = c.execute("""SELECT newurl FROM database WHERE url = ?""", (data,)).fetchone()
		    for slink in sl:
		        return slink

	def getNewGenLink(self,data):
		with conn:
			rows = c.execute("SELECT generatedurl FROM database WHERE url = ?", (data,)).fetchone()
			for row in rows:
				print(row)


if __name__ == '__main__':
	with conn:
		rows = c.execute("SELECT date FROM database").fetchall()
		for row in rows:
			req = row[0]
			if str(today) > req:
				c.execute("DELETE FROM database WHERE date=?",(req,)).fetchall()
	DataBase('foo').viewData()