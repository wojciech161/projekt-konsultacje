# Obsluga bazy danych plus funkcje pobierajace rozne wartosci z bazy
# Autor: Marcin Wojciechowski

import MySQLdb

#Funkcja laczy sie z baza danych.
def connectToDatabase(host, user, password, databaseName):
	db = MySQLdb.connect(host, user, password, databaseName)
	return db

#Funkcja zamyka polaczenie z baza danych
def closeDBConnection(dbHandle):
	dbHandle.close()

#Przykladowa funkcja wrzucajaca cos do bazy
#(zebyscie wiedzieli jak pozniej do wyjebania)
def insertToLocations(dbhandle, room, building):
	cursor = dbhandle.cursor()
	
	sqlquery = """INSERT INTO Localizations(room, building) values('%s', '%s')""" %(room, building)
	
	try:
		cursor.execute(sqlquery)
		dbhandle.commit()
	except:
		print "Error with inserting data!"
		dbhandle.rollback()

#Przykladowa funkcja wyswietlajaca cos z bazy
#(zebyscie wiedzieli jak pozniej do wyjebania)
def printLocalizations(dbHandle):
	cursor = dbHandle.cursor()
	
	sqlquery = """select * from Localizations"""
	
	try:
		cursor.execute(sqlquery)
		
		print "Localizations table"
		print "id	room	building"
		results = cursor.fetchall()
		for row in results:
			print "%s 	%s 	%s" %(row[0], row[1], row[2])
	except:
		print "Error with reading data"

#Przyklad. Uzupelnijcie dane
host = "localhost"
user = "UZYTKOWNIK"
password = "HASLO"
databaseName = "NAZWA BAZY"
	
dbcon = connectToDatabase(host, user, password, databaseName)

#Odkomentowac co chcecie
#insertToLocations(dbcon, "51", "C-3")
#printLocalizations(dbcon)

closeDBConnection(dbcon)
