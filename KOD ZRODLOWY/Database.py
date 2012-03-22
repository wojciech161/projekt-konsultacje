# Functions for using database(MySQL)
# Authors: Marcin Wojciechowski, Lukasz Leczycki

#-*- coding: utf-8 -*-

import MySQLdb

def connectToDatabase(host, user, password, databaseName):
    """Funkcja laczy sie z baza danych."""
    
    try:
         db = MySQLdb.connect(host, user, password, databaseName)
    except:
         print "Nie udalo sie podlaczyc"
         return -1
	    
    return db

def closeDBConnection(dbHandle):
	u"""Funkcja zamyka polaczenie z baza danych"""
	
	dbHandle.close()


def addLocalization(dbhandle, room, building):
	"""Funkcja dodajaca lokalizacje do bazy danych
	Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym"""
	
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

def changeLocalization(dbhandle, localizationID, room, building):
	"""Funkcja zmieniajaca lokalizacje wg ID
	Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym"""
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
	
def getLocalization(dbhandle, localizationID):
	"""Funkcja zwracajaca dane o lokalizacji po podaniu ID"""
	
	cursor = dbhandle.cursor()
	
	sqlquery = """select * from Localizations where localization_ID = %d""" %localizationID
	
	try:
		cursor.execute(sqlquery)
		results = cursor.fetchall()
		return results
	except:
		print "Error with getting localization"
		return -1
	

def addInfoBoard(dbhandle):
	"""Funkcja dodajaca pusty InfoBoard
	Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym"""

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

def addInfoBoardWithMessage(dbhandle, message):
	"""Funkcja dodaje InfoBoard z wiadomoscia.
	Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym"""
	
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

def changeInfoBoard(dbhandle, infoBoardID, message):
	"""Funkcja zmieniajaca wiadomosc w infoboard o danym id
	Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym"""
	
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
	
def getInfoBoard(dbhandle, infoboardID):
	"""Funkcja pobierajaca InfoBoard po podaniu ID"""
	
	cursor = dbhandle.cursor()
	
	sqlquery = """select * from InfoBoards where infoboard_ID = %d"""%(infoboardID)
	
	try:
		cursor.execute(sqlquery)
		results = cursor.fetchall()
		return results
	except:
		print "Error with getting infoboard"
		return -1

def addConsultation(dbhandle, tutorID, startHour, endHour, consultationDay, weekType, studentsLimit, localizationID):
	"""Funkcja dodaje konsultacje
	Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym"""
	
	cursor = dbhandle.cursor()
	
	sqlquery = """INSERT INTO Consultations(
	tutor_ID, startHour, endHour, day, weekType, studentsLimit, localization_id) 
	values ('%d', '%s', '%s', '%s', '%s', '%d', '%d');""" % (tutorID, startHour, endHour, consultationDay, weekType, studentsLimit, localizationID)
	
	try:
		cursor.execute(sqlquery)
		dbhandle.commit()
	except:
		print "Error with adding consultation!"
		dbhandle.rollback()
		return -1
	
	return 0

def deleteAllConsultations(dbhandle):
	"""Funkcja usuwa wszystkie konsultacje z bazy
	Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym"""
	
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

def deleteTutorConsultations(dbhandle, tutorID):
	"""Funkcja usuwa konsultacje danego prowadzacego
	Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym"""
	
	cursor = dbhandle.cursor()
	
	sqlquery = """delete from Consultations where tutor_ID = %d""" %tutorID
	
	try:
		cursor.execute(sqlquery)
		dbhandle.commit()
	except:
		print "Error with deleting consultation"
		dbhandle.rollback()
		return -1
	
	return 0
	
def deleteConsultation(dbhandle, consultationID):
	"""Funkcja usuwa konsultacje o podamym ID
	Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym"""
	
	cursor = dbhandle.cursor()
	
	sqlquery = """delete from Consultations where consultation_ID = %d""" %consultationID
	
	try:
		cursor.execute(sqlquery)
		dbhandle.commit()
	except:
		print "Error with deleting consultation"
		dbhandle.rollback()
		return -1
	
	return 0
	
def editConsultation(dbhandle, consultationID, startHour, endHour, consultationDay, weekType, studentsLimit, localizationID):
	"""Funkcja edytuje konsultacje o podanym ID
	Zwraca 0 przy poprawnym zakonczeniu, -1 w blednym"""
	
	cursor = dbhandle.cursor()
	
	sqlquery1 = """update Consultations set startHour = '%s' where consultation_ID = %d""" %(startHour, consultationID)
	sqlquery2 = """update Consultations set endHour = '%s' where consultation_ID = %d""" %(endHour, consultationID)
	sqlquery3 = """update Consultations set day = '%s' where consultation_ID = %d""" %(consultationDay, consultationID)
	sqlquery4 = """update Consultations set weekType = '%s' where consultation_ID = %d""" %(weekType, consultationID)
	sqlquery5 = """update Consultations set studentsLimit = '%d' where consultation_ID = %d""" %(studentsLimit, consultationID)
	sqlquery6 = """update Consultations set localization_ID = '%d' where consultation_ID = %d""" %(localizationID, consultationID)
	
	try:
		cursor.execute(sqlquery1)
		cursor.execute(sqlquery2)
		cursor.execute(sqlquery3)
		cursor.execute(sqlquery4)
		cursor.execute(sqlquery5)
		cursor.execute(sqlquery6)
		dbhandle.commit()
	except:
		print "Error with editing consultation"
		dbhandle.rollback()
		return -1
	
	return 0

def getAllTutorsIDs(dbhandle):
	u"""Funkcja zwracajaca ID wszystkich prowadzacych """
	
	cursor = dbhandle.cursor()
	
	sqlquery = """select tutor_ID from Tutors"""
	
	try:
		cursor.execute(sqlquery)
		results = cursor.fetchall()
		return results
	except:
		print "Error with getting Tutor id s"
		return -1
	

def getAllTableValues(dbhandle, tutorID):
	u""" Funkcja zwracajaca wszystkie wartosci potrzebne do wygenerowania tabeli
	Zwraca dane w kolejnosci:
	IMIE NAZWISKO WWW STOPIEN TEL GODZINYKONSULTACJI DZIEN TYPTYG. BUDYNEK POKOJ WIADOMOSC
	dla prowadzacego o podanym ID"""

	cursor = dbhandle.cursor()
	
	sqlquery = """select t.name, t.surname, t.www, t.degree, t.phone, c.startHour, 
	c.endHour, c.day, c.weekType, l.building, l.room, ib.message
	from Tutors t 
	join Consultations c on (c.tutor_ID = t.tutor_ID) 
	join Localizations l on (t.localization_ID = l.localization_ID) 
	join InfoBoards ib on (t.infoboard_ID = ib.infoboard_ID) 
	where t.tutor_ID = %d"""%tutorID
	
	try:
		cursor.execute(sqlquery)
		results = cursor.fetchall()
		return results
	except:
		print "Error with getting table information"
		return -1

def addTutor(dbHandle, **data):
    u"""Funkcja dodająca Prowadzącego
        Parametry dbHandle - wskaźnik na połączoną bazę danych
        **data - mapa danych do wprowadzenia. Minimum jakie musi być wprowadzone
        to login, name, surname, institute, email

        Funkcja zwraca -1 jeśli nie wykona się poprawnie wypisuje też błąd
        Funkcja zwraca 1 jeśli wykona się poprawnie
        Funkcja łapie wyjątki dotyczące niepoprawnego wysłania zapytania do bazy
        """
    cursor = dbHandle.cursor()
    
    if(data.has_key('name')):
        name = data['name']
    else:
        print "Name not specified"
        return -1
    
    if(data.has_key('surname')):
        surname = data['surname']
    else:
        print "Surname not specified"
        return -1
    
    if(data.has_key('login')):
        login = data['login']
    else:
        print "Login not specified"
        return -1
    
    if (data.has_key('institute')):
        institute = data['institute']
    else:
        print "Institute not specified"
        return -1

    if (data.has_key('email')):
        email = data['email']
    else:
        print "Email not specified"
        return -1
    
    sqlqueryU = """INSERT INTO Users (login, type) values ('%s', 'tutor') """ % (login)
    
    try:
        cursor.execute(sqlqueryU)
        dbHandle.commit()
    except:
        print "Error with inserting data!1"
        dbHandle.rollback()
        return -1

    sqlqueryU = """SELECT user_ID FROM USERS WHERE login = ('%s')""" % (login)

    try:
        cursor.execute(sqlqueryU)
        id_u= cursor.fetchone()[0]
        dbHandle.commit()
    except:
        print "Error with inserting data!2"
        dbHandle.rollback()
        return -1
    print id_u
    sqlqueryT = """INSERT INTO Tutors (tutor_id, name, surname, institute, email)
    values ('%s', '%s', '%s', '%s', '%s')""" % (id_u, name, surname, institute, email)
    
    try:
        cursor.execute(sqlqueryT)
        dbHandle.commit()
        print "Udalo sie"
    except:
        print "Error with inserting data!3"
        dbHandle.rollback()
        return -1
    
    #////////////////////////Koniec obowiązkowych danych
    
    if(data.has_key('degree')):
        sqlqueryT = """UPDATE Tutors set degree = '%s' where tutor_id =
        '%s'""" % (data['degree'], id_u)
        try:
            cursor.execute(sqlqueryT)
            dbHandle.commit()
        except:
            print "Error with inserting data4!"
            dbHandle.rollback()
            return -1
        
    if(data.has_key('phone')):
        sqlqueryT = """UPDATE Tutors set phone = '%s' where tutor_id =
        '%s' """ % (data['phone'], id_u)
        try:
            cursor.execute(sqlqueryT)
            dbHandle.commit()
        except:
            print "Error with inserting data5!"
            dbHandle.rollback()
            return -1

    if (data.has_key('www')):
        sqlqueryT = """UPDATE Tutors set www = '%s' where tutor_id =
        '%s' """ % (data['www'], id_u)
        try:
            cursor.execute(sqlqueryT)
            dbHandle.commit()
        except:
            print "Error with inserting data6!"
            dbHandle.rollback()
            return -1

    if(data.has_key('room') and data.has_key('building')):
        sqlqueryL = """SELECT localization_id FROM Localizations where
        room = '%s' and building = '%s'"""
        id_l = -1
        try:
            cursor.execute(sqlqueryL)
            id_l = cursor.fetchone()[0]
            dbHandle.commit()
        except:
            print "Error with inserting data7!"
            dbHandle.rollback()
            return -1
      #  if(id_l>-1):
        sqlqueryT = """UPDATE Tutors set localization_id = '%s' where tutor_id =
        '%s' """ % (id_l, id_u)
        try:
            cursor.execute(sqlqueryT)
            dbHandle.commit()
        except:
            print "Error with inserting data8!"
            dbHandle.rollback()
            return -1
    return 1
#//////////////////////Koniec funkcji add Tutor


#/////////////////////Funkcja editTutor

def editTutor(dbHandle, tutor_id, **data):
    u"""Zmienia dane prowadzącego o zadanym id
        Parametry dbHandle - wskaźnik na połączoną bazę danych
        tutor_id - dane id tutora którego dane chcemy zmienić
        (prawdopodobnie bedzie kolejna funkcja do odebrania tego)
        **data -  dane do zmiany
        Funkcja zwraca -1 jeśli nie wykona się poprawnie wypisuje też błąd
        Funkcja zwraca 1 jeśli wykona się poprawnie
        Funkcja łapie wyjątki dotyczące niepoprawnego wysłania zapytania do bazy   
    """
    cursor = dbHandle.cursor()
    if(data.has_key('name')):
        sqlquery = """UPDATE Tutors SET name = '%s' where tutor_id =
        '%s' """ % (data['name'], tutor_id)
        try:
            cursor.execute(sqlquery)
            dbHandle.commit()
        except:
            print "Error with updating name!"
            dbHandle.rollback()
            return -1

    if(data.has_key('surname')):
        sqlquery = """UPDATE Tutors SET surname = '%s' where tutor_id =
        '%s' """ % (data['surname'], tutor_id)
        try:
            cursor.execute(sqlquery)
            dbHandle.commit()
        except:
            print "Error with updating surname!"
            dbHandle.rollback()
            return -1

    if(data.has_key('degree')):
        sqlquery = """UPDATE Tutors SET degree = '%s' where tutor_id =
        '%s' """ % (data['degree'], tutor_id)
        try:
            cursor.execute(sqlquery)
            dbHandle.commit()
        except:
            print "Error with updating degree!"
            dbHandle.rollback()
            return -1

    if(data.has_key('institute')):
        sqlquery = """UPDATE Tutors SET institute = '%s' where tutor_id =
        '%s' """ % (data['institute'], tutor_id)
        try:
            cursor.execute(sqlquery)
            dbHandle.commit()
        except:
            print "Error with updating institute!"
            dbHandle.rollback()
            return -1

    if(data.has_key('phone')):
        sqlquery = """UPDATE Tutors SET phone = '%s' where tutor_id =
        '%s' """ % (data['phone'], tutor_id)
        try:
            cursor.execute(sqlquery)
            dbHandle.commit()
        except:
            print "Error with updating phone!"
            dbHandle.rollback()
            return -1

    if(data.has_key('email')):
        sqlquery = """UPDATE Tutors SET email = '%s' where tutor_id =
        '%s' """ % (data['email'], tutor_id)
        try:
            cursor.execute(sqlquery)
            dbHandle.commit()
        except:
            print "Error with updating email!"
            dbHandle.rollback()
            return -1

    if(data.has_key('www')):
        sqlquery = """UPDATE Tutors SET www = '%s' where tutor_id =
        '%s' """ % (data['www'], tutor_id)
        try:
            cursor.execute(sqlquery)
            dbHandle.commit()
        except:
            print "Error with updating www!"
            dbHandle.rollback()
            return -1


    if(data.has_key('room') and data.has_key('building')):
        sqlquery = """SELECT localization_id FROM Localizations where
        room = '%s' and building = '%s'"""
  
        try:
            cursor.execute(sqlquery)
            id_l = cursor.fetchone()[0]
            dbHandle.commit()
        except:
            print "Error with inserting data!"
            dbHandle.rollback()
            return -1
       
        sqlquery = """UPDATE Tutors set localization_id = '%s where tutor_id =
        '%s' """ % (id_l, id_u)
        try:
            cursor.execute(sqlquery)
            dbHandle.commit()
        except:
            print "Error with inserting data!"
            dbHandle.rollback()
            return -1

    return 1
    
def getUserIDByLogin(dbhandle, login):
	u""" Funkcja zwraca UID po podaniu loginu
	Jesli sie nie wykona zwraca -1"""

	cursor = dbhandle.cursor()
	
	sqlquery = """select user_ID from Users where login = '%s'"""%login
	
	try:
		cursor.execute(sqlquery)
		results = cursor.fetchone()
		return results
	except:
		print "Error with getting table information"
		return -1
		
def getUserType(dbhandle, uid):
	u""" Funkcja zwraca typ uzytkownika po podaniu UID
	Jesli sie nie wykona zwraca -1"""

	cursor = dbhandle.cursor()
	
	sqlquery = """select type from Users where user_ID = '%d'"""%uid
	
	try:
		cursor.execute(sqlquery)
		results = cursor.fetchone()
		return results
	except:
		print "Error with getting table information"
		return -1



#Przyklad. Uzupelnijcie dane
#Wszystko co ponizej bedzie do usuniecia w ostatecznym rozrachunku.

#dbcon = connectToDatabase("localhost", "pzuser", "pzpass", "ProjektZespolowy")

#res = getUserType(dbcon, "jnowak")

#print res

#for row in res:
#     print row

#closeDBConnection(dbcon)
