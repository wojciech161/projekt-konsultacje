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

#Funkcja dodajaca lokalizacje do bazy danych
#Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym
def addLocalization(dbhandle, room, building):
	cursor = dbhandle.cursor()
	
	sqlquery = """INSERT INTO Localizations(room, building) values('%s', '%s')""" %(room, building)
	
	try:
		cursor.execute(sqlquery)
		dbhandle.commit()
	except:
		print "Error with inserting data!"
		dbhandle.rollback()
		return -1
	
	return 0

#Funkcja zmieniajaca lokalizacje wg ID
#Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym
def changeLocalization(dbhandle, localizationID, room, building):
	cursor = dbhandle.cursor()
	
	sqlquery1 = """UPDATE Localizations set room = '%s' where localization_ID = %d""" %(room, localizationID)
	sqlquery2 = """UPDATE Localizations set building = '%s' where localization_ID = %d""" %(building, localizationID)
	
	try:
		cursor.execute(sqlquery1)
		cursor.execute(sqlquery2)
		dbhandle.commit()
	except:
		print "Error with changing localization"
		dbhandle.rollback()
		return -1
	
	return 0
	
#Funkcja zwracajaca dane o lokalizacji po podaniu ID
def getLocalization(dbhandle, localizationID):
	cursor = dbhandle.cursor()
	
	sqlquery = """select * from Localizations where localization_ID = %d""" %localizationID
	
	try:
		cursor.execute(sqlquery)
		results = cursor.fetchall()
		return results
	except:
		print "Error with getting localization"
		return -1
	

#Funkcja dodajaca pusty InfoBoard
#Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym
def addInfoBoard(dbhandle):
	cursor = dbhandle.cursor()
	
	sqlquery = """INSERT INTO InfoBoards() values ()"""
	
	try:
		cursor.execute(sqlquery)
		dbhandle.commit()
	except:
		print "Error with adding InfoBoard"
		dbhandle.rollback()
		return -1
	
	return 0

#Funkcja dodaje InfoBoard z wiadomoscia.
#Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym
def addInfoBoardWithMessage(dbhandle, message):
	cursor = dbhandle.cursor()
	
	sqlquery = """INSERT INTO InfoBoards(message) values ('%s')"""%message
	
	try:
		cursor.execute(sqlquery)
		dbhandle.commit()
	except:
		print "Error with adding InfoBoard"
		dbhandle.rollback()
		return -1
	
	return 0

#Funkcja zmieniajaca wiadomosc w infoboard o danym id
#Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym
def changeInfoBoard(dbhandle, infoBoardID, message):
	cursor = dbhandle.cursor()
	
	sqlquery1 = """UPDATE InfoBoards set message = '%s' where infoboard_ID = %d""" %(message, infoBoardID)
	sqlquery2 = """UPDATE InfoBoards set dateOfAdding = CURRENT_TIMESTAMP where infoboard_ID = %d""" %infoBoardID
	
	try:
		cursor.execute(sqlquery1)
		cursor.execute(sqlquery2)
		dbhandle.commit()
	except:
		print "Error with changing InfoBoard"
		dbhandle.rollback()
		return -1
	
	return 0

#Funkcja dodaje konsultacje
#Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym
def addConsultation(dbhandle, tutorID, startHour, endHour, consultationDay, weekType, studentsLimit):
	cursor = dbhandle.cursor()
	
	sqlquery = """INSERT INTO Consultations(
	tutor_ID, startHour, endHour, consultation_day, weekType, studentsLimit) 
	values ('%d', '%s', '%s', '%s', '%s', '%d');""" % (tutorID, startHour, endHour, consultationDay, weekType, studentsLimit)
	
	try:
		cursor.execute(sqlquery)
		dbhandle.commit()
	except:
		print "Error with adding consultation!"
		dbhandle.rollback()
		return -1
	
	return 0

#Funkcja usuwa wszystkie konsultacje z bazy
#Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym
def deleteAllConsultations(dbhandle):
	cursor = dbhandle.cursor()
	
	sqlquery = """delete from Consultations"""
	
	try:
		cursor.execute(sqlquery)
		dbhandle.commit()
	except:
		print "Error with deleting all consultations"
		dbhandle.rollback()
		return -1
	
	return 0

#Przyklad. Uzupelnijcie dane
#Wszystko co ponizej bedzie do usuniecia w ostatecznym rozrachunku.
host = "localhost"
user = "pzuser"
password = "pzpass"
databaseName = "ProjektZespolowy"
	
dbcon = connectToDatabase(host, user, password, databaseName)

res = getLocalization(dbcon, 2)

print res

closeDBConnection(dbcon)
