#!/usr/bin/env python
#encoding:UTF-8

#Generowanie pliku z tabela HTML

import sys
import MySQLdb

connection = MySQLdb.connect("localhost", "root", "maciek1", "projekt")


HTML = "<table border='1'><tr valign='center'><td>Katedra</td><td>Prowadzący i terminy konsultacji</td></tr>\n"

c = connection.cursor()
TR=""
#Pobieranie instytutow
c.execute("SELECT DISTINCT Institute FROM Tutors")
for ins in c.fetchall ():
        TR = TR + "<tr>"
	#1 kolumna tabeli - instytuty(katedry)
	TR = TR + "<td>%s</td>" % (ins[0])
	query = "SELECT degree, name, surname, tutor_ID, phone, email, www  FROM Tutors WHERE Institute = '%s'" % (ins[0])
	c.execute(query)
	#2 kolumna tabeli - prowadzacy
	TR = TR + "<td><table widht='100%' border='1' rules='rows' frame='void'>"
	for prof in c.fetchall ():
		TR=TR+"<tr><td>%s %s %s<br>%s<br>%s<br>%s</td><td><ul>" % (prof[0], prof[1], prof[2], prof[4], prof[6], prof[5])
		#3 kolumna tabeli - terminy konsultacji
		query= "SELECT * FROM Consultations WHERE tutor_ID = '%s'" % (prof[3]) #laczenie tabel - tutor_ID
		c.execute(query)
		for termin in c.fetchall():
			TR= TR+ "<li>%s - %s, %s %s, %s</li>" % (termin[2], termin[3], termin[4], termin[5], termin[6])
		TR=TR+"</ul><td></tr>"
		
	TR = TR + "</table>"

HTML = HTML + TR

#print HTML
#Zapis tabeli do pliku table.html
f = open('table.html', 'w')
f.write(HTML)
f.close()
