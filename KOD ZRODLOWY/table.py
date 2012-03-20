#!/usr/bin/env python
#encoding:UTF-8

import sys
import MySQLdb
import csv

con = MySQLdb.connect("localhost", "root", "", "projekt")


HTML=""

HTML= HTML + "<table border='1'><tr valign='center'><td>Katedra</td><td>Prowadzący i terminy konsultacji</td></tr>\n"

c = con.cursor()
TR=""
c.execute("SELECT DISTINCT Institute FROM Tutors")
for ins in c.fetchall ():
        TR = TR + "<tr>"
	#1 kolumna - zaklady
	TR = TR + "<td>%s</td>" % (ins[0])
	query = "SELECT degree, name, surname, tutor_ID, phone, email, www  FROM Tutors WHERE Institute = '%s'" % (ins[0])
	c.execute(query)
	#2 kolumna - nazwiska
	TR = TR + "<td><table widht='100%' border='1' rules='rows' frame='void'>"
	for kto in c.fetchall ():
		TR=TR+"<tr><td>%s %s %s<br>%s<br>%s<br>%s</td><td><ul>" % (kto[0], kto[1], kto[2], kto[4], kto[6], kto[5])
		#3 kolumna - godziny
		query= "SELECT * FROM Consultations WHERE tutor_ID = '%s'" % (kto[3])
		c.execute(query)
		for termin in c.fetchall():
			TR= TR+ "<li>%s - %s, %s %s, %s</li>" % (termin[2], termin[3], termin[4], termin[5], termin[6])
		TR=TR+"</ul><td></tr>"
		
	TR = TR + "</table>"

HTML = HTML + TR

print HTML
f = open('table.html', 'w')
f.write(HTML)
f.close()
