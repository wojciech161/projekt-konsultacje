#-*- coding: utf-8 -*--
from django.db import models
import datetime

class User(models.Model):
	login = models.CharField(max_length = 50)
	last_login_date = models.DateTimeField('Data ostatniego logowania', null=True)
	typ = models.CharField(max_length = 15)
	def __unicode__(self):
		return self.login
	
class Student(models.Model):
	student_ID = models.ForeignKey(User)
	name = models.CharField('Imie', max_length = 20)
	surname = models.CharField('Nazwisko', max_length = 50)
	album_number = models.IntegerField('Nr indeksu')
	faculty = models.CharField('Wydzial', max_length = 40, null=True)
	study_year = models.IntegerField('Rok studiow', null=True)
	major = models.CharField('Kierunek', max_length = 60, null=True)
	def __unicode__(self):
		return self.album_number
	
class Administrator(models.Model):
	administrator_ID = models.ForeignKey(User)
	name = models.CharField('Imie', max_length = 20)
	surname = models.CharField('Nazwisko', max_length = 50)
	def __unicode__(self):
		return self.surname + ' ' + self.name
	
class Assistant(models.Model):
	assistant_ID = models.ForeignKey(User)
	name = models.CharField('Imie', max_length = 20)
	surname = models.CharField('Nazwisko', max_length = 50)
	def __unicode__(self):
		return self.surname + ' ' + self.name
	
class Localization(models.Model):
	room = models.CharField('Pokoj', max_length = 8)
	building = models.CharField('Budynek', max_length = 8)
	def __unicode__(self):
		return self.room + ' ' + self.building
		
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
	def __unicode__(self):
		return self.surname + ' ' + self.name
		
class InfoBoard(models.Model):
	date_of_adding = models.DateTimeField('Data dodania')
	message = models.CharField('Tresc wiadomosci', max_length = 300, null=True)
	tutor_id = models.ForeignKey(Tutor)
	def __unicode__(self):
		tut = self.tutor_id
		return tut.surname + ' ' + tut.name

MINUTES_CHOICES = (
    ('15', '15'),
    ('30', '30'),
    ('45', '45'),
	)	
	
HOUR_CHOICES = (
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
	('10', '10'),
	('11', '11'),
	('12', '12'),
	('13', '13'),
	('14', '14'),
	('15', '15'),
	('16', '16'),
	('17', '17'),
	('18', '18'),
	('19', '19'),
	('20', '20'),
	('21', '21'),
	)	
class Consultation(models.Model):
	tutor_ID = models.ForeignKey(Tutor)
	start_hour = models.IntegerField('Godzina rozpoczecia')
	start_minutes = models.CharField(max_length = 2, choices = MINUTES_CHOICES)
	end_hour = models.IntegerField('Godzina zakonczenia')
	end_minutes = models.CharField(max_length = 2, choices = MINUTES_CHOICES)
	day = models.CharField('Dzien', max_length = 20)
	week_type = models.CharField('Typ tygodnia', max_length = 1)
	students_limit = models.IntegerField('Limit', null=True)
	students_registred = models.IntegerField('Ilosc zarejestrowanych', null = True)
	localization_ID = models.ForeignKey(Localization)
	expiry_date = models.DateField()
	def __unicode__(self):
		tut = self.tutor_ID
		tekst = ' '.join([ "%s %s %s %s %s" % (tut.surname, tut.name, self.start_hour, self.end_hour, self.day) ])
		return tekst

class ConsultationAssignment(models.Model):
	student_ID = models.ForeignKey(Student)
	consultation_ID = models.ForeignKey(Consultation)
	day = models.DateTimeField('Dzien')
	def __unicode__(self):
		stud = self.student_ID
		cons = self.consultation_ID
		tut = cons.tutor_ID
		return stud.surname + ' konsultacje u  ' + tut.surname + ' o godzinie ' + cons.start_hour 
