import ldap
from django.contrib.auth.models import User

def authorize(login, password):
	u"""Sprawdzanie na serwerze LDAP-a czy dane pasuja"""
	
	print "authorize"
	server = "ldap://z-student.pwr.wroc.pl:389"
	auth = "uid=%s, ou=People, o=pwr.wroc.pl,o=pracownicy"%login
	ld = ldap.initialize(server)
		
	try:
		result = ld.simple_bind_s(auth, password)
		return result
	except:
		auth = "uid=%s, ou=People, o=student.pwr.wroc.pl,o=studenci"%login
		try:
			result = ld.simple_bind_s(auth, password)
			return result
		except:
			print "Logowanie nie powiodlo sie."
			return -1

class LDAPBackend(object):
	def authenticate(self, username=None, password=None):
		print "Authenticate"
		au = authorize(username, password)
		print au
		if au == -1:
			return None
		
		try:
			user = User.objects.get(username = username)
		except User.DoesNotExist:
			user = User(username=username, password='')
			user.set_unusable_password()
			user.save()
			
		return user

	def get_user(self, user_id):
		try:
			return User.objects.get(pk = user_id)
		except User.DoesNotExist:
			return None
