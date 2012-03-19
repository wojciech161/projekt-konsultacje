#-*- coding: utf-8 -*-

#Obsluga kont użytkowników Admina oraz Usera
#Autor: Łukasz Łęczycki

import MySQLdb
from Database import connectToDatabase, closeDBConnection

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
print 0


#////////////////// Cześć testująca wykomentować wyrzucić wykorzystać 1 z 3
host = "localhost"
user = "root"
password = "shogun13"
databaseName = "Konsultacje"

dbcon = connectToDatabase(host, user, password, databaseName)
if(dbcon == -1):
    print "Blad"
    exit
else:
    data = {'name': "Krzys", "surname":"Kowal", "login": "sta", "institute":
            "AIR", "email": "cos@cos.pl", "degree": "mgr", "phone":"901212","www":"www.nic.nic.com"}
    addTutor(dbcon, **data)
    #editTutor(dbcon, 12, **data)
    closeDBConnection(dbcon)
print addTutor.__doc__
print u"śąć"







