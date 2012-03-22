#!/usr/bin/env python
#encoding:UTF-8

#Generowanie pliku z tabela HTML

import sys
import MySQLdb

connection = MySQLdb.connect("localhost", "root", "password", "projekt")

c = connection.cursor()
CSV = ""
#Pobieranie instytutow
c.execute("SELECT DISTINCT Institute FROM Tutors")
for ins in c.fetchall ():
        #1 kolumna tabeli - instytuty(katedry)
	query = "SELECT degree, name, surname, tutor_ID, phone, email, www  FROM Tutors WHERE Institute = '%s'" % (ins[0])
	c.execute(query)
	#2 kolumna tabeli - prowadzacy
	for prof in c.fetchall ():
		#3 kolumna tabeli - terminy konsultacji
		query= "SELECT * FROM Consultations WHERE tutor_ID = '%s'" % (prof[3]) #laczenie tabel - tutor_ID
		c.execute(query)
		for termin in c.fetchall():
			CSV = CSV + "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (ins[0], prof[3], prof[0], prof[1], prof[2], prof[4], prof[6], prof[5], termin[2], termin[3], termin[4], termin[5], termin[6])



#print CSV
#Zapis danych do pliku table.csv
f = open('table.csv', 'w')
f.write(CSV)
f.close()
