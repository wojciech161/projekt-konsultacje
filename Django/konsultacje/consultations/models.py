from django.db import models

class Users(models.Model):
	login = models.CharField(max_length = 50)
	last_login_date = models.DateTimeField()
	typ = models.CharField(max_length = 15)
	
class Students(models.Model):
	student_ID = models.ForeignKey(Users)
	name = models.CharField(max_length = 20)
	surname = models.CharField(max_length = 50)
	album_number = models.IntegerField()
	faculty = models.CharField(max_length = 40)
	study_year = models.IntegerField()
	major = models.CharField(max_length = 60)

class Administrators(models.Model):
	administrator_ID = models.ForeignKey(Users)
	name = models.CharField(max_length = 20)
	surname = models.CharField(max_length = 50)

class Assistants(models.Model):
	assistant_ID = models.ForeignKey(Users)
	name = models.CharField(max_length = 20)
	surname = models.CharField(max_length = 50)

class InfoBoards(models.Model):
	date_of_adding = models.DateTimeField()
	message = models.CharField(max_length = 300)

class Localizations(models.Model):
	room = models.CharField(max_length = 8)
	building = models.CharField(max_length = 8)

class Tutors(models.Model):
	tutor_ID = models.ForeignKey(Users)
	degree = models.CharField(max_length = 40)
	name = models.CharField(max_length = 20)
	surname = models.CharField(max_length = 50)
	institute = models.CharField(max_length = 50)
	phone = models.CharField(max_length = 20)
	email = models.CharField(max_length = 50)
	www = models.CharField(max_length = 60)
	localization_ID = models.ForeignKey(Localizations)
	infoboard_ID = models.ForeignKey(InfoBoards)

class Consultations(models.Model):
	tutor_ID = models.ForeignKey(Tutors)
	start_hour = models.DateTimeField()
	end_hour = models.DateTimeField()
	day = models.CharField(max_length = 15)
	week_type = models.CharField(max_length = 1)
	students_limit = models.IntegerField()
	localization_ID = models.ForeignKey(Localizations)

class ConsultationAssignments(models.Model):
	student_ID = models.ForeignKey(Students)
	consultation_ID = models.ForeignKey(Consultations)
	day = models.DateTimeField()
