from flask import Flask,url_for,redirect,render_template,request
from main import slinkGen, shortenUrls
import sqlite3
import datetime

app = Flask(__name__)
today = datetime.date.today()

@app.route("/", methods=["GET","POST"])
def homepage():
	if request.method == "POST":
		if len(str(request.form['getUrl'])) == 0:
			return redirect(url_for('error'))
		else:
			enteredlink = str(request.form['getUrl'])
			with sqlite3.connect("database.db") as conn:
				c = conn.cursor()
				try:
					if enteredlink in c.execute("SELECT url FROM database WHERE url=?",(enteredlink,)).fetchone():
						keylink = c.execute("SELECT shorturl FROM database WHERE url=?",(enteredlink,)).fetchone()[0]
						return redirect(url_for('getLink', link=keylink))
				except TypeError:
					c.execute("INSERT INTO database(url,newurl,shorturl,date) VALUES(?,?,?,?)",(enteredlink,slinkGen(),shortenUrls(),today))
					keylink = c.execute("SELECT shorturl FROM database WHERE url=?",(enteredlink,)).fetchone()[0]
					return redirect(url_for('getLink', link=keylink))

	return render_template("index.html")


@app.route("/yourlink/<link>", methods=["GET","POST"])
def getLink(link):
	with sqlite3.connect('database.db') as conn:
		c = conn.cursor()
		nlink = c.execute("SELECT newurl FROM database WHERE shorturl = ?",(link,)).fetchone()[0]
		reLink = f'http://127.0.0.1:5000/{nlink}'
		return render_template("gettingLink.html", link = reLink)


@app.route("/<link>")
def redir(link):
	with sqlite3.connect("database.db") as conn:
		c = conn.cursor()
		try:
			url = c.execute("SELECT newurl FROM database WHERE newurl=?",(link,)).fetchone()[0]	
			if url:
				linked = c.execute("SELECT url FROM database WHERE newurl=?",(url,)).fetchone()[0]
				return redirect(linked)
		except TypeError:
			return redirect(url_for("error"))


@app.route("/About")
def about():
	return render_template("about.html")


@app.route("/ERROR")
def error():
	return render_template("404.html")


if __name__ == '__main__':
	app.run(debug=True)
	with sqlite3.connect("database.db") as conn:
		c = conn.cursor()
		rows = c.execute("SELECT date FROM database").fetchall()
		for row in rows:
			req = row[0]
			if str(today) > req:
				c.execute("DELETE FROM database WHERE date=?",(req,)).fetchall()