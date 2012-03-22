from django.db import models

class User(models.Model):
	login = models.CharField(max_length = 50)
	last_login_date = models.DateTimeField('Data ostatniego logowania', null=True)
	typ = models.CharField(max_length = 15)
	
class Student(models.Model):
	student_ID = models.ForeignKey(User)
	name = models.CharField('Imie', max_length = 20)
	surname = models.CharField('Nazwisko', max_length = 50)
	album_number = models.IntegerField('Nr indeksu')
	faculty = models.CharField('Wydzial', max_length = 40, null=True)
	study_year = models.IntegerField('Rok studiow', null=True)
	major = models.CharField('Kierunek', max_length = 60, null=True)

class Administrator(models.Model):
	administrator_ID = models.ForeignKey(User)
	name = models.CharField('Imie', max_length = 20)
	surname = models.CharField('Nazwisko', max_length = 50)

class Assistant(models.Model):
	assistant_ID = models.ForeignKey(User)
	name = models.CharField('Imie', max_length = 20)
	surname = models.CharField('Nazwisko', max_length = 50)

class InfoBoard(models.Model):
	date_of_adding = models.DateTimeField('Data dodania')
	message = models.CharField('Tresc wiadomosci', max_length = 300, null=True)

class Localization(models.Model):
	room = models.CharField('Pokoj', max_length = 8)
	building = models.CharField('Budynek', max_length = 8)

class Tutor(models.Model):
	tutor_ID = models.ForeignKey(User)
	degree = models.CharField('Stopien naukowy', max_length = 40, null=True)
	name = models.CharField('Imie', max_length = 20)
	surname = models.CharField('Nazwisko', max_length = 50)
	institute = models.CharField('Jednostka organizacyjna', max_length = 50)
	phone = models.CharField('Telefon', max_length = 20, null=True)
	email = models.CharField('E-mail', max_length = 50)
	www = models.CharField('WWW', max_length = 60, null=True)
	localization_ID = models.ForeignKey(Localization)
	infoboard_ID = models.ForeignKey(InfoBoard)

class Consultation(models.Model):
	tutor_ID = models.ForeignKey(Tutor)
	start_hour = models.DateTimeField('Godzina rozpoczecia')
	end_hour = models.DateTimeField('Godzina zakonczenia')
	day = models.CharField('Dzien', max_length = 15)
	week_type = models.CharField('Typ tygodnia', max_length = 1)
	students_limit = models.IntegerField('Limit', null=True)
	localization_ID = models.ForeignKey(Localization)

class ConsultationAssignment(models.Model):
	student_ID = models.ForeignKey(Student)
	consultation_ID = models.ForeignKey(Consultation)
	day = models.DateTimeField('Dzien')
