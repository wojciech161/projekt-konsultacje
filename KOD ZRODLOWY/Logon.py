# Authorization using LDAP protocol
# Author: Marcin Wojciechowski
# Date: 20.03.2012

import ldap
from Database import getUserIDByLogin, getUserType, connectToDatabase

def authorization(login, password, dbConnection):
	u"""Function authorizes a user
		Returns UID if login is correct
		Otherwise returns -1"""
		
	server = "ldap://z-student.pwr.wroc.pl:389"
	auth = "uid=%s, ou=People, o=student.pwr.wroc.pl,o=pracownicy"%login
	ld = ldap.initialize(server)
	
	try:
		result = ld.simple_bind_s(auth, password)
	except:
		print "Logowanie nie powiodlo sie."
		return -1
	else:
		return getUserIDByLogin(dbConnection, login)
		
def checkUser(uid, dbcon):
	u"""Funkcja sprawdza prawa uzytkownika"""
	print uid
	return getUserType(dbcon, uid)
