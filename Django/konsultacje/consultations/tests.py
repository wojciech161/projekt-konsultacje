#-*- coding: utf-8 -*--
#testy jednostkowe: Andrzej Walkowiak#

from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext, loader, Context
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from consultations.models import *
from consultations.views import *
from django.template import Context, loader
from consultations.models import User
from django.contrib import auth
from consultations import consultationdata
from consultations import singleconsultationdata
from consultations import uploadfileform
from datetime import date
from operator import itemgetter, attrgetter
from django.test.client import RequestFactory
import MySQLdb
import cStringIO as StringIO
import csv
import sys
import time
import os

from django.test import TestCase
from django.test.client import Client

class MyUser:
	authenticated = True
	def is_authenticated(self):
		return self.authenticated

class SimpleTest(TestCase):
	login = 't.est'
	tytul = 'dr inz'
	imie = 'adam'
	nazwisko = 'testowy'
	instytut = 'i6'
	budynek = 'C-3'
	pokoj = '11'
	email = 'a@a.pl'
	telefon = '333'
	www = 'www.x.pl'	
	
	def setUp(self):
		"""
		Funkcja wykonujaca sie na starcie testow. Wprowadaza do testowej bazy konta asystenta, tutora i admina
		koniecznych do przetestowania czesci funkcji widoku.
		"""
		self.saveTestAssistant(8001)
		self.saveTestAdministrator(8002)
		self.saveTestTutor(8003, 1)
		
	def saveTestAssistant(self, id):
		"""
		funckja pomocnicza - tworzaca testowego asystenta w testowej bazie
		"""
		user = User()
		user.login = 'asystent.Test'
		user.id = id
		user.save()
		
		assistant = Assistant()
		assistant.surname = 'surnameTest'
		assistant.name = 'nameTest'
		assistant.assistant_ID_id = id
		assistant.assistant_ID = user
		assistant.save()
		
		self.saveTestTutor(id, 4)
		
	def saveTestAdministrator(self, id):
		"""
		funckja pomocnicza - tworzaca testowego administratora w testowej bazie
		"""
		user = User()
		user.login = 'admin.Test'
		user.id = id
		user.save()
		
		admin = Administrator()
		admin.surname = 'surnameTest'
		admin.name = 'nameTest'
		admin.administrator_ID_id = id
		admin.administrator_ID = user
		admin.save()
	
	def saveTestTutor(self, id, loc_id):
		"""
		funckja pomocnicza - tworzaca testowego tutora w testowej bazie, razem z potrzbnymi jego atrybutami
		"""
		user = User()
		tutor = Tutor()
		localization = Localization()
		
		user.login = "tutor.Test"
		user.id = id
		user.save()
		
		localization.id = loc_id
		localization.room = self.pokoj
		localization.building = self.budynek
		localization.save()
		
		tutor.tutor_ID_id = id
		tutor.tutor_ID = user
		tutor.localization_ID_id = loc_id
		tutor.degree = self.tytul
		tutor.name = self.imie
		tutor.surname = self.nazwisko
		tutor.institute = self.instytut
		tutor.phone = self.telefon
		tutor.email = self.email
		tutor.www = self.www
		tutor.save()
		
		iboard = InfoBoard()
		iboard.date_of_adding = date.today()
		iboard.message = ""
		iboard.tutor_id = tutor
		iboard.save()
		
		self.saveTestAdministrator(id)
		
		return tutor
		
	def test_time_cmp(self):
		"""
        Testuje porównywanie czasu, czyli dni i godzin.
		Np. wtorek 15.00 jest przed wtorek 17.00
		a wtorek 13.00 jest przed czwartek 9.00.
        """
		
		a = singleconsultationdata.SingleConsultationsData()
		a.day = 'Wtorek'
		a.start_hour = 15
		
		b = singleconsultationdata.SingleConsultationsData()
		b.day = 'Wtorek'
		b.start_hour = 17
		
		self.assertEqual(time_cmp(a,None), 1)
		self.assertEqual(time_cmp(a,b)<0, True)
		
		a.day = 'Wtorek'
		a.start_hour = 13
		b.day = 'Czwartek'
		b.start_hour = 9
		self.assertEqual(time_cmp(a,b)<0, True)
		b.day = 'Wtorek'
		b.start_hour = 13
		self.assertEqual(time_cmp(a,b), 0)
		
	def test_notAuthenticated(self):
		"""
        Testuje niepowodzenie autoryzacji uzytkownika na przykladowej funkcji to wykorzystujacej.
		Wiele innych funkcji rowniez sprawdza autoryzacje, ale robia to w dokladnie ten sam sposob,
		jak przetestowana tu funkcja. Z tego wzgledu w ich testach nie bedziemy juz tego sprawdzac.
        """
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'login': 't.est', 'tytul': 'dr inz', 'imie': 'adam', 'nazwisko': 'testowy',
												'instytut': 'i6', 'budynek': 'C-3', 'pokoj': '11', 'email': 'a@a.pl', 
												'telefon': '333', 'www': 'www.x.pl'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		testUser.authenticated = False
		setattr(post_request, 'user', testUser)
		result = assistant_adduser(post_request, 1)
		expected = HttpResponseRedirect(reverse('consultations.views.authorization'))
		self.assertEqual(expected['Location']==result['Location'], True)

	def test_assistant_adduser(self):
		"""
		Testuje wprowadzenie usera o id = 9999, loginie 't.est' do bazy przez asystenta. 
		Bada przypadki:
		- zapytania typu POST (wlasciwego), i odpowiedniego dla niego przejscia na stronie
		- poprawnosci wprowadzenia usera do bazy danych
		- zapytania typu GET (niewlasciwego), i odpowiedniego dla niego przejscia na stronie
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'login': 't.est', 'tytul': 'dr inz', 'imie': 'adam', 'nazwisko': 'testowy',
												'instytut': 'i6', 'budynek': 'C-3', 'pokoj': '11', 'email': 'a@a.pl', 
												'telefon': '333', 'www': 'www.x.pl'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = assistant_adduser(post_request, 9999)
		expected = HttpResponseRedirect(reverse('consultations.views.assistant_index', args=(9999,)))
		self.assertEqual(expected['Location']==result['Location'], True)
		
		try:
			User.objects.get(login='t.est')
		except:
			self.fail("Nie dodano usera pomyslnie")
		
		self.saveTestAssistant(9999)
		
		testUser.authenticated = True
		get_request = rf.get('/submit/')
		if not hasattr(get_request, 'user'):
			setattr(get_request, 'user', testUser)
		result = assistant_adduser(get_request, 9999)		
		self.assertTemplateUsed(result, 'assistant_addtutor.html')
		
	
	def test_assistant_consultation_add(self):
		"""
		Testuje wprowadzenie przykladowej konsultacji do bazy przez asystenta.
		Wykorzystuje testowo wprowadzone na start konto tutora o id=8003.
		Bada przypadki:
		- zapytania typu POST (wlasciwego), i odpowiedniego dla niego przejscia na stronie
		- poprawnosci wprowadzenia konsultacji do bazy danych
		- zapytania typu GET (niewlasciwego), i odpowiedniego dla niego przejscia na stronie
		- podania z³ej daty przy wprowadzeniu konsultacji i zachowania systemu w tym przypadku
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 13, 'start_minutes': '00', 'end_hour': 15, 'end_minutes': '00',
												'day': 'Czwartek', 'week_type': 'P', 'students_limit': 0, 'room': '234', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		#self.saveTestTutor(2)
		
		result = assistant_consultation_add(post_request, 8003, 8003)
		expected = HttpResponseRedirect(reverse('consultations.views.assistant_consultation_list', args=(8003, 8003,)))
		self.assertEqual(expected['Location']==result['Location'], True)
		
		try:
			user = User.objects.get(id=8003)
			tutor = Tutor.objects.get(tutor_ID = user)
			Consultation.objects.get(start_hour = 13, start_minutes = '00', end_hour = 15, 
					end_minutes = '00', day = 'Czwartek', week_type = 'P', tutor_ID = tutor)
		except:
			self.fail("Nie dodano konsultacji poprawnie")
			
		rf = RequestFactory()
		get_request = rf.get('/submit/')
		if not hasattr(get_request, 'user'):
			setattr(get_request, 'user', testUser)
			
		#self.saveTestAssistant(80002)
		
		result = assistant_consultation_add(get_request, 8001, 8001)		
		self.assertTemplateUsed(result, "assistant_consultation_add.html")
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 13, 'start_minutes': '00', 'end_hour': 15, 'end_minutes': '00',
												'day': 'Wtorek', 'week_type': 'P', 'students_limit': 0, 'room': '234', 
												'building': 'C-3', 'expiry_date': 'BLEBLE'})
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		expected = HttpResponse('Podano z\xc5\x82\xc4\x85 dat\xc4\x99')
		result = assistant_consultation_add(post_request, 8003, 8003)
		self.assertEqual(result._get_content(), expected._get_content())
	
	def test_admin_consultation_add(self):
		"""
		Testuje wprowadzenie przykladowej konsultacji do bazy przez admina.
		Wykorzystuje testowo wprowadzone na start konto tutora o id=8003.
		Bada przypadki:
		- zapytania typu POST (wlasciwego), i odpowiedniego dla niego przejscia na stronie
		- poprawnosci wprowadzenia konsultacji do bazy danych
		- zapytania typu GET (niewlasciwego), i odpowiedniego dla niego przejscia na stronie
		- podania z³ej daty przy wprowadzeniu konsultacji i zachowania systemu w tym przypadku
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 13, 'start_minutes': '00', 'end_hour': 15, 'end_minutes': '00',
												'day': 'Wtorek', 'week_type': 'P', 'students_limit': 0, 'room': '234', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		#self.saveTestTutor(3)
		
		result = admin_consultation_add(post_request, 8003, 8003)
		expected = HttpResponseRedirect(reverse('consultations.views.admin_consultation_list', args=(8003, 8003,)))
		self.assertEqual(expected['Location']==result['Location'], True)
		rf = RequestFactory()
		get_request = rf.get('/submit/')
		if not hasattr(get_request, 'user'):
			setattr(get_request, 'user', testUser)
			
		try:
			user = User.objects.get(id=8003)
			tutor = Tutor.objects.get(tutor_ID = user)
			Consultation.objects.get(start_hour = 13, start_minutes = '00', end_hour = 15, 
					end_minutes = '00', day = 'Wtorek', week_type = 'P', tutor_ID = tutor)
		except:
			self.fail("Nie dodano konsultacji poprawnie")
			
		#self.saveTestAdministrator(800)
		
		result = admin_consultation_add(get_request, 8003, 8003)		
		self.assertTemplateUsed(result, "admin_consultation_add.html")
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 13, 'start_minutes': '00', 'end_hour': 15, 'end_minutes': '00',
												'day': 'Wtorek', 'week_type': 'P', 'students_limit': 0, 'room': '234', 
												'building': 'C-3', 'expiry_date': 'BLEBLE'})
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		expected = HttpResponse('Podano z\xc5\x82\xc4\x85 dat\xc4\x99')
		result = admin_consultation_add(post_request, 8003, 8003)
		self.assertEqual(result._get_content(), expected._get_content())
		
	def test_admin_adduser(self):
		"""
		Testuje wprowadzenie przykladowego usera o id=9998 i loginie 't.est2' do bazy przez admina.
		Bada przypadki:
		- zapytania typu POST (wlasciwego), i odpowiedniego dla niego przejscia na stronie
		- poprawnosci wprowadzenia usera do bazy danych
		- zapytania typu GET (niewlasciwego), i odpowiedniego dla niego przejscia na stronie
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'login': 't.est2', 'tytul': 'dr inz', 'imie': 'adam', 'nazwisko': 'testowy',
												'instytut': 'i6', 'budynek': 'C-3', 'pokoj': '11', 'email': 'a@a.pl', 
												'telefon': '333', 'www': 'www.x.pl'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_adduser(post_request, 9998)
		expected = HttpResponseRedirect(reverse('consultations.views.admin_index', args=(9998,)))
		self.assertEqual(expected['Location']==result['Location'], True)
		
		try:
			User.objects.get(login='t.est2')
		except:
			self.fail("Nie dodano usera pomyslnie")

		self.saveTestAssistant(9998)
		
		testUser.authenticated = True
		get_request = rf.get('/submit/')
		if not hasattr(get_request, 'user'):
			setattr(get_request, 'user', testUser)
		result = admin_adduser(get_request, 9998)		
		self.assertTemplateUsed(result, 'admin_addtutor.html')
		
	def test_admin_assistant_add(self):
		"""
		Testuje wprowadzenie przykladowego asystenta o id=9997 i loginie 'test.asyst' przez admina.
		Bada przypadki:
		- zapytania typu POST (wlasciwego), i odpowiedniego dla niego przejscia na stronie
		- poprawnosci wprowadzenia konta asystenta do bazy danych
		- zapytania typu GET (niewlasciwego), i odpowiedniego dla niego przejscia na stronie
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'login': 'test.asyst', 'imie': 'adam', 'nazwisko': 'asystent'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_assistant_add(post_request, 9997)
		expected = HttpResponseRedirect(reverse('consultations.views.admin_assistant_list', args=(9997,)))
		self.assertEqual(expected['Location']==result['Location'], True)
		
		try:
			User.objects.get(login='test.asyst')
			Assistant.objects.get(name='adam', surname='asystent')
		except:
			self.fail("Nie dodano asystenta pomyslnie")

		self.saveTestAdministrator(9997)
		
		testUser.authenticated = True
		get_request = rf.get('/submit/')
		if not hasattr(get_request, 'user'):
			setattr(get_request, 'user', testUser)
		result = admin_assistant_add(get_request, 9997)		
		self.assertTemplateUsed(result, 'admin_addassistant.html')
		
	def test_admin_admin_add(self):
		"""
		Testuje wprowadzenie konta admina o id=9996 i loginie 'test.admin' przez inne konto admina.
		Bada przypadki:
		- zapytania typu POST (wlasciwego), i odpowiedniego dla niego przejscia na stronie
		- poprawnosci wprowadzenia konta administratora do bazy danych
		- zapytania typu GET (niewlasciwego), i odpowiedniego dla niego przejscia na stronie
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'login': 'test.admin', 'imie': 'adam', 'nazwisko': 'admin'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_admin_add(post_request, 9996)
		expected = HttpResponseRedirect(reverse('consultations.views.admin_admin_list', args=(9996,)))
		self.assertEqual(expected['Location']==result['Location'], True)
		
		try:
			User.objects.get(login='test.admin')
			Administrator.objects.get(name='adam', surname='admin')
		except:
			self.fail("Nie dodano asystenta pomyslnie")

		self.saveTestAdministrator(9996)
		
		testUser.authenticated = True
		get_request = rf.get('/submit/')
		if not hasattr(get_request, 'user'):
			setattr(get_request, 'user', testUser)
		result = admin_admin_add(get_request, 9996)		
		self.assertTemplateUsed(result, 'admin_addadmin.html')
		
	def test_add_consultation(self):
		"""
		Testuje wprowadzenie przykladowej konsultacji do bazy.
		Wykorzystuje testowo wprowadzone na start konto tutora o id=8003.
		Bada przypadki:
		- zapytania typu POST (wlasciwego), i odpowiedniego dla niego przejscia na stronie
		- poprawnosci wprowadzenia konsultacji do bazy danych
		- zapytania typu GET (niewlasciwego), i odpowiedniego dla niego przejscia na stronie
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': '', 'start_minutes': '00', 'end_hour': 15, 'end_minutes': '00',
												'day': 'Wtorek', 'week_type': 'P', 'students_limit': 0, 'room': '234', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		#self.saveTestTutor(3)
		
		result = add_consultation(post_request, 8003)
		expected = HttpResponse("Nie mozna dodac konsultacji")
		self.assertEqual(result._get_content(), expected._get_content())
		
		post_request = rf.post('/submit/', {'start_hour': 13, 'start_minutes': '00', 'end_hour': 15, 'end_minutes': '00',
												'day': 'Wtorek', 'week_type': 'N', 'students_limit': 0, 'room': '234', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = add_consultation(post_request, 8003)
		expected = HttpResponseRedirect(reverse('consultations.views.consultations_detail', args=(8003, )))
		self.assertEqual(expected['Location']==result['Location'], True)
		
		try:
			user = User.objects.get(id=8003)
			tutor = Tutor.objects.get(tutor_ID = user)
			Consultation.objects.get(start_hour = 13, start_minutes = '00', end_hour = 15, 
					end_minutes = '00', day = 'Wtorek', week_type = 'N', tutor_ID = tutor)
		except:
			self.fail("Nie dodano konsultacji poprawnie")
			
		rf = RequestFactory()
		get_request = rf.get('/submit/')
		if not hasattr(get_request, 'user'):
			setattr(get_request, 'user', testUser)
			
		#self.saveTestAdministrator(800)
		
		result = add_consultation(get_request, 8003)		
		self.assertTemplateUsed(result, "add_consultation.html")

	def test_get_data_for_consultations_detail(self):
		"""
		Testuje pomocnicza funkcje pobierana danych konsultacji dla tutora. 
		Bada przypadki:
		- bledu dodania konsultacji do nieistniejacego tutora
		- sprawdzenie stanu konsultacji przed i po dodaniem
		"""
		result = get_data_for_consultations_detail(123456789)
		self.assertEqual(HttpResponse("Blad krytyczny")._get_content(), result._get_content())
		
		tutor = self.saveTestTutor(9995, 2)   #nowe konto tutora dla tego testu
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': '', 'start_minutes': '00', 'end_hour': 15, 'end_minutes': '00',
												'day': 'Wtorek', 'week_type': 'P', 'students_limit': 0, 'room': '234', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()

		result = get_data_for_consultations_detail(9995)
		if len(result['tutor_connsultations'])!=0:
			self.fail("Tutor ma konsultacje a nie powinien, bo nic nie dodalismy.")
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		add_consultation(post_request, 9995)	#dodaj jedna konsultacje
		result = get_data_for_consultations_detail(9995)
		
		if len(result['tutor_connsultations'])!=0:
			self.fail("Tutor nie ma konsultacji a powinien, bo mu dodalismy.")
		
	def test_consultation_index(self):
		"""
		Testuje poprawnosc wykonania funkcji pobierajacej wszystkich wykladowcow. 
		Bada przypadki:
		- poprawnego przejscia do strony po wykonaniu operacji wyswietlania
		"""
		result = consultation_index(None)
		self.assertTemplateUsed(result, 'index.html')
		
	def test_tutors_index(self):
		"""
		Testuje poprawnosc wykonania funkcji sortujacej wszystkich wykladowcow. 
		Bada przypadki:
		- poprawnego przejscia do strony po wykonaniu operacji wyswietlania
		"""
		result = tutors_index(None)
		self.assertTemplateUsed(result, 'index.html')
	
	def test_tutor_index(self):
		"""
		Bada przypadki:
		- poprawnego przejscia do strony przy uzytkowniku autoryzowanym
		- poprawnego przejscia do strony przy uzytkowniku nieautoryzowanym
		"""
		rf = RequestFactory()
		testUser = MyUser()
		post_request = rf.post('/submit/')	
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = tutor_index(post_request, 8003)
		self.assertTemplateUsed(result, 'tutor_index.html')
		
		testUser.authenticated = False
		expected = HttpResponseRedirect(reverse('consultations.views.authorization'))
		if hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		result = tutor_index(post_request, 8003)	
		self.assertEqual(expected._get_content(), result._get_content())
		
	def test_tutor_detail(self):
		"""
		Testuje funkcje pobeirajaca szczegoly dla wskazanego tutora.
		Bada przypadki:
		- poprawnego pobrania danych tutora
		- poprawnego przejscia do strony po wykonaniu zapytania POST
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'login': 't.est', 'tytul': 'dr inz', 'imie': 'adam', 'nazwisko': 'testowy',
												'instytut': 'i6', 'budynek': 'C-3', 'pokoj': '11', 'email': 'a@a.pl', 
												'telefon': '333', 'www': 'www.x.pl'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = tutor_detail(post_request, 8003)
		self.assertContains(result, "Dane zostały zmienione")
		
	def test_consultations_detail(self):
		"""
		Testuje funkcje pobeirajaca szczegoly dla konsultacji.
		Bada przypadki:
		- poprawnego pobrania danych konsultacji
		- poprawnego przejscia do strony po wykonaniu zapytania POST
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 15, 'start_minutes': '00', 'end_hour': 17, 'end_minutes': '00',
												'day': 'Sobota', 'week_type': 'P', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = consultations_detail(post_request, 8003)
		self.assertTemplateUsed(result, 'consultations_detail.html')
	def test_edit_consultation(self):
		"""
		Testuje funkcje edytujaca konsultacje
		Bada przypadki:
		- poprawnego edytowania konsultacji przy pomocy zmiany startowej godziny dodanej konsultacji
		- poprawnego przejscia do strony po wykonaniu zapytania POST
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 11, 'start_minutes': '00', 'end_hour': 13, 'end_minutes': '00',
												'day': 'Niedziela', 'week_type': 'N', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		user = User.objects.get(id=8003)
		tutor = Tutor.objects.get(tutor_ID = user)
		consultations = Consultation.objects.filter(tutor_ID = tutor.id)
		
		#dodanie przykladowych kons. do edycji
		add_consultation(post_request, 8003)		
		
		consultations = Consultation.objects.filter(tutor_ID = tutor.id)
		cons_id_to_edit = consultations[0].id
		
		self.assertEqual(len(consultations),1)  #upewnienie sie, ze wprowadzone poprawnie
		self.assertEqual(consultations[0].start_hour, 11)
		
		post_request = rf.post('/submit/', {'start_hour': 12, 'start_minutes': '00', 'end_hour': 13, 'end_minutes': '00',
												'day': 'Niedziela', 'week_type': 'N', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = edit_consultation(post_request, 8003, cons_id_to_edit)
		consultations = Consultation.objects.filter(tutor_ID = tutor.id)
		self.assertEqual(consultations[0].start_hour, 12)
		
		expected = HttpResponseRedirect(reverse('consultations.views.consultations_detail', args=(8003,)))
		self.assertEqual(expected._get_content(), result._get_content())
		
	def test_delete_consultation(self):
		"""
		Testuje funkcje kasujaca konsultacje
		Bada przypadki:
		- proby usuwanai konsultacji nieistniejacej
		- poprawne usuniecie istniejacej konsultacji
		- poprawnego przejscia do strony po wykonaniu kasowania
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 11, 'start_minutes': '00', 'end_hour': 13, 'end_minutes': '00',
												'day': 'Niedziela', 'week_type': 'N', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		user = User.objects.get(id=8003)
		tutor = Tutor.objects.get(tutor_ID = user)
		consultations = Consultation.objects.filter(tutor_ID = tutor.id)
		#dodanie przykladowych kons. do kasowania
		
		self.assertEqual(0, len(consultations))   #start - bec konsultacji
		add_consultation(post_request, 8003)
		
		consultations = Consultation.objects.filter(tutor_ID = tutor.id)
		cons_id_to_delete = consultations[0].id
		self.assertEqual(1, len(consultations))   #dodano przykladowe kons.
		
		result = delete_consultation(post_request, 8003, cons_id_to_delete)
		consultations = Consultation.objects.filter(tutor_ID = tutor.id)
		self.assertEqual(0, len(consultations))  #po usunieciu
		
		self.assertTemplateUsed(result, 'consultations_detail.html')
		
	def test_admin_choose_panel(self):
		"""
		Testuje funkcje wyboru panelu
		Bada przypadki:
		- poprawnego przejscia do strony panelu
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_choose_panel(post_request, 8002)
		self.assertTemplateUsed(result, 'admin_choose_panel.html')
	
	def test_edit_infoboard(self):
		"""
		Testuje funkcje zmiany tresci w infoboardzie tutora
		Bada przypadki:
		- poprawnej edycji informacji
		"""
		tutor = self.saveTestTutor(7777, 5)
		#infoboard jest pusty
		user = User.objects.get(id=7777)
		tutor = Tutor.objects.get(tutor_ID = user)
		infoboard = InfoBoard.objects.get(tutor_id = tutor.id)
		self.assertEqual(infoboard.message, '')
		
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'Informacja': 'testoweNoweInfo123'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = edit_infoboard(post_request, user)		#edycja wiadomosci na 'testoweNoweInfo123'
		infoboard = InfoBoard.objects.get(tutor_id = tutor.id)
		self.assertEqual(infoboard.message, 'testoweNoweInfo123')
		
	def test_assistant_index(self):
		"""
		Testuje poprawne indexowanie tutorow przez asystenta
		Bada przypadki:
		- poprawnego przejscia do strony po wyswietleniu asystentow
		"""
		
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = assistant_index(post_request, 8001)
		self.assertTemplateUsed(result, 'assistant_index.html')
	
	def test_assistant_consultations_delete_confirm(self):
		"""
		Testuje poprawne usuwanie konsultacji przez asystenta
		Bada przypadki:
		- poprawnego usuniecia konsultacji przy dobrym potwierdzeniu
		- nieusuniecia przy niepotwierdzeniu
		"""
		
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'potwierdzenie': 'TAK'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = assistant_consultations_delete_confirm(post_request, 8001)
		expected = HttpResponseRedirect(reverse('consultations.views.assistant_consultations_delete', args=(8001,)))
		self.assertEqual(result._get_content(), expected._get_content())
		
		
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'potwierdzenie': 'NIE'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = assistant_consultations_delete_confirm(post_request, 8001)
		self.assertContains(result, "Nie udało się usunąć konsultacji.")
		self.assertTemplateUsed(result, 'assistant_consultations_delete_confirm.html')
		
	def test_assistant_consultations_delete(self):
		"""
		Testuje poprawne usuwanie wszystkich konsultacji przez asystenta
		Bada przypadki:
		- poprawnego usuniecia konsultacji z bazy
		- przejscia do odpowiedniej strony po usunieciu
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 11, 'start_minutes': '00', 'end_hour': 13, 'end_minutes': '00',
												'day': 'Niedziela', 'week_type': 'N', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		consultations = Consultation.objects.all()		
		
		#dodanie przykladowych kons. do edycji
		add_consultation(post_request, 8003)	
		self.assertEqual(len(consultations)>0, True)
		
		result = assistant_consultations_delete(post_request, 8001)
		expected = HttpResponseRedirect(reverse('consultations.views.assistant_index', args=(8001,)))
		self.assertEqual(result._get_content(), expected._get_content())
		
		consultations = Consultation.objects.all()	
		self.assertEqual(len(consultations), 0)
	
	def test_assistant_tutor_edit(self):
		"""
		Testuje poprawne edytowanie informacji o tutorze przez asystenta
		Bada przypadki:
		- poprawnej edycji tutora
		- przejscia do odpowiedniej strony po edycji
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'login': 't.est', 'tytul': 'dr inz', 'imie': 'NOWE_IMIE', 'nazwisko': 'testowy',
												'instytut': 'i6', 'budynek': 'C-3', 'pokoj': '11', 'email': 'a@a.pl', 
												'telefon': '333', 'www': 'www.x.pl'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		self.saveTestTutor(7778, 6)
		user = User.objects.get(id=7778)
		tutor = Tutor.objects.get(tutor_ID = user)
		
		old_name = tutor.name
		new_name = 'NOWE_IMIE'
		
		result = assistant_tutor_edit(post_request, 8001, user)
		expected = HttpResponseRedirect(reverse('consultations.views.assistant_index', args=(7778,)))
		self.assertEqual(result._get_content(), expected._get_content())
		self.assertNotEqual(old_name, new_name)
		
		new_tutor = Tutor.objects.get(tutor_ID = user)
		self.assertEqual(new_tutor.name, new_name)
		
	def test_assistant_tutor_delete_confirm(self):
		"""
		Testuje poprawne przejscie do strony po zatwierdzonym usunieciu tutora przez asystenta
		Bada przypadki:
		- poprawnego przejscia do odpowiedniej strony po usunieciu zatwierdzonym
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = assistant_tutor_delete_confirm(post_request, 8001, 8003)
		self.assertTemplateUsed(result, 'assistant_tutor_delete_confirm.html')
		
	def test_assistant_tutor_delete(self):
		"""
		Testuje poprawne usuniecie tutora przez asystenta
		Bada przypadki:
		- usuniecie wskazanego tutora
		- poprawnego przejscia do odpowiedniej strony po usunieciu
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		
		#utworzenie tutora do kasowania
		self.saveTestTutor(7776, 7)
		user = User.objects.get(id=7776)
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = assistant_tutor_delete(post_request, 7776, user)
		expected = HttpResponseRedirect(reverse('consultations.views.assistant_index', args=(7776,)))
		
		try:
			user = User.objects.get(id=7776)
			self.fail("Nie skasowano poprawnie zamierzonego tutora")
			tutor = Tutor.objects.get(tutor_ID = user)
			self.fail("Nie skasowano poprawnie zamierzonego tutora")
			localization = Localization.objects.get(tutor_id = tutor)
			self.fail("Nie skasowano poprawnie zamierzonego tutora")
		except:
			pass
			
	def test_assistant_consultation_list(self):
		"""
		Testuje poprawne wylistowanie konsultacji tutora przez asystenta
		Bada przypadki:
		- blad w podaniu zlych danych
		- poprawnego przejscia do odpowiedniej strony po prawidlowym procesie
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = assistant_consultation_list(post_request, 0, None)
		self.assertContains(result, "Blad krytyczny")
		
		user = User.objects.get(id=8003)
		result = assistant_consultation_list(post_request, 8001, user)
		self.assertTemplateUsed(result, 'assistant_consultations_list.html')
		
	def test_assistant_consultation_edit(self):
		"""
		Testuje poprawna edycje konsultacji przez asystenta
		Bada przypadki:
		- blad w podaniu zlych danych
		- poprawnego przejscia do odpowiedniej strony po prawidlowym procesie
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 11, 'start_minutes': '00', 'end_hour': 13, 'end_minutes': '00',
												'day': 'Niedziela', 'week_type': 'N', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		user = User.objects.get(id=8003)
		tutor = Tutor.objects.get(tutor_ID = user)
		consultations = Consultation.objects.filter(tutor_ID = tutor.id)
		
		#dodanie przykladowych kons. do edycji
		add_consultation(post_request, 8003)		
		
		consultations = Consultation.objects.filter(tutor_ID = tutor.id)
		cons_id_to_edit = consultations[0].id
		
		self.assertEqual(len(consultations),1)  #upewnienie sie, ze wprowadzone poprawnie
		self.assertEqual(consultations[0].start_hour, 11)
		
		post_request = rf.post('/submit/', {'start_hour': 12, 'start_minutes': '00', 'end_hour': 13, 'end_minutes': '00',
												'day': 'Niedziela', 'week_type': 'N', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = assistant_consultation_edit(post_request, 8001, 8003, cons_id_to_edit)
		consultations = Consultation.objects.filter(tutor_ID = tutor.id)
		self.assertEqual(consultations[0].start_hour, 12)
		self.assertTemplateUsed(result, "assistant_consultation_edit.html")
	
	def test_assistant_consultation_delete_confirm(self):
		"""
		Testuje poprawna przejscie strony po zatwierdzonym usnieciu konsultacji przez asystenta
		Bada przypadki:
		- poprawnego przejscia do odpowiedniej strony po procesie usuniecia
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 11, 'start_minutes': '00', 'end_hour': 13, 'end_minutes': '00',
												'day': 'Niedziela', 'week_type': 'N', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = assistant_consultation_delete_confirm(post_request, 8001, 8003, None)
		self.assertTemplateUsed(result, 'assistant_consultation_delete_confirm.html')
		
	def test_assistant_consultation_delete(self):
		"""
		Testuje poprawn usniecie konsultacji przez asystenta
		Bada przypadki:
		- usuniecia isntiejacej konsultacji
		- poprawnego przejscia do odpowiedniej strony po procesie usuniecia
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 11, 'start_minutes': '00', 'end_hour': 13, 'end_minutes': '00',
												'day': 'Niedziela', 'week_type': 'N', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		#dodanie przykladowych kons. do usuniecia	
		add_consultation(post_request, 8003)
		
		consultations = Consultation.objects.all()
		loc_id = consultations[0].localization_ID
		consultation_id = consultations[0].id
		
			
		self.assertEqual(len(consultations), 1)
			
		result = assistant_consultation_delete(post_request, 8001, 8003, consultation_id)
		
		try:
			consultations = Consultation.objects.get(id = consultation_id)
			self.fail("Nie skasowano poprawnie zamierzonych konsultacji")
			localization = Localization.objects.get(id = loc_id)
			self.fail("Nie skasowano poprawnie zamierzonych konsultacji")
		except:
			pass
			
	def test_assistant_consultation_add(self):
		"""
		Testuje wprowadzenie przykladowej konsultacji do bazy przez asystenta.
		Wykorzystuje testowo wprowadzone na start konto tutora o id=8003.
		Bada przypadki:
		- zapytania typu POST (wlasciwego), i odpowiedniego dla niego przejscia na stronie
		- poprawnosci wprowadzenia konsultacji do bazy danych
		- zapytania typu GET (niewlasciwego), i odpowiedniego dla niego przejscia na stronie
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 9, 'start_minutes': '00', 'end_hour': 11, 'end_minutes': '00',
												'day': 'Czwartek', 'week_type': 'N', 'students_limit': 0, 'room': '234', 
												'building': 'C-5', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		#self.saveTestTutor(3)
		expected = HttpResponseRedirect(reverse('consultations.views.assistant_consultation_list', args=(8001, 8003,)))
		result = assistant_consultation_add(post_request, 8001, 8003)
		self.assertEqual(expected['Location']==result['Location'], True)
		
		try:
			user = User.objects.get(id=8003)
			tutor = Tutor.objects.get(tutor_ID = user)
			Consultation.objects.get(start_hour = 9, start_minutes = '00', end_hour = 11, 
					end_minutes = '00', day = 'Czwartek', week_type = 'N', tutor_ID = tutor)
		except:
			self.fail("Nie dodano konsultacji poprawnie")
			
		rf = RequestFactory()
		get_request = rf.get('/submit/')
		if not hasattr(get_request, 'user'):
			setattr(get_request, 'user', testUser)
			
		#self.saveTestAdministrator(800)
		
		result = assistant_consultation_add(get_request, 8001, 8003)		
		self.assertTemplateUsed(result, "assistant_consultation_add.html")
		
	def test_assistant_consultation_deleteall_confirm(self):
		"""
		Testuje zdarzenia po potwierdzeniu usuniecia wszystkich konsultacji
		Bada przypadki:
		- poprawnego przejscia na strone po usunieciu konsultacji
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = assistant_consultation_deleteall_confirm(post_request, 8001, 8003)
		self.assertTemplateUsed(result, 'assistant_consultation_deleteall_confirm.html')
		
	def test_assistant_consultation_deleteall(self):
		"""
		Testuje usuniecie przez asystenta wszystkich konsultacji tutora
		Bada przypadki:
		- usuniecia wszystkich konsultacji przykladowego tutora o id=8003
		- prawidlowego przejscia na strone po usunieciu wszystkich kosnultacji tutora
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 11, 'start_minutes': '00', 'end_hour': 13, 'end_minutes': '00',
												'day': 'Niedziela', 'week_type': 'N', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		#dodanie przykladowych kons. do usuniecia	
		add_consultation(post_request, 8003)
			
		tutor = Tutor.objects.get(tutor_ID = User.objects.get(id=8003))
		consults = Consultation.objects.filter(tutor_ID_id = tutor.id)		
		self.assertEqual(len(consults)>0, True)
		
		result = assistant_consultation_deleteall(post_request, 8001, 8003)
		self.assertTemplateUsed(result, 'consultations.views.assistant_consultation_list')
		tutor = Tutor.objects.get(tutor_ID = User.objects.get(id=8003))
		consults = Consultation.objects.filter(tutor_ID_id = tutor.id)		
		self.assertEqual(len(consults), 0)
		
	def test_choose_panel(self):
		"""
		Testuje wybor panelu asystenta
		Bada przypadki:
		- prawidlowe przejscie na strone panelu danego asystenta
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = choose_panel(post_request, 8001)
		self.assertTemplateUsed(result, 'choose_panel.html')
		
	def test_assistant_export_csv(self):
		"""
		Testuje uruchomienie eskportu do pliku csv
		Bada przypadki:
		- prawidlowe przejscie na strone eksportu pliku csv
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = assistant_export_csv(post_request, 8001)
		self.assertTemplateUsed(result, 'assistant_export_csv.html')
		
	def test_assistant_import_csv(self):
		"""
		Testuje uruchomienie importu do pliku csv
		Bada przypadki:
		- prawidlowe przejscie na strone importu pliku csv
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = assistant_import_csv(post_request, 8001)
		self.assertTemplateUsed(result, 'assistant_import_csv.html')
		
	def test_export_csv(self):
		"""
		Testuje prawidlowa generacje pliku csv
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = export_csv(post_request, None)
		self.assertEqual(result['Content-Disposition'],'attachment; filename=konsultacje.csv')
	
	def test_admin_index(self):
		"""
		Testuje prawidlowa generacje strony glownej admina
		Bada przypadki:
		- wygenerowania i przejscia do strony glownej admina
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
	
		result = export_csv(post_request, None)
		self.assertTemplateUsed(result, 'admin_index.html')
		
	def test_admin_consultations_delete_confirm(self):
		"""
		Testuje poprawne usuwanie konsultacji przez admina
		Bada przypadki:
		- poprawnego usuniecia konsultacji przy dobrym potwierdzeniu
		- nieusuniecia przy niepotwierdzeniu
		"""
		
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'potwierdzenie': 'TAK'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = admin_consultations_delete_confirm(post_request, 8002)
		expected = HttpResponseRedirect(reverse('consultations.views.admin_consultations_delete', args=(8002,)))
		self.assertEqual(result._get_content(), expected._get_content())
		
		
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'potwierdzenie': 'NIE'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = admin_consultations_delete_confirm(post_request, 8002)
		reload(sys) 
		sys.setdefaultencoding('utf8')
		self.assertContains(result, "Nie udało się usunąć konsultacji.")
		self.assertTemplateUsed(result, 'admin_consultations_delete_confirm.html')
		
	def test_admin_consultations_delete(self):
		"""
		Testuje poprawne usuwanie wszystkich konsultacji przez asystenta
		Bada przypadki:
		- poprawnego usuniecia konsultacji z bazy
		- przejscia do odpowiedniej strony po usunieciu
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 11, 'start_minutes': '00', 'end_hour': 13, 'end_minutes': '00',
												'day': 'Niedziela', 'week_type': 'N', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		consultations = Consultation.objects.all()		
		
		#dodanie przykladowych kons. do edycji
		add_consultation(post_request, 8003)	
		self.assertEqual(len(consultations)>0, True)
		
		result = admin_consultations_delete(post_request, 8002)
		expected = HttpResponseRedirect(reverse('consultations.views.admin_index', args=(8002,)))
		self.assertEqual(result._get_content(), expected._get_content())
		
		consultations = Consultation.objects.all()	
		self.assertEqual(len(consultations), 0)
		
	def test_admin_tutor_edit(self):
		"""
		Testuje poprawne edytowanie informacji o tutorze przez admina
		Bada przypadki:
		- poprawnej edycji tutora
		- przejscia do odpowiedniej strony po edycji
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'login': 't.est', 'tytul': 'dr inz', 'imie': 'NOWE_IMIE_ZMIENIONE_PRZEZ_ADMINA', 'nazwisko': 'testowy',
												'instytut': 'i6', 'budynek': 'C-3', 'pokoj': '11', 'email': 'a@a.pl', 
												'telefon': '333', 'www': 'www.x.pl'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		self.saveTestTutor(7774, 15)
		user = User.objects.get(id=7774)
		tutor = Tutor.objects.get(tutor_ID = user)
		
		old_name = tutor.name
		new_name = 'NOWE_IMIE_ZMIENIONE_PRZEZ_ADMINA'
		
		result = admin_tutor_edit(post_request, 8002, 7774)
		expected = HttpResponseRedirect(reverse('consultations.views.admin_index', args=(8002,)))
		self.assertNotEqual(result._get_content(), expected._get_content())
		self.assertNotEqual(old_name, new_name)
		
		new_tutor = Tutor.objects.get(tutor_ID = user)
		self.assertNotEqual(new_tutor.name, new_name)
		
	def test_admin_tutor_delete_confirm(self):
		"""
		Testuje poprawne przejscie do strony po potwierdzeniu usuniecia tutora przez admina
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_tutor_delete_confirm(post_request, 8002, 8003)
		self.assertTemplateUsed(result, 'admin_tutor_delete_confirm.html')
		
	def test_admin_tutor_delete(self):
		"""
		Testuje poprawne usuniecie tutora przez administratora
		Bada przypadki:
		- usuniecie wskazanego tutora
		- poprawnego przejscia do odpowiedniej strony po usunieciu
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		
		#utworzenie tutora do kasowania
		self.saveTestTutor(7776, 7)
		user = User.objects.get(id=7776)
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = assistant_tutor_delete(post_request, 7776, user)
		expected = HttpResponseRedirect(reverse('consultations.views.admin_index', args=(7776,)))
		
		try:
			user = User.objects.get(id=7776)
			self.fail("Nie skasowano poprawnie zamierzonego tutora")
			tutor = Tutor.objects.get(tutor_ID = user)
			self.fail("Nie skasowano poprawnie zamierzonego tutora")
			localization = Localization.objects.get(tutor_id = tutor)
			self.fail("Nie skasowano poprawnie zamierzonego tutora")
		except:
			pass
			
	def test_admin_consultation_list(self):
		"""
		Testuje poprawne wylistowanie konsultacji tutora przez administratora
		Bada przypadki:
		- blad w podaniu zlych danych
		- poprawnego przejscia do odpowiedniej strony po prawidlowym procesie
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_consultation_list(post_request, 0, None)
		self.assertContains(result, "Blad krytyczny")
		
		user = User.objects.get(id=8003)
		result = admin_consultation_list(post_request, 8002, user)
		self.assertTemplateUsed(result, 'admin_consultations_list.html')
		
	def test_admin_consultation_edit(self):
		"""
		Testuje poprawna edycje konsultacji przez administratora
		Bada przypadki:
		- blad w podaniu zlych danych
		- poprawnego przejscia do odpowiedniej strony po prawidlowym procesie
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 11, 'start_minutes': '00', 'end_hour': 13, 'end_minutes': '00',
												'day': 'Niedziela', 'week_type': 'N', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		user = User.objects.get(id=8003)
		tutor = Tutor.objects.get(tutor_ID = user)
		consultations = Consultation.objects.filter(tutor_ID = tutor.id)
		
		#dodanie przykladowych kons. do edycji
		add_consultation(post_request, 8003)		
		
		consultations = Consultation.objects.filter(tutor_ID = tutor.id)
		cons_id_to_edit = consultations[0].id
		
		self.assertEqual(len(consultations),1)  #upewnienie sie, ze wprowadzone poprawnie
		self.assertEqual(consultations[0].start_hour, 11)
		
		post_request = rf.post('/submit/', {'start_hour': 12, 'start_minutes': '00', 'end_hour': 13, 'end_minutes': '00',
												'day': 'Niedziela', 'week_type': 'N', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_consultation_edit(post_request, 8002, 8003, cons_id_to_edit)
		consultations = Consultation.objects.filter(tutor_ID = tutor.id)
		self.assertEqual(consultations[0].start_hour, 12)
		self.assertTemplateUsed(result, "admin_consultation_edit.html")
		
	def test_admin_consultation_delete_confirm(self):
		"""
		Testuje poprawna przejscie strony po zatwierdzonym usnieciu konsultacji przez administratora
		Bada przypadki:
		- poprawnego przejscia do odpowiedniej strony po procesie usuniecia
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 11, 'start_minutes': '00', 'end_hour': 13, 'end_minutes': '00',
												'day': 'Niedziela', 'week_type': 'N', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_consultation_delete_confirm(post_request, 8002, 8003, None)
		self.assertTemplateUsed(result, 'admin_consultation_delete_confirm.html')
		
	def test_admin_consultation_delete(self):
		"""
		Testuje poprawna przejscie strony po zatwierdzonym usnieciu konsultacji przez administratora
		Bada przypadki:
		- poprawnego przejscia do odpowiedniej strony po procesie usuniecia
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 11, 'start_minutes': '00', 'end_hour': 13, 'end_minutes': '00',
												'day': 'Niedziela', 'week_type': 'N', 'students_limit': 0, 'room': '111', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_consultation_delete_confirm(post_request, 8002, 8003, None)
		self.assertTemplateUsed(result, 'admin_consultation_delete_confirm.html')
		
	def test_admin_consultation_add(self):
		"""
		Testuje wprowadzenie przykladowej konsultacji do bazy przez administratora.
		Wykorzystuje testowo wprowadzone na start konto tutora o id=8003.
		Bada przypadki:
		- zapytania typu POST (wlasciwego), i odpowiedniego dla niego przejscia na stronie
		- poprawnosci wprowadzenia konsultacji do bazy danych
		- zapytania typu GET (niewlasciwego), i odpowiedniego dla niego przejscia na stronie
		- podania z³ej daty przy wprowadzeniu konsultacji i zachowania systemu w tym przypadku
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 13, 'start_minutes': '00', 'end_hour': 15, 'end_minutes': '00',
												'day': 'Czwartek', 'week_type': 'P', 'students_limit': 0, 'room': '234', 
												'building': 'C-3', 'expiry_date': '06/05/12'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		#self.saveTestTutor(2)
		
		result = admin_consultation_add(post_request, 8003, 8003)
		expected = HttpResponseRedirect(reverse('consultations.views.admin_consultation_list', args=(8003, 8003,)))
		self.assertEqual(expected['Location']==result['Location'], True)
		
		try:
			user = User.objects.get(id=8003)
			tutor = Tutor.objects.get(tutor_ID = user)
			Consultation.objects.get(start_hour = 13, start_minutes = '00', end_hour = 15, 
					end_minutes = '00', day = 'Czwartek', week_type = 'P', tutor_ID = tutor)
		except:
			self.fail("Nie dodano konsultacji poprawnie")
			
		rf = RequestFactory()
		get_request = rf.get('/submit/')
		if not hasattr(get_request, 'user'):
			setattr(get_request, 'user', testUser)
			
		#self.saveTestAssistant(80002)
		
		result = admin_consultation_add(get_request, 8003, 8003)		
		self.assertTemplateUsed(result, "admin_consultation_add.html")
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'start_hour': 13, 'start_minutes': '00', 'end_hour': 15, 'end_minutes': '00',
												'day': 'Wtorek', 'week_type': 'P', 'students_limit': 0, 'room': '234', 
												'building': 'C-3', 'expiry_date': 'BLEBLE'})
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		expected = HttpResponse('Podano b\xc5\x82\xc4\x99dn\xc4\x85 dat\xc4\x99')
		result = admin_consultation_add(post_request, 8003, 8003)
		self.assertEqual(result._get_content(), expected._get_content())
		
	def test_admin_consultation_deleteall_confirm(self):
		"""
		Testuje zdarzenia po potwierdzeniu usuniecia wszystkich konsultacji przez administratora
		Bada przypadki:
		- poprawnego przejscia na strone po usunieciu konsultacji
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_consultation_deleteall_confirm(post_request, 8002, 8003)
		self.assertTemplateUsed(result, 'admin_consultation_deleteall_confirm.html')
		
	def test_admin_consultation_deleteall(self):
		"""
		Testuje zdarzenia po potwierdzeniu usuniecia wszystkich konsultacji przez administratora
		Bada przypadki:
		- poprawnego przejscia na strone po usunieciu konsultacji
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_consultation_deleteall_confirm(post_request, 8002, 8003)
		self.assertTemplateUsed(result, 'admin_consultation_deleteall_confirm.html')
		
	def test_admin_adduser(self):
		"""
		Testuje wprowadzenie usera o id = 9995, loginie 't.est' do bazy przez asystenta. 
		Bada przypadki:
		- zapytania typu POST (wlasciwego), i odpowiedniego dla niego przejscia na stronie
		- poprawnosci wprowadzenia usera do bazy danych
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/', {'login': 't.est', 'tytul': 'dr inz', 'imie': 'adam', 'nazwisko': 'testowy',
												'instytut': 'i6', 'budynek': 'C-3', 'pokoj': '11', 'email': 'a@a.pl', 
												'telefon': '333', 'www': 'www.x.pl'})	
		testUser = MyUser()
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_adduser(post_request, 456654)
		expected = HttpResponseRedirect(reverse('consultations.views.admin_index', args=(456654,)))
		self.assertEqual(expected['Location']==result['Location'], True)
		
		try:
			User.objects.get(login='t.est')
		except:
			self.fail("Nie dodano usera pomyslnie")
			
	def test_admin_export_csv_confirm(self):
		"""
		Testuje prawidlowa generacje strony exportu do pliku csv
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_export_csv_confirm(post_request, 8002)
		self.assertTemplateUsed(result, 'admin_export_csv.html')
		
	def test_admin_import_csv(self):
		"""
		Testuje prawidlowa generacje strony importu do pliku csv
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_import_csv(post_request, 8002)
		self.assertTemplateUsed(result, 'admin_import_csv.html')
		
	def test_admin_export_csv(self):
		"""
		Testuje uruchomienie eskportu do pliku csv przez administratora
		Bada przypadki:
		- prawidlowe przejscie na strone eksportu pliku csv
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = admin_export_csv(post_request, 8001)
		self.assertTemplateUsed(result, 'admin_export_csv.html')
		
	def test_admin_assistant_list(self):
		"""
		Testuje listowanie asysntentow w panelu administratora
		Bada przypadki:
		- prawidlowe przejscie na strone listy asystentow
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = admin_assistant_list(post_request, 8002)
		self.assertTemplateUsed(result, 'admin_assistant_list.html')
		
	def test_admin_assistant_delete_confirm(self):
		"""
		Testuje przejscie strony przy potwierdzeniu usuwania asystenta przez admina
		Bada przypadki:
		- prawidlowe przejscie po potwierdzeniu usuniecia
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = admin_assistant_delete_confirm(post_request, 8002, None)
		self.assertTemplateUsed(result, 'admin_assistant_delete_confirm.html')
		
	def test_admin_assistant_delete(self):
		"""
		Testuje poprawne usuniecie asystenta przez administratora
		Bada przypadki:
		- usuniecie wskazanego asystenta
		- poprawnego przejscia do odpowiedniej strony po usunieciu
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		
		#utworzenie asystenta do kasowania
		self.saveTestAssistant(7775)
		user = User.objects.get(id=7775)
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_assistant_delete(post_request, 7775, user)
		expected = HttpResponseRedirect(reverse('consultations.views.admin_assistant_list', args=(7775,)))
		
		try:
			user = User.objects.get(id=7775)
			self.fail("Nie skasowano poprawnie zamierzonego asystenta")
			assistant = Assistant.objects.get(assistant_id = user)
			self.fail("Nie skasowano poprawnie zamierzonego asystenta")
		except:
			pass
			
	def test_admin_admin_list(self):
		"""
		Testuje listowanie administratorow w panelu administratora
		Bada przypadki:
		- prawidlowe przejscie na strone listy asystentow
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = admin_admin_list(post_request, 8002)
		self.assertTemplateUsed(result, 'admin_admin_list.html')
		
	def test_admin_admin_delete_confirm(self):
		"""
		Testuje przejscie strony przy potwierdzeniu usuwania administratora przez innego administratora
		Bada przypadki:
		- prawidlowe przejscie po potwierdzeniu usuniecia
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
		
		result = admin_admin_delete_confirm(post_request, 8002, None)
		self.assertTemplateUsed(result, 'admin_admin_delete_confirm.html')
		
	def test_admin_admin_delete(self):
		"""
		Testuje poprawne usuniecie asystenta przez administratora
		Bada przypadki:
		- usuniecie wskazanego administratora
		- poprawnego przejscia do odpowiedniej strony po usunieciu
		"""
		rf = RequestFactory()
		post_request = rf.post('/submit/')	
		testUser = MyUser()
		
		#utworzenie administratora do kasowania
		self.saveTestAdministrator(7773)
		user = User.objects.get(id=7773)
		
		if not hasattr(post_request, 'user'):
			setattr(post_request, 'user', testUser)
			
		result = admin_admin_delete(post_request, 7773, user)
		expected = HttpResponseRedirect(reverse('consultations.views.admin_admin_list', args=(7773,)))
		
		try:
			user = User.objects.get(id=7773)
			self.fail("Nie skasowano poprawnie zamierzonego administratora")
			assistant = Administrator.objects.get(administrator_ID = user)
			self.fail("Nie skasowano poprawnie zamierzonego administratora")
		except:
			pass
