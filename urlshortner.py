import random
import string
import sqlite3

conn = sqlite3.connect("urls.db")
c = conn.cursor()

#Creats a new database
#And also checks if database of some name exists already(i.e in this case 'urls')

conn.execute(""" CREATE TABLE IF NOT EXISTS urls(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    newurl TEXT NOT NULL
)""")


#this is a Data interpretation object which contains all the actions associated within database

class DataInterpretator:

    def addData(self):
        with conn:
            c.execute("INSERT INTO urls(url , newurl) VALUES(?, ?)",(link ,slink))
            print("Added")

    def viewData(self):
        with conn:
            rows = c.execute("SELECT * FROM urls").fetchall()
            for row in rows:
                print(row)

    def deleteData(self):
        with conn:
            c.execute("DELETE FROM urls")

data = DataInterpretator()

#Actual Script Starts from HERE

link = input("Enter your link here: ")

#This is a loop which checks if user entered any link or not
#and has 10 tries till exit from script

for i in range(11):
    if i == 10:
        print("Too many tries!!")
        exit()
    else:
        if len(link) == 0:
            print("\nNo Link Entered!!")
            link = input("Enter your link here: ")
        else:
            print("\nYour Link:\n"+link)
            break

# this function checks if the user entered link is in database or not
# and calls the particular function when the condition is satisfied
# i.e if the user entered link is not in database it will return the already existing shortned link for db
# if not then it will generate a new link and store it in the database

def checker():
    with conn:
        if c.execute("""SELECT url FROM urls WHERE url = ?""", (link,)).fetchone() != None:
            return occupiedLinks()
        else:
            return slinkGen()

#this function is resposible for generating a slink and adding data in db

def slinkGen():
    chars = string.ascii_letters + string.digits
    global slink
    slink = ""
    for i in range(6): 
        slink += random.choice(chars)
    finishedLink = 'https://shortenmylink.sl/'+ slink
    print("\nShortned Link:\n"+finishedLink)
    # global slink
    # slink = "FykiZs"
    data.addData()

#this function is resposible for printing shortned link when user link matches within database

def occupiedLinks():
    with conn:
        sl = c.execute("""SELECT newurl FROM urls WHERE url = ?""", (link,)).fetchone()
        for slink in sl:
            print("\nShortned Link:\nhttps://shortenmylink.sl/"+slink)


if __name__ == "__main__":            
    checker()
