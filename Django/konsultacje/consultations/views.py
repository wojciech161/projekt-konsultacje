﻿#-*- coding: utf-8 -*--
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from consultations.models import *
from django.template import Context, loader
from consultations.models import User, Consultation, Localization, InfoBoard, Assistant, Administrator
from django.contrib import auth
from consultations import consultationdata
from consultations import singleconsultationdata
from consultations import uploadfileform
from datetime import date 
from operator import itemgetter, attrgetter 
import string

import cStringIO as StringIO
import csv
import sys
import time
import os

#FUNKCJE POMOCNICZE
def get_data_for_consultations_detail(tutor_id):
	try:
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
	except:
		return HttpResponse("Blad krytyczny")
	tutor_id_from_table = tutor.id
	#pobieramy konsultacje tutora
	try:
		consultations = Consultation.objects.filter(tutor_ID = tutor_id_from_table)
	except:
		consultations = None
	#pobieramy lokalizacje
	consultations_data = []
	for consultation in consultations:
		c_id = consultation.id
		try:
			tutor_of_consultation = consultation.tutor_ID
		except:
			tutor_of_consultation = None
		try:
			consultation_localization = consultation.localization_ID
		except:
			consultation_localization = None
		consult = singleconsultationdata.SingleConsultationsData()
		consult.day = consultation.day
		consult.week_type = consultation.week_type
		consult.hours = "".join("%s.%s-%s.%s")%(consultation.start_hour, consultation.start_minutes, consultation.end_hour, consultation.end_minutes)
		consult.building = consultation_localization.building
		consult.room = consultation_localization.room
		consult.students_limit = consultation.students_limit
		consult.id = consultation.id
		consultations_data.append(consult)
	
	data = {'tutor_id':tutor_id, 'tutor_connsultations':consultations_data}
	return data
	
def time_cmp(x,y):
	if (y == None):
		return 1
	if (x.day == y.day):
		return int(x.start_hour - y.start_hour)
	else:
		days = { u'Poniedziałek' : 1,
				u'Wtorek' : 2,
				u'Środa' : 3,
				u'Czwartek' : 4,
				u'Piątek' : 5,
				u'Sobota' : 6,
				u'Niedziela' : 7,
				}
		x_val = days[x.day]
		y_val = days[y.day]
		return x_val - y_val
	
	
	
def count_consultation_hours(tutor_id):
	tutor = Tutor.objects.get(id = tutor_id)
	consultations = Consultation.objects.filter(tutor_ID = tutor)
	total_consultation_hours = 0
	for con in consultations:
		hours = con.end_hour - con.start_hour
		total_consultation_hours += hours
	return total_consultation_hours
	
def error_file_append(user, error_info, error_place):
	reload(sys)
	sys.setdefaultencoding('utf8')
	try:
		errorfile = open("/home/kons/logs/errors", "a+")
	except:
		return "Nie mogę dodać błędu!"
	else:
		current_date = str(date.today())
		errorfile.write(current_date)
		errorfile.write(" Użytkownik: ")
		errorfile.write(user)
		errorfile.write(" Zgłoszone z miejsca: ")
		errorfile.write(error_place)
		errorfile.write(" Błąd: ")
		errorfile.write(error_info)
		errorfile.write("\n")
		errorfile.close()
		return "Błąd został dodany"
		
def log_file_append(user, log):
	reload(sys)
	sys.setdefaultencoding('utf8')
	try:
		errorfile = open("/home/kons/logs/logs", "a+")
	except:
		pass
	else:
		current_date = str(date.today())
		errorfile.write(current_date)
		errorfile.write(" Użytkownik: ")
		errorfile.write(user)
		errorfile.write(" ")
		errorfile.write(log)
		errorfile.write("\n")
		errorfile.close()

def insert(L_tutor, list, next_letter, slot):
	place = 0
	list.pop(slot)
	for tutor in list:
		if (tutor.surname[:1] >= next_letter and tutor.surname[:1] != 'Ą' and tutor.surname[:1] != 'Ę' and tutor.surname[:1] != 'Ć' and tutor.surname[:1] != 'Ł' and tutor.surname[:1] != 'Ń' and tutor.surname[:1] != 'Ó' and tutor.surname[:1] != 'Ś'):
			list.insert(place, L_tutor)
			
			break
		place = place + 1	
	
	return list
	

			
def sort_tutors(tutor_list):
	reload(sys)
	sys.setdefaultencoding('utf8')
	list = sorted (tutor_list,  key=attrgetter('surname'))
	i = len(list)
	i = i-1
	while (i >= 0 and list[i].surname[:1] >= 'Z'):
		if (list[i].surname[:1] == 'Ą'):
			list = insert(list[i], list, 'B', i)
		else:	
			if (list[i].surname[:1] == 'Ę'):
				list = insert(list[i], list, 'F', i)
			else:	
				if (list[i].surname[:1] == 'Ć'):
					list = insert(list[i], list, 'D', i)
				else:	
					if (list[i].surname[:1] == 'Ł'):
						list = insert(list[i], list, 'M', i)
					else:	
						if (list[i].surname[:1] == 'Ń'):
							list = insert(list[i], list, 'O', i)
						else:	
							if (list[i].surname[:1] == 'Ó'):
								list = insert(list[i], list, 'P', i)
							else:	
								if (list[i].surname[:1] == 'Ś'):
									list = insert(list[i], list, 'T', i)
								else:
									break
		
		
	return list
		
##############KONIEC FUNKCJI POMOCNICZYCH

def consultation_index(request):
	#Pobieramy wszystkich wykladowcow
	try:
		tutors_list = Tutor.objects.all()
	except:
		tutor_list = None
	
		
	consultations_data = []
	for tutor in tutors_list:
		t_id = tutor.id
		try:
			tutor_consultations = Consultation.objects.filter(tutor_ID = t_id)
		except:
			tutor_consultations = None
		try:
			tutor_localizations = Localization.objects.get(id = tutor.localization_ID_id)
		except:
			tutor_localizations = None
		try:
			tutor_info = InfoBoard.objects.get(tutor_id = t_id)
		except:
			tutor_info = InfoBoard()
			tutor_info.message = ""
		consult = consultationdata.ConsultationsData()
		consult.name = tutor.name
		consult.surname = tutor.surname
		consult.www = "\"http://" + tutor.www + "\""
		consult.title = tutor.degree
		try:
			consult.localization = "".join("%s, %s")%(tutor_localizations.building, tutor_localizations.room)
		except:
			pass
		consult.phone = tutor.phone[8:]
		today = date.today()
		consult.consultations = []
		raw_consultations = []
		
		today = date.today();
		
		for con in tutor_consultations:
			try:
				con_localization = Localization.objects.get(id = con.localization_ID_id)
			except:
				pass
			single_con = singleconsultationdata.SingleConsultationsData()
			single_con.day = con.day
			single_con.start_hour = con.start_hour
			single_con.week_type = con.week_type
			if (single_con.week_type == 'A'):
				single_con.week_type = " "
			single_con.end_hour = con.end_hour
			single_con.expiry_date = con.expiry_date
			single_con.start_minutes = con.start_minutes
			single_con.end_minutes = con.end_minutes
			single_con.building = con_localization.building
			single_con.room = con_localization.room
			raw_consultations.append(single_con)
		raw_consultations = sorted(raw_consultations, cmp=time_cmp)
		
		for con in raw_consultations:
			strcon = "".join("%s %s %s:%s-%s:%s %s %s")%(con.day, con.week_type, con.start_hour,con.start_minutes, con.end_hour,con.end_minutes, con_localization.room, con_localization.building )
			if (today > con.expiry_date):
				strcon = "".join("<font color=\"#808080\"> %s %s %s:%s-%s:%s %s %s (Nieaktualne) </font>")%(con.day, con.week_type, con.start_hour,con.start_minutes, con.end_hour,con.end_minutes, con_localization.room, con_localization.building )
			if (strcon ==""):
				strcon = " "
			consult.consultations.append(strcon)
		
		consult.info = tutor_info.message
		if (len(consult.info) > 100):
			consult.info_short = consult.info[:70] + u"... Najedź by wyświetlić całość"
		else:
			consult.info_short = consult.info
		
		consultations_data.append(consult)
		consult = None
	consultations_data = sort_tutors(consultations_data)
	t = loader.get_template('index.html')
	c = Context({'consultations_data' : consultations_data, })
	return HttpResponse(t.render(c))
	
def tutors_index(request):
	tutors_list = Tutor.objects.all().order_by('name')[:5]
	t = loader.get_template('index.html')
	c = Context({'tutors_list': tutors_list,})
	return HttpResponse(t.render(c))
	

def tutor_index(request, tutor_id):
	if request.user.is_authenticated():
		return render_to_response('tutor_index.html', {'tutor_id':tutor_id})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
	
def tutor_detail(request, tutor_id):
	reload(sys)
	sys.setdefaultencoding('utf8')
	
	if request.user.is_authenticated():
		
		status = ""
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		user_name = tutor.name
		user_surname = tutor.surname
		tutor_id_from_table = tutor.id
		try:
			localization = Localization.objects.get(id = tutor.localization_ID_id)
		except:
			localization = None
			
		if request.POST:
			#zbiermay dane
			try:
				title = request.POST.get('tytul')
				name = request.POST.get('imie')
				surname = request.POST.get('nazwisko')
				building = request.POST.get('budynek')
				room = request.POST.get('pokoj')
				phone = request.POST.get('telefon')
				mail = request.POST.get('email')
				www = request.POST.get('www')
				
				#zapisujemy zmiany w bazie
				tutor.degree = title
				tutor.name = name
				tutor.surname = surname
				tutor.phone = phone
				tutor.email = mail
				tutor.www = www
				tutor.save()
				
				localization.room = room
				localization.building = building
				localization.save()
				status = "Dane zostały zmienione"
				try:
					log_file_append(tutor.tutor_ID.login, "zmienił swoje dane")
				except:
					pass
				
			except:
				status = "Błąd: Nie mogę zmienić danych"
		return render_to_response('tutor_detail.html', {'tutor_id':tutor_id, 'localization':localization, 'tutor':tutor, 'status':status, 'user_name':user_name, 'user_surname':user_surname}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
	
def consultations_detail(request, tutor_id):
	if request.user.is_authenticated():
		#pobieramy tutora
		try:
			tutor = Tutor.objects.get(tutor_ID = tutor_id)
		except:
			return HttpResponse("Blad krytyczny")
		tutor_id_from_table = tutor.id
		user_name = tutor.name
		user_surname = tutor.surname
		#pobieramy konsultacje tutora
		try:
			consultations = Consultation.objects.filter(tutor_ID = tutor_id_from_table)
		except:
			consultations = None
		#pobieramy lokalizacje
		consultations_data = []
		for consultation in consultations:
			c_id = consultation.id
			try:
				tutor_of_consultation = consultation.tutor_ID
			except:
				tutor_of_consultation = None
			try:
				consultation_localization = consultation.localization_ID
			except:
				consultation_localization = None
			consult = singleconsultationdata.SingleConsultationsData()
			consult.day = consultation.day
			consult.week_type = consultation.week_type
			consult.start_hour = consultation.start_hour
			consult.hours = "".join("%s.%s-%s.%s")%(consultation.start_hour, consultation.start_minutes, consultation.end_hour, consultation.end_minutes)
			consult.building = consultation_localization.building
			consult.room = consultation_localization.room
			if (consultation.students_limit == 0):
				consult.students_limit = "-"
			else:
				consult.students_limit =consultation.students_limit
			consult.id = consultation.id
			today = date.today();
			if(today>consultation.expiry_date):
				consult.expiry = "expiry"
			else:
				consult.expiry = "not_expiry"
			consult.expiry_date = consultation.expiry_date
			consultations_data.append(consult)
			
		consultations_data = sorted (consultations_data,  cmp=time_cmp)	
		return render_to_response('consultations_detail.html', {'tutor_id':tutor_id, 'tutor_connsultations':consultations_data, 'user_name':user_name, 'user_surname':user_surname}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))

def edit_consultation(request, tutor_id, consultation_id):
	if request.user.is_authenticated():
		try:
			tutor = Tutor.objects.get(tutor_ID = tutor_id)
			user_name = tutor.name
			user_surname = tutor.surname
		except:
			user_name = ""
			user_surname = ""
		
		try:
			consultation = Consultation.objects.get(id = consultation_id)
		except:
			return HttpResponse("Nie istnieje taka konsultacja")
		else:
			localization = consultation.localization_ID
			start_hour = consultation.start_hour
			start_minutes = consultation.start_minutes
			end_hour = consultation.end_hour
			end_minutes = consultation.end_minutes
			day = consultation.day
			week_type = consultation.week_type
			students_limit = consultation.students_limit
			building = localization.building
			room = localization.room
			new_localization = Localization()
			try:
				expiry_year = consultation.expiry_date.year
				expiry_month = consultation.expiry_date.month
				expiry_day = consultation.expiry_date.day
				expiry_date ="".join("%s/%s/%s")%(expiry_day, expiry_month, expiry_year) 
			except:
				expiry_date = ""
			
			
			if request.POST:
				start_hour = request.POST.get('start_hour')
				consultation.start_hour = start_hour
				
				start_minutes = request.POST.get('start_minutes')
				consultation.start_minutes = start_minutes
				
				end_hour = request.POST.get('end_hour')
				consultation.end_hour = end_hour
				
				end_minutes = request.POST.get('end_minutes')
				consultation.end_minutes = end_minutes
				
				day = request.POST.get('day')
				consultation.day = day
				
				week_type = request.POST.get('week_type')
				consultation.week_type = request.POST.get('week_type')
				
				students_limit = request.POST.get('students_limit')
				consultation.students_limit = request.POST.get('students_limit')
				if (consultation.students_limit == ""):
					consultation.students_limit = 0
				
				building = request.POST.get('building')
				
				room = request.POST.get('room')

				try:
					new_localization = Localization.objects.get(room = room, building = building)
					consultation.localization_ID = new_localization
				except:
					new_localization.room = room
					new_localization.building = building
					new_localization.save()
					consultation.localization_ID = new_localization
					
				expiry_date = request.POST.get('expiry_date')
				expiry_date_splitted = expiry_date.split("/")
				try:
					new_expiry_date = date(	int(expiry_date_splitted[2]), int(expiry_date_splitted[1]), int(expiry_date_splitted[0]))
					consultation.expiry_date = new_expiry_date
				except:
					return HttpResponse("Podano złą datę")
				
				try:
					consultation.save() 
				except:
					return HttpResponse("Nie udało się zapisać zmian - sprawdź poprawność pól")
				
				try:
					log_file_append(tutor.tutor_ID.login, "edytował swoje konsultacje")
				except:
					pass
				
				#data = get_data_for_consultations_detail(tutor_id)#pobranie danych do obsługi strony consultations_detail
				#return render_to_response('consultations_detail.html', data, context_instance = RequestContext(request))#wyświetlenie consultations_detail jeśli udało się zapisać nową konsultację	
				return HttpResponseRedirect(reverse('consultations.views.consultations_detail', args=(tutor_id,)))
				
		
		
			date_used = []
			empty_date = ""
			date_dir = "/home/kons/data"
			date_filename = "date.txt"
			filepath = os.path.join(date_dir, date_filename)
			dates_read = open(filepath, "rb")
			for lines in dates_read:
				date_used.append(lines)
			dates_read.close()
			while (len(date_used)<6):
				date_used.append(empty_date)
			
			
			return render_to_response("edit_consultation.html", {'consultation_id' : consultation_id, 'tutor_id' : tutor_id, 'start_hour' : start_hour,'start_minutes' : start_minutes, 'end_hour' : end_hour, 'end_minutes' : end_minutes, 'day' : day, 'week_type' : week_type, 'students_limit' : students_limit, 'building' : building, 'room' : room, 'expiry_date' : expiry_date, 'user_name':user_name, 'user_surname':user_surname, 'date_name1':date_used[0], 'date_value1':date_used[1], 'date_name2':date_used[2], 'date_value2':date_used[3], 'date_name3':date_used[4], 'date_value3':date_used[5] }, context_instance = RequestContext(request))
				
	else:
		return render_to_response(reverse('consultations.views.authorization'))

def delete_consultation(request, tutor_id, consultation_id):
	try:
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		log_file_append(tutor.tutor_ID.login, "usunął swoją konsultację")
	except:
		pass
	
	try:
		consultation = Consultation.objects.get(id = consultation_id)
		consultation.delete()
		consultations_detail(request, tutor_id)
		
		data = get_data_for_consultations_detail(tutor_id)#pobranie danych do obsługi strony consultations_detail
		return render_to_response('consultations_detail.html', data, context_instance = RequestContext(request))#wyświetlenie consultations_detail
				#jeśli udało się zapisać nową konsultację	
	except:
		return HttpResponse ("Blad")
	
def add_consultation(request, tutor_id):
	
	date_used = []
	empty_date = ""
	date_dir = "/home/kons/data"
	date_filename = "date.txt"
	filepath = os.path.join(date_dir, date_filename)
	dates_read = open(filepath, "rb")
	for lines in dates_read:
		date_used.append(lines)
	dates_read.close()
	while (len(date_used)<6):
		date_used.append(empty_date)
	
	if request.user.is_authenticated():
		
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		new_start_hour = ""
		new_start_minutes = ""
		new_end_minutes = ""
		new_end_hour = ""
		new_day = ""
		new_week_type = ""
		new_students_limit = ""
		new_room = tutor.localization_ID.room
		new_building = tutor.localization_ID.building
		new_expiry_year = ""
		new_expiry_month = ""
		new_expiry_day = ""
		new_expiry_date = ""
		
		#print new_room
		
		if request.POST:
			
			new_start_hour = request.POST.get('start_hour')
			#print new_start_hour
			new_start_minutes = request.POST.get('start_minutes')
			#print new_start_minutes
			
			new_end_hour = request.POST.get('end_hour')
			#print new_end_hour
			new_end_minutes = request.POST.get('end_minutes')
			#print new_end_minutes
			
			new_day = request.POST.get('day')
			#print new_day
			new_week_type = request.POST.get('week_type')
			#print new_week_type
			new_students_limit = request.POST.get('students_limit')
			if (new_students_limit == ""):
				new_students_limit = 0
			new_room = request.POST.get('room')
			new_building = request.POST.get('building')
			try:
				new_localization = Localization.objects.get(room = new_room, building = new_building)
			except:
				new_localization = Localization()
				new_localization.room = new_room
				new_localization.building = new_building
				new_localization.save()
			
			
			new_expiry = request.POST.get('expiry_date')
			new_expiry_splitted = new_expiry.split('/')
			if (len(new_expiry_splitted) != 3):
				new_expiry = date_used[1]
				new_expiry_splitted = new_expiry.split('/')
			new_expiry_date = date(	int(new_expiry_splitted[2]), int(new_expiry_splitted[1]), int(new_expiry_splitted[0]))
			
			if (new_start_hour != "" and new_start_minutes != "" and new_end_hour != "" and new_end_minutes != "" and new_day != "" and new_week_type != "" and new_localization != ""):
				try:
					consultation = Consultation(tutor_ID = tutor, start_hour = new_start_hour, start_minutes = new_start_minutes, end_hour = new_end_hour, 
					end_minutes = new_end_minutes, day = new_day, week_type = new_week_type, localization_ID = new_localization, expiry_date = new_expiry_date)
				except:
					return HttpResponse("Nie mozna dodac konsultacji")
				if(new_students_limit != None):
					try:
						consultation.students_limit = new_students_limit
					except:
						pass
				try:
					consultation.save()
				except:
					return HttpResponse("Nie udało się dodac konsultacji, sprawdź poprawność pól")
				
				try:
					log_file_append(tutor.tutor_ID.login, "dodał konsultację")
				except:
					pass
				
				return HttpResponseRedirect(reverse('consultations.views.consultations_detail', args=( tutor_id,)))
							
			else:
				return HttpResponse("Nie mozna dodac konsultacji")
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		user_name = tutor.name
		user_surname = tutor.surname
		
		date_used = []
		empty_date = ""
		date_dir = "/home/kons/data"
		date_filename = "date.txt"
		filepath = os.path.join(date_dir, date_filename)
		dates_read = open(filepath, "rb")
		for lines in dates_read:
			date_used.append(lines)
		dates_read.close()
		while (len(date_used)<6):
			date_used.append(empty_date)
			
		return render_to_response("add_consultation.html", { 'user_id':tutor_id, 'tutor_id' : tutor_id, 'start_hour' : new_start_hour, 'start_minutes' : new_start_minutes,  'end_hour' : new_end_hour, 'end_minutes' : new_end_minutes, 'day' : new_day, 'week_type' : new_week_type, 'students_limit' : new_students_limit, 'expiry_year' : new_expiry_year, 'expiry_month' : new_expiry_month, 'expiry_day' : new_expiry_day, 'building' : new_building, 'room' : new_room, 'user_name':user_name, 'user_surname':user_surname, 'date_name1':date_used[0], 'date_value1':date_used[1], 'date_name2':date_used[2], 'date_value2':date_used[3], 'date_name3':date_used[4], 'date_value3':date_used[5]}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))
		
def tutor_export_html(request, tutor_id):
	import codecs
	from django.core.servers.basehttp import FileWrapper
	if request.user.is_authenticated():
		
		
		
		html_dir = '/home/kons/html'
		filename = 'konsultacje.html'
		filepath = os.path.join(html_dir, filename)
		before_filepath = '/home/kons/repo/projekt-konsultacje/Django/przed.txt'
		html = open(filepath, "w")
		before = open(before_filepath, "r")
		i = 0
		for lines in before:
			html.write(lines)
			if (lines.count("eeeeee") == 1):
				try:
					tutors_list = Tutor.objects.all()
				except:
					tutor_list = None
				
					
				consultations_data = []
				for tutor in tutors_list:
					t_id = tutor.id
					try:
						tutor_consultations = Consultation.objects.filter(tutor_ID = t_id)
					except:
						tutor_consultations = None
					try:
						tutor_localizations = Localization.objects.get(id = tutor.localization_ID_id)
					except:
						tutor_localizations = None
					try:
						tutor_info = InfoBoard.objects.get(tutor_id = t_id)
					except:
						tutor_info = InfoBoard()
						tutor_info.message = ""
					consult = consultationdata.ConsultationsData()
					consult.name = tutor.name
					consult.surname = tutor.surname
					consult.www = "\"http://" + tutor.www + "\""
					consult.title = tutor.degree
					try:
						consult.localization = "".join("%s, %s")%(tutor_localizations.building, tutor_localizations.room)
					except:
						pass
					consult.phone = tutor.phone
					today = date.today()
					consult.consultations = []
					raw_consultations = []
					for con in tutor_consultations:
						try:
							con_localization = Localization.objects.get(id = con.localization_ID_id)
						except:
							pass
						single_con = singleconsultationdata.SingleConsultationsData()
						single_con.day = con.day
						single_con.start_hour = con.start_hour
						single_con.week_type = con.week_type
						if (single_con.week_type == 'A'):
							single_con.week_type = " "
						single_con.end_hour = con.end_hour
						single_con.expiry_date = con.expiry_date
						single_con.start_minutes = con.start_minutes
						single_con.end_minutes = con.end_minutes
						single_con.building = con_localization.building
						single_con.room = con_localization.room
						raw_consultations.append(single_con)
					raw_consultations = sorted(raw_consultations, cmp=time_cmp)
					
					for con in raw_consultations:
						strcon = "".join("%s %s %s.%s-%s.%s")%(con.day, con.week_type, con.start_hour,con.start_minutes, con.end_hour,con.end_minutes )
						if (today>con.expiry_date):
							strcon = ""
						else:
							strcon = "".join("%s %s %s.%s-%s.%s [%s %s] ;")%(con.day, con.week_type, con.start_hour, con.start_minutes, con.end_hour, con.end_minutes, con_localization.room, con_localization.building)
						if (strcon ==""):
							strcon = " "
						consult.consultations.append(strcon)
					
					consult.info = tutor_info.message
					if (len(consult.info) > 100):
						consult.info_short = consult.info[:70]
					else:
						consult.info_short = consult.info
					consultations_data.append(consult)
					consult = None
				consultations_data = sorted (consultations_data,  key=attrgetter('surname'))
				
				check = 1
				i = 0
				for con in consultations_data:
					if (check == 1):
						check = 2
					else:
						if (i%2 == 0):
							html.write("<TR>")
						else:
							html.write("<TR style=\"BACKGROUND-COLOR: rgb(238,238,238)\" mce_style=\"background-color: #eeeeee;\">")
						i = i+1
					html.write("<TD>")
					surname = con.surname
					surname = surname.encode('utf8')
					html.write(surname)
					html.write("</TD>")
					html.write("<TD>")
					name = con.name
					name = name.encode('utf8')
					html.write(name)
					html.write("</TD>")
					html.write("<TD>")
					title = con.title
					title = title.encode('utf8')
					html.write(title)
					html.write("</TD>")
					html.write("<TD>")
					localization = con.localization
					localization = localization.encode('utf8')
					html.write(localization)
					html.write("</TD>")
					html.write("<TD>")
					phone = con.phone
					phone = phone[8:]
					phone = phone.encode('utf8')
					html.write(phone)
					html.write("</TD>")
					html.write("<TD>")
					for single_con in con.consultations:
						single_con = single_con.encode('utf8')
						html.write(single_con)
						html.write("<br>")
					html.write("</TD>")
					html.write("<TD title = \" ")
					info = con.info
					info = info.encode('utf8')
					html.write(info)
					html.write(" \" >")
					info_short = con.info_short
					info_short = info_short.encode('utf8')
					html.write(info_short)
					if (info_short != info):
						html.write("<span style =\"color:blue;text-decoration:underline\"> ... </span>")
					html.write("</TD>")
					html.write("</TR>")
			
		
		before.close()
		html.close()
		filepath = "/home/kons/html/konsultacje.html"
		htmlfile = open(filepath, "r")
		filename = "konsultacje.html"
		wrapper = FileWrapper(htmlfile)
		
		response = HttpResponse(wrapper, mimetype='application/force-download')
		response['Content-Disposition'] = 'attachment; filename=%s' % filename
		response['Content-Length'] = os.path.getsize(filepath)
		return response
		#return HttpResponseRedirect(reverse('consultations.views.consultations_detail', args=(tutor_id,)))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_export_html(request, user_id):
	import codecs
	from django.core.servers.basehttp import FileWrapper
	if request.user.is_authenticated():
		
		
		
		html_dir = '/home/kons/html'
		filename = 'konsultacje.html'
		filepath = os.path.join(html_dir, filename)
		before_filepath = '/home/kons/repo/projekt-konsultacje/Django/przed.txt'
		html = open(filepath, "w")
		before = open(before_filepath, "r")
		i = 0
		for lines in before:
			html.write(lines)
			if (lines.count("eeeeee") == 1):
				try:
					tutors_list = Tutor.objects.all()
				except:
					tutor_list = None
				
					
				consultations_data = []
				for tutor in tutors_list:
					t_id = tutor.id
					try:
						tutor_consultations = Consultation.objects.filter(tutor_ID = t_id)
					except:
						tutor_consultations = None
					try:
						tutor_localizations = Localization.objects.get(id = tutor.localization_ID_id)
					except:
						tutor_localizations = None
					try:
						tutor_info = InfoBoard.objects.get(tutor_id = t_id)
					except:
						tutor_info = InfoBoard()
						tutor_info.message = ""
					consult = consultationdata.ConsultationsData()
					consult.name = tutor.name
					consult.surname = tutor.surname
					consult.www = "\"http://" + tutor.www + "\""
					consult.title = tutor.degree
					try:
						consult.localization = "".join("%s, %s")%(tutor_localizations.building, tutor_localizations.room)
					except:
						pass
					consult.phone = tutor.phone
					today = date.today()
					consult.consultations = []
					raw_consultations = []
					for con in tutor_consultations:
						try:
							con_localization = Localization.objects.get(id = con.localization_ID_id)
						except:
							pass
						single_con = singleconsultationdata.SingleConsultationsData()
						single_con.day = con.day
						single_con.start_hour = con.start_hour
						single_con.week_type = con.week_type
						if (single_con.week_type == 'A'):
							single_con.week_type = " "
						single_con.end_hour = con.end_hour
						single_con.expiry_date = con.expiry_date
						single_con.start_minutes = con.start_minutes
						single_con.end_minutes = con.end_minutes
						single_con.building = con_localization.building
						single_con.room = con_localization.room
						raw_consultations.append(single_con)
					raw_consultations = sorted(raw_consultations, cmp=time_cmp)
					
					for con in raw_consultations:
						strcon = "".join("%s %s %s.%s-%s.%s")%(con.day, con.week_type, con.start_hour,con.start_minutes, con.end_hour,con.end_minutes )
						if (today>con.expiry_date):
							strcon = ""
						else:
							strcon = "".join("%s %s %s.%s-%s.%s [%s %s] ;")%(con.day, con.week_type, con.start_hour, con.start_minutes, con.end_hour, con.end_minutes, con_localization.room, con_localization.building)
						if (strcon ==""):
							strcon = ""
						consult.consultations.append(strcon)
					
					consult.info = tutor_info.message
					if (len(consult.info) > 100):
						consult.info_short = consult.info[:70]
					else:
						consult.info_short = consult.info
					consultations_data.append(consult)
					consult = None
				consultations_data = sorted (consultations_data,  key=attrgetter('surname'))
				
				check = 1
				i = 0
				for con in consultations_data:
					if (check == 1):
						check = 2
					else:
						if (i%2 == 0):
							html.write("<TR>")
						else:
							html.write("<TR style=\"BACKGROUND-COLOR: rgb(238,238,238)\" mce_style=\"background-color: #eeeeee;\">")
						i = i+1
					html.write("<TD>")
					surname = con.surname
					surname = surname.encode('utf8')
					html.write(surname)
					html.write("</TD>")
					html.write("<TD>")
					name = con.name
					name = name.encode('utf8')
					html.write(name)
					html.write("</TD>")
					html.write("<TD>")
					title = con.title
					title = title.encode('utf8')
					html.write(title)
					html.write("</TD>")
					html.write("<TD>")
					localization = con.localization
					localization = localization.encode('utf8')
					html.write(localization)
					html.write("</TD>")
					html.write("<TD>")
					phone = con.phone
					phone = phone[8:]
					phone = phone.encode('utf8')
					html.write(phone)
					html.write("</TD>")
					html.write("<TD>")
					for single_con in con.consultations:
						single_con = single_con.encode('utf8')
						html.write(single_con)
						html.write("<br>")
					html.write("</TD>")
					html.write("<TD title = \" ")
					info = con.info
					info = info.encode('utf8')
					html.write(info)
					html.write(" \" >s")
					info_short = con.info_short
					info_short = info_short.encode('utf8')
					html.write(info_short)
					if (info_short != info):
						html.write("<span style =\"color:blue;text-decoration:underline\"> ... </span>")
					html.write("</TD>")
					html.write("</TR>")
			
		
		before.close()
		html.close()
		filepath = "/home/kons/html/konsultacje.html"
		htmlfile = open(filepath, "r")
		filename = "konsultacje.html"
		wrapper = FileWrapper(htmlfile)
		
		response = HttpResponse(wrapper, mimetype='application/force-download')
		response['Content-Disposition'] = 'attachment; filename=%s' % filename
		response['Content-Length'] = os.path.getsize(filepath)
		return response
		#return HttpResponseRedirect(reverse('consultations.views.assistant_index', args=(user_id,)))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
		
def admin_export_html(request, user_id):
	import codecs
	from django.core.servers.basehttp import FileWrapper
	if request.user.is_authenticated():
		
		
		html_dir = '/home/kons/html'
		filename = 'konsultacje.html'
		filepath = os.path.join(html_dir, filename)
		before_filepath = '/home/kons/repo/projekt-konsultacje/Django/przed.txt'
		
		html = open(filepath, "w")
		before = open(before_filepath, "r")
		i = 0
		for lines in before:
			html.write(lines)
			if (lines.count("eeeeee") == 1):
				try:
					tutors_list = Tutor.objects.all()
				except:
					tutor_list = None
				
					
				consultations_data = []
				for tutor in tutors_list:
					t_id = tutor.id
					try:
						tutor_consultations = Consultation.objects.filter(tutor_ID = t_id)
					except:
						tutor_consultations = None
					try:
						tutor_localizations = Localization.objects.get(id = tutor.localization_ID_id)
					except:
						tutor_localizations = None
					try:
						tutor_info = InfoBoard.objects.get(tutor_id = t_id)
					except:
						tutor_info = InfoBoard()
						tutor_info.message = ""
					consult = consultationdata.ConsultationsData()
					consult.name = tutor.name
					consult.surname = tutor.surname
					consult.www = "\"http://" + tutor.www + "\""
					consult.title = tutor.degree
					try:
						consult.localization = "".join("%s, %s")%(tutor_localizations.building, tutor_localizations.room)
					except:
						pass
					consult.phone = tutor.phone
					today = date.today()
					consult.consultations = []
					raw_consultations = []
					for con in tutor_consultations:
						try:
							con_localization = Localization.objects.get(id = con.localization_ID_id)
						except:
							pass
						single_con = singleconsultationdata.SingleConsultationsData()
						single_con.day = con.day
						single_con.start_hour = con.start_hour
						single_con.week_type = con.week_type
						if (single_con.week_type == 'A'):
							single_con.week_type = " "
						single_con.end_hour = con.end_hour
						single_con.expiry_date = con.expiry_date
						single_con.start_minutes = con.start_minutes
						single_con.end_minutes = con.end_minutes
						single_con.building = con_localization.building
						single_con.room = con_localization.room
						raw_consultations.append(single_con)
					raw_consultations = sorted(raw_consultations, cmp=time_cmp)
					
					for con in raw_consultations:
						strcon = "".join("%s %s %s.%s-%s.%s")%(con.day, con.week_type, con.start_hour,con.start_minutes, con.end_hour,con.end_minutes )
						if (today>con.expiry_date):
							strcon = ""
						else:
							strcon = "".join("%s %s %s.%s-%s.%s [%s %s] ;")%(con.day, con.week_type, con.start_hour, con.start_minutes, con.end_hour, con.end_minutes, con_localization.room, con_localization.building)
						if (strcon ==""):
							strcon = ""
						consult.consultations.append(strcon)
					
					consult.info = tutor_info.message
					if (len(consult.info) > 100):
						consult.info_short = consult.info[:70] 
					else:
						consult.info_short = consult.info
					consultations_data.append(consult)
					consult = None
				consultations_data = sorted (consultations_data,  key=attrgetter('surname'))
				
				check = 1
				i = 0
				for con in consultations_data:
					if (check == 1):
						check = 2
					else:
						if (i%2 == 0):
							html.write("<TR>")
						else:
							html.write("<TR style=\"BACKGROUND-COLOR: rgb(238,238,238)\" mce_style=\"background-color: #eeeeee;\">")
						i = i+1
					html.write("<TD>")
					surname = con.surname
					surname = surname.encode('utf8')
					html.write(surname)
					html.write("</TD>")
					html.write("<TD>")
					name = con.name
					name = name.encode('utf8')
					html.write(name)
					html.write("</TD>")
					html.write("<TD>")
					title = con.title
					title = title.encode('utf8')
					html.write(title)
					html.write("</TD>")
					html.write("<TD>")
					localization = con.localization
					localization = localization.encode('utf8')
					html.write(localization)
					html.write("</TD>")
					html.write("<TD>")
					phone = con.phone
					phone = phone[8:]
					phone = phone.encode('utf8')
					html.write(phone)
					html.write("</TD>")
					html.write("<TD>")
					for single_con in con.consultations:
						single_con = single_con.encode('utf8')
						html.write(single_con)
						html.write("<br>")
					html.write("</TD>")
					html.write("<TD title = \" ")
					info = con.info
					info = info.encode('utf8') 
					html.write(info)
					html.write(" \" >")
					info_short = con.info_short
					info_short = info_short.encode('utf8')
					html.write(info_short)
					if (info_short != info):
						html.write("<span style =\"color:blue;text-decoration:underline\"> ... </span>")
					html.write("</TD>")
					html.write("</TR>")
			
		before.close()
		html.close()
		filepath = "/home/kons/html/konsultacje.html"
		htmlfile = open(filepath, "r")
		filename = "konsultacje.html"
		wrapper = FileWrapper(htmlfile)
		
		response = HttpResponse(wrapper, mimetype='application/force-download')
		response['Content-Disposition'] = 'attachment; filename=%s' % filename
		response['Content-Length'] = os.path.getsize(filepath)
		return response
		#return HttpResponseRedirect(reverse('consultations.views.admin_index', args=(user_id,)))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))

def admin_choose_panel(request, user_id):
	if request.user.is_authenticated():
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname	
		return render_to_response('admin_choose_panel.html', {'user_id':user_id, 'user_name':user_name, 'user_surname':user_surname})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))

def authorization(request):	
	state = "Proszę się zalogować"
	username = password = ''
	user_is_tutor = False
	user_is_assistant = False
	user_is_admin = False
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				try:
					user_from_table = User.objects.get(login = username)
				except:
					state = """Użytkownik nie posiada konta w bazie danych.
								Proszę skontaktować się z Administratorem"""
				else:
					try:
						tutor_from_table = Tutor.objects.get(tutor_ID = user_from_table.id)
					except:
						user_is_tutor = False
						state = "Użytkownik nie jest wykładowcą"
					else:
						user_is_tutor = True
					
					try:
						assistant_from_table = Assistant.objects.get(assistant_ID = user_from_table.id)
					except:
						user_is_assistant = False
						state = "Uzytkownik nie jest asystentem"
					else:
						user_is_assistant = True
						
					try:
						admin_from_table = Administrator.objects.get(administrator_ID = user_from_table.id)
					except:
						user_is_admin = False
						state = "Użytkownik nie jest administratorem"
					else:
						user_is_admin = True
						
					if user_is_tutor and not(user_is_assistant) and not(user_is_admin):
						login(request, user)
						state = "Zalogowano"
						return HttpResponseRedirect(reverse('consultations.views.consultations_detail', args=(user_from_table.id,)))
					elif not(user_is_tutor) and user_is_assistant and not(user_is_admin):
						login(request, user)
						state = "Zalogowano"
						return HttpResponseRedirect(reverse('consultations.views.assistant_index', args=(user_from_table.id,)))
					elif user_is_tutor and user_is_assistant and not(user_is_admin):
						login(request, user)
						state = "Zalogowano"
						return HttpResponseRedirect(reverse('consultations.views.choose_panel', args=(user_from_table.id,)))
					elif user_is_admin and not(user_is_tutor):
						login(request, user)
						state = "Zalogowano"
						return HttpResponseRedirect(reverse('consultations.views.admin_index', args=(user_from_table.id,)))
					elif user_is_admin and user_is_tutor:
						login(request, user)
						state = "Zalogowano"
						return HttpResponseRedirect(reverse('consultations.views.admin_choose_panel', args=(user_from_table.id,)))
					else:
						state = "Błąd logowania!"
			else:
				state = "Twoje konto nie zostalo jeszcze aktywowane"
		else:
			state = "Login lub hasło nieprawidłowe"
		
	return render_to_response('logging.html', {'state':state, 'username':username}, context_instance = RequestContext(request))
	
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('consultations.views.consultation_index'))
	
def edit_infoboard(request, tutor_id):
	if request.user.is_authenticated():
		status = ""
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		user_name = tutor.name
		user_surname = tutor.surname	
		tutor_id_from_table = tutor.id
		try:
			infoboard = InfoBoard.objects.get(tutor_id = tutor_id_from_table)
			
		except:
			infoboard = None
		
		if (len(infoboard.message) > 100):
			infoboard_short = infoboard.message[:70] + u"... Najedź by wyświetlić całość"
		else:
			infoboard_short = infoboard.message
		if (infoboard != None):
			if (infoboard.message == ""):
				infoboard.message ="\nDodano:" +  date.today().isoformat()
		#print infoboard.message
		if request.POST:
			#zbieramy dane
			try:
				info = request.POST.get('Informacja')
				#zapisujemy zmiany w bazie
				infoboard.message = info
				
				infoboard.save()
				infoboard_short = infoboard.message
				if (len(infoboard.message) > 100):
					infoboard_short = infoboard.message[:70] + u"... Najedź by wyświetlić całość"
				if (infoboard != None):
					if (infoboard.message == ""):
						infoboard.message ="\nDodano:" +  date.today().isoformat()	
				status = "Dane zostały zmienione"
				
				try:
					log_file_append(tutor.tutor_ID.login, "zmienił swoją informację")
				except:
					pass
				
			except:
				status = "Błąd: Nie mogę zmienić danych"
		return render_to_response('infoboard_edit.html', {'tutor_id':tutor_id, 'infoboard':infoboard, 'infoboard_short' : infoboard_short, 'status':status, 'user_name':user_name, 'user_surname':user_surname}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_index(request, user_id):
	if request.user.is_authenticated():
		#Pobieramy wszystkich wykladowcow
		try:
			tutors_list = Tutor.objects.all()
		except:
			tutor_list = None
			
		consultations_data = []
		for tutor in tutors_list:
			t_id = tutor.id
			try:
				tutor_consultations = Consultation.objects.filter(tutor_ID = t_id)
			except:
				tutor_consultations = None
			try:
				tutor_localizations = Localization.objects.get(id = tutor.localization_ID_id)
			except:
				tutor_localizations = None
			try:
				tutor_info = InfoBoard.objects.get(tutor_id = t_id)
			except:
				tutor_info = InfoBoard()
				tutor_info.message = ""
			# Liczymy godziny konsultacji
			con_hours = count_consultation_hours(t_id)
			consult = consultationdata.ConsultationsData()
			consult.tutor_id = tutor.tutor_ID_id
			consult.name =tutor.name
			consult.surname = tutor.surname
			consult.www = "\"http://" + tutor.www + "\""
			consult.title = tutor.degree
			consult.localization = "".join("%s, %s")%(tutor_localizations.building, tutor_localizations.room)
			consult.phone = tutor.phone
			consult.consultations = ""
			today = date.today()
			consult.consultations = []
			raw_consultations = []
			for con in tutor_consultations:
				single_con = singleconsultationdata.SingleConsultationsData()
				single_con.day = con.day
				single_con.start_hour = con.start_hour
				single_con.week_type = con.week_type
				if (single_con.week_type == 'A'):
					single_con.week_type = " "
				single_con.end_hour = con.end_hour
				single_con.expiry_date = con.expiry_date
				single_con.start_minutes = con.start_minutes
				single_con.end_minutes = con.end_minutes
				raw_consultations.append(single_con)
			raw_consultations = sorted(raw_consultations, cmp=time_cmp)
			
			for con in raw_consultations:
				strcon = "".join("%s %s %s:%s-%s:%s")%(con.day, con.week_type, con.start_hour,con.start_minutes, con.end_hour,con.end_minutes )
				if(today>con.expiry_date):
					consult.expiry = "expiry"
				else:
					consult.expiry = "not_expiry"
				if (strcon != ""):
					consult.consultations.append(strcon)

					
					
			
			consult.info = tutor_info.message
			if con_hours < 4:
				consult.consultation_status = "Za mało godzin"
			else:
				consult.consultation_status = "OK"
			consultations_data.append(consult)
			consult = None
		consultations_data = sort_tutors(consultations_data)
		t = loader.get_template('assistant_index.html')
		assistant = Assistant.objects.get(assistant_ID = user_id)
		user_surname = assistant.surname
		user_name = assistant.name
		c = Context({'user_id' : user_id, 'consultations_data' : consultations_data, 'user_name':user_name, 'user_surname':user_surname })
		return HttpResponse(t.render(c))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
	
def assistant_change_dates(request, user_id):
	if request.user.is_authenticated():
		reload(sys)
		sys.setdefaultencoding('utf8')
		assistant = Assistant.objects.get(assistant_ID = user_id)
		status = ""
		date_used = []
		empty_date = ""
		date_dir = "/home/kons/data"
		date_filename = "date.txt"
		filepath = os.path.join(date_dir, date_filename)
		dates_read = open(filepath, "rb")
		for lines in dates_read:
			date_used.append(lines)
		dates_read.close()
		while (len(date_used)<6):
			date_used.append(empty_date)
		#print infoboard.message
		if request.POST:
			#zbieramy dane
			try:
				date_used[0] = request.POST.get('date_name1')
				date_used[1] = request.POST.get('date_value1')
				date_used[2] = request.POST.get('date_name2')
				date_used[3] = request.POST.get('date_value2')
				date_used[4] = request.POST.get('date_name3')
				date_used[5] = request.POST.get('date_value3')
				
				dates_write = open(filepath, "w")
				dates_write.write(date_used[0])
				dates_write.write("\n")
				dates_write.write(date_used[1])
				dates_write.write("\n")
				dates_write.write(date_used[2])
				dates_write.write("\n")
				dates_write.write(date_used[3])
				dates_write.write("\n")
				dates_write.write(date_used[4])
				dates_write.write("\n")
				dates_write.write(date_used[5])
				dates_write.write("\n")
				
				status = "Dane zostały zmienione"
				try:
					log_file_append(assistans.user_id.login, "zmienił ustalone daty")
				except:
					pass
			except:
				status = "Błąd: Nie mogę zmienić danych"

		user_surname = assistant.surname
		user_name = assistant.name
		return render_to_response('assistant_date.html', {'user_id':user_id, 'user_name':user_name, 'user_surname':user_surname, 'status':status, 'date_name1':date_used[0], 'date_name2':date_used[2], 'date_name3':date_used[4], 'date_value1':date_used[1], 'date_value2':date_used[3], 'date_value3':date_used[5]}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
	
	
	
	
def assistant_consultations_delete_confirm(request, user_id):
	if request.user.is_authenticated():
		assistant = Assistant.objects.get(assistant_ID = user_id)
		status = ""
		
		if request.POST:
			confirmation = request.POST.get("potwierdzenie")
			if(confirmation == "TAK"):
				status = "Pomyślnie usunięto konsultacje z bazy."
				
				try:
					log_file_append(assistant.assistant_ID.login, "usunął wszystkie konsultacje")
				except:
					pass
				
				return HttpResponseRedirect(reverse('consultations.views.assistant_consultations_delete', args=(user_id,)))
			else:
				status = "Nie udało się usunąć konsultacji."
		
		user_surname = assistant.surname
		user_name = assistant.name
		return render_to_response('assistant_consultations_delete_confirm.html', {'user_id':user_id, 'user_name':user_name, 'user_surname':user_surname, 'status':status}, context_instance = RequestContext(request) )
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization') )
		
def assistant_consultations_delete(request, user_id):
	if request.user.is_authenticated():
		
		consult_list = Consultation.objects.all()
		for c in consult_list:
			c.delete()
		
		return HttpResponseRedirect(reverse('consultations.views.assistant_index', args=(user_id,)))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_tutor_edit(request, user_id, tutor_id):
	if request.user.is_authenticated():
		assistant = Assistant.objects.get(assistant_ID = user_id)
		status = ""
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_id_from_table = tutor.id
		try:
			localization = Localization.objects.get(id = tutor.localization_ID_id)
		except:
			localization = None
			
		if request.POST:
			#zbiermay dane
			try:
				title = request.POST.get('tytul')
				name = request.POST.get('imie')
				surname = request.POST.get('nazwisko')
				building = request.POST.get('budynek')
				room = request.POST.get('pokoj')
				phone = request.POST.get('telefon')
				mail = request.POST.get('email')
				www = request.POST.get('www')
				
				#zapisujemy zmiany w bazie
				tutor.degree = title
				tutor.name = name
				tutor.surname = surname
				tutor.phone = phone
				tutor.email = mail
				tutor.www = www
				tutor.save()
				localization.room = room
				localization.building = building
				localization.save()
				status = "Dane zostały zmienione"
				try:
					log_file_append(assistant.assistant_ID.login, "zmienił dane prowadzącego jako asystent")
				except:
					pass
				
				return HttpResponseRedirect(reverse('consultations.views.assistant_index', args=(user_id,)))
			except:
				status = "Błąd: Nie mogę zmienić danych"
		user_surname = assistant.surname
		user_name = assistant.name
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_name	= tutor.name
		tutor_surname = tutor.surname
		return render_to_response('assistant_tutor_edit.html', {'user_id':user_id, 'tutor_id':tutor_id, 'localization':localization, 'tutor':tutor, 'status':status, 'user_name':user_name, 'user_surname':user_surname}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
	
def assistant_tutor_delete_confirm(request, user_id, tutor_id):
	if request.user.is_authenticated():
		assistant = Assistant.objects.get(assistant_ID = user_id)
		user_surname = assistant.surname
		user_name = assistant.name
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		return render_to_response('assistant_tutor_delete_confirm.html', {'user_id':user_id, 'tutor_id':tutor_id, 'user_name':user_name, 'user_surname':user_surname, 'tutor':tutor})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_tutor_delete(request, user_id, tutor_id):
	if request.user.is_authenticated():
		
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		user = tutor.tutor_ID
		localization = tutor.localization_ID
		tutor.delete()
		user.delete()
		localization.delete()
		try:
			assistant = Assistant.objects.get(assistant_ID = user_id)
			log_file_append(assistant.assistant_ID.login, "usunął wszystkie konsultacje")
		except:
			pass
		
		return HttpResponseRedirect(reverse('consultations.views.assistant_index', args=(user_id,)))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_consultation_list(request, user_id, tutor_id):
	if request.user.is_authenticated():
		#pobieramy tutora
		try:
			tutor = Tutor.objects.get(tutor_ID = tutor_id)
		except:
			return HttpResponse("Blad krytyczny")
		tutor_id_from_table = tutor.id
		#pobieramy konsultacje tutora
		try:
			consultations = Consultation.objects.filter(tutor_ID = tutor_id_from_table)
		except:
			consultations = None
		#pobieramy lokalizacje
		consultations_data = []
		for consultation in consultations:
			c_id = consultation.id
			try:
				tutor_of_consultation = consultation.tutor_ID
			except:
				tutor_of_consultation = None
			try:
				consultation_localization = consultation.localization_ID
			except:
				consultation_localization = None
			consult = singleconsultationdata.SingleConsultationsData()
			consult.day = consultation.day
			consult.week_type = consultation.week_type

			consult.start_hour = consultation.start_hour
			consult.hours = "".join("%s.%s-%s.%s")%(consultation.start_hour, consultation.start_minutes, consultation.end_hour, consultation.end_minutes)
			consult.building = consultation_localization.building
			consult.room = consultation_localization.room
			consult.students_limit = consultation.students_limit
			if (consult.students_limit == 0):
				consult.students_limit = "-"
			consult.id = consultation.id
			today = date.today();
			if(today>consultation.expiry_date):
				consult.expiry = "expiry"
			else:
				consult.expiry = "not_expiry"
			consult.expiry_date = consultation.expiry_date
			consultations_data.append(consult)
		consultations_data = sorted (consultations_data,  cmp=time_cmp)	
		assistant = Assistant.objects.get(assistant_ID = user_id)
		user_surname = assistant.surname
		user_name = assistant.name
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_name	= tutor.name
		tutor_surname = tutor.surname
		return render_to_response('assistant_consultations_list.html', {'user_id':user_id, 'tutor_id':tutor_id, 'tutor_connsultations':consultations_data, 'user_name':user_name, 'user_surname':user_surname, 'tutor_name':tutor_name, 'tutor_surname':tutor_surname}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))
		
def assistant_consultation_edit(request, user_id, tutor_id, consultation_id):
	if request.user.is_authenticated():
		assistant = Assistant.objects.get(assistant_ID = user_id)
		try:
			tutor = Tutor.objects.get(tutor_ID = tutor_id)
			consult = Consultation.objects.get(id = consultation_id)
			localization = Localization.objects.get(id = consult.localization_ID_id)
		except:
			return HttpResponse("Blad krytyczny");
		else:
			start_hour = consult.start_hour
			start_minutes = consult.start_minutes
			end_hour = consult.end_hour
			end_minutes = consult.end_minutes
			day = consult.day
			week_type = consult.week_type
			students_limit = consult.students_limit
			building = localization.building
			room = localization.room
			expiry_date = ""
			expiry = ""
			try:
				expiry_year = consult.expiry_date.year
				expiry_month = consult.expiry_date.month
				expiry_day = consult.expiry_date.day
				expiry ="".join("%s/%s/%s")%(expiry_day, expiry_month, expiry_year) 
			except:
				pass
				
		
		if request.POST:
			start_hour = request.POST.get('start_hour')
			start_minutes = request.POST.get('start_minutes')
			end_hour = request.POST.get('end_hour')
			end_minutes = request.POST.get('end_minutes')
			day = request.POST.get('day')
			week_type = request.POST.get('week_type')
			students_limit = request.POST.get('students_limit')
			if (students_limit == ""):
				students_limit = 0
			building = request.POST.get('building')
			room = request.POST.get('room')
			
			consult.start_hour = start_hour
			consult.start_minutes = start_minutes
			consult.end_hour = end_hour
			consult.end_minutes = end_minutes
			consult.day = day
			consult.week_type = week_type
			consult.students_limit = students_limit
			localization.building = building
			localization.room = room
			try:
				expiry = request.POST.get('expiry_date')
				data = expiry.split('/')
				expiry_date = date(	int(data[2]), int(data[1]), int(data[0]))
				consult.expiry_date = expiry_date
			except:
				pass
			try:
				consult.save()
				localization.save()
			except:
				return HttpResponse("Nie udało się zmienić konsultacji")
			
			try:
				log_file_append(assistant.assistant_ID.login, "zmienił konsultację użytkownika jako asystent")
			except:
				pass
			
			return HttpResponseRedirect(reverse('consultations.views.assistant_consultation_list', args=(user_id, tutor_id,)))
		user_surname = assistant.surname
		user_name = assistant.name	
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_name	= tutor.name
		tutor_surname = tutor.surname
		
		date_used = []
		empty_date = ""
		date_dir = "/home/kons/data"
		date_filename = "date.txt"
		filepath = os.path.join(date_dir, date_filename)
		dates_read = open(filepath, "rb")
		for lines in dates_read:
			date_used.append(lines)
		dates_read.close()
		while (len(date_used)<6):
			date_used.append(empty_date)
		
		return render_to_response("assistant_consultation_edit.html", {'user_id':user_id, 'consultation_id' : consultation_id, 'tutor_id' : tutor_id, 'start_hour' : start_hour,'start_minutes' : start_minutes, 'end_hour' : end_hour, 'end_minutes' : end_minutes, 'day' : day, 'week_type' : week_type, 'students_limit' : students_limit, 'building' : building, 'room' : room, 'expiry_date' : expiry, 'user_name':user_name, 'user_surname':user_surname, 'tutor_name':tutor_name, 'tutor_surname':tutor_surname, 'date_name1':date_used[0], 'date_value1':date_used[1], 'date_name2':date_used[2], 'date_value2':date_used[3], 'date_name3':date_used[4], 'date_value3':date_used[5]}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))
		
def assistant_consultation_delete_confirm(request, user_id, tutor_id, consultation_id):
	if request.user.is_authenticated():
		assistant = Assistant.objects.get(assistant_ID = user_id)
		user_surname = assistant.surname
		user_name = assistant.name
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_name	= tutor.name
		tutor_surname = tutor.surname
		return render_to_response('assistant_consultation_delete_confirm.html', {'user_id':user_id, 'tutor_id':tutor_id, 'consultation_id':consultation_id, 'user_name':user_name, 'user_surname':user_surname, 'tutor_name':tutor_name, 'tutor_surname':tutor_surname})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_consultation_delete(request, user_id, tutor_id, consultation_id):
	if request.user.is_authenticated():
		
		consult = Consultation.objects.get(id = consultation_id)
		localization = consult.localization_ID
		consult.delete()
		localization.delete()
		
		try:
			assistant = Assistant.objects.get(assistant_ID = user_id)
			log_file_append(assistant.assistant_ID.login, "usunął konsultację użytkownika jako asystent")
		except:
			pass
		
		return HttpResponseRedirect(reverse('consultations.views.assistant_consultation_list', args=(user_id, tutor_id,)))
	
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_consultation_add(request, user_id, tutor_id):
	if request.user.is_authenticated():
		
		tutor = Tutor.objects.get(tutor_ID_id = tutor_id)
		
		new_start_hour = ""
		new_start_minutes = ""
		new_end_minutes = ""
		new_end_hour = ""
		new_day = ""
		new_week_type = ""
		new_students_limit = ""
		new_room = tutor.localization_ID.room
		new_building = tutor.localization_ID.building
		new_expiry = ""
		new_expiry_date = ""
		
		if request.POST:
			
			new_start_hour = request.POST.get('start_hour')
			new_start_minutes = request.POST.get('start_minutes')
			new_end_hour = request.POST.get('end_hour')
			new_end_minutes = request.POST.get('end_minutes')
			new_day = request.POST.get('day')
			new_week_type = request.POST.get('week_type')
			new_students_limit = request.POST.get('students_limit')
			if (new_students_limit == ""):
				new_students_limit = 0
			new_room = request.POST.get('room')
			new_building = request.POST.get('building')
			new_expiry = request.POST.get('expiry_date')
			
			new_localization = Localization()
			new_localization.room = new_room
			new_localization.building = new_building
			new_localization.save()
			
			new_consultation = Consultation()
			new_consultation.tutor_ID = tutor
			new_consultation.start_hour = new_start_hour
			new_consultation.start_minutes = new_start_minutes
			new_consultation.end_hour = new_end_hour
			new_consultation.end_minutes = new_end_minutes
			new_consultation.day = new_day
			new_consultation.week_type = new_week_type
			new_consultation.students_limit = new_students_limit
			
			new_consultation.localization_ID = new_localization
			
			data = new_expiry.split('/')
			try:
				new_expiry_date = date(	int(data[2]), int(data[1]), int(data[0]))
			except:
				return HttpResponse("Podano złą datę")
			new_consultation.expiry_date = new_expiry_date		
			new_consultation.save()
			
			try:
				assistant = Assistant.objects.get(assistant_ID = user_id)
				log_file_append(assistant.assistant_ID.login, "dodał konsultację jako asystent")
			except:
				pass
				
			return HttpResponseRedirect(reverse('consultations.views.assistant_consultation_list', args=(user_id, tutor_id,)))
		assistant = Assistant.objects.get(assistant_ID = user_id)
		user_surname = assistant.surname
		user_name = assistant.name	
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_name	= tutor.name
		tutor_surname = tutor.surname
		
		date_used = []
		empty_date = ""
		date_dir = "/home/kons/data"
		date_filename = "date.txt"
		filepath = os.path.join(date_dir, date_filename)
		dates_read = open(filepath, "rb")
		for lines in dates_read:
			date_used.append(lines)
		dates_read.close()
		while (len(date_used)<6):
			date_used.append(empty_date)
		
		return render_to_response("assistant_consultation_add.html", { 'user_id':user_id, 'tutor_id' : tutor_id, 'start_hour' : new_start_hour, 'start_minutes' : new_start_minutes,  'end_hour' : new_end_hour, 'end_minutes' : new_end_minutes, 'day' : new_day, 'week_type' : new_week_type, 'students_limit' : new_students_limit, 'room' : new_room, 'building' : new_building, 'expiry_date' : new_expiry_date, 'user_name':user_name, 'user_surname':user_surname, 'tutor_name':tutor_name, 'tutor_surname':tutor_surname, 'date_name1':date_used[0], 'date_value1':date_used[1], 'date_name2':date_used[2], 'date_value2':date_used[3], 'date_name3':date_used[4], 'date_value3':date_used[5]}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))
		
def assistant_consultation_deleteall_confirm(request, user_id, tutor_id):
	if request.user.is_authenticated():
		assistant = Assistant.objects.get(assistant_ID = user_id)
		user_surname = assistant.surname
		user_name = assistant.name
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_name	= tutor.name
		tutor_surname = tutor.surname
		return render_to_response('assistant_consultation_deleteall_confirm.html', {'user_id':user_id, 'tutor_id':tutor_id, 'user_name':user_name, 'user_surname':user_surname})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_consultation_deleteall(request, user_id, tutor_id):
	if request.user.is_authenticated():
		try:
			tutor = Tutor.objects.get(tutor_ID = tutor_id)
		except:
			return HttpResponse("Blad krytyczny")
		tutor_id_from_table = tutor.id
		
		consults = Consultation.objects.filter(tutor_ID_id = tutor_id_from_table)
		for con in consults:
			con.delete()
		
		try:
			assistant = Assistant.objects.get(assistant_ID = user_id)
			log_file_append(assistant.assistant_ID.login, "usunął wszystkie konsultacje użytkownia jako asystent")
		except:
			pass
		
		return HttpResponseRedirect(reverse('consultations.views.assistant_consultation_list', args=(user_id, tutor_id,)))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_adduser(request, user_id):
	if request.user.is_authenticated():
		status = ""
		login = ""
		
		user = User()
		tutor = Tutor()
		localization = Localization()
		
		user.login = ""
		user.last_login_date = date.today()
		user.typ = ""
		
		tutor.degree = ""
		tutor.name = ""
		tutor.surname = ""
		tutor.institute = ""
		tutor.phone = ""
		tutor.email = ""
		tutor.www = ""
						
		localization.room = ""
		localization.building = ""
		
		if request.POST:
			#zbiermay dane
			try:
				login = request.POST.get('login')
				title = request.POST.get('tytul')
				name = request.POST.get('imie')
				surname = request.POST.get('nazwisko')
				institute = request.POST.get('instytut')
				building = request.POST.get('budynek')
				room = request.POST.get('pokoj')
				phone = request.POST.get('telefon')
				mail = request.POST.get('email')
				www = request.POST.get('www')
				
				#zapisujemy zmiany w bazie
				
				user.login = login
				user.save()
				
				localization.room = room
				localization.building = building
				localization.save()
				
				tutor.tutor_ID = user
				tutor.degree = title
				tutor.name = name
				tutor.surname = surname
				tutor.institute = institute
				tutor.phone = phone
				tutor.email = mail
				tutor.www = www
				tutor.localization_ID = localization
				
				tutor.save()
				
				iboard = InfoBoard()
				iboard.date_of_adding = date.today()
				iboard.message = ""
				iboard.tutor_id = tutor
				iboard.save()
				
				status = "Dodano użytkownika"
				
				try:
					assistant = Assistant.objects.get(assistant_ID = user_id)
					log_file_append(assistant.assistant_ID.login, "dodał użytkownika")
				except:
					pass
			except:
				status = "Błąd: Nie mogę dodać użytkownika"
			else:
				return HttpResponseRedirect(reverse('consultations.views.assistant_index', args=(user_id,)))
		assistant = Assistant.objects.get(assistant_ID = user_id)
		user_surname = assistant.surname
		user_name = assistant.name
		return render_to_response('assistant_addtutor.html', {'user_id':user_id, 'user_login':login, 'localization':localization, 'tutor':tutor, 'status':status, 'user_name':user_name, 'user_surname':user_surname}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def choose_panel(request, user_id):
	if request.user.is_authenticated():
		assistant = Assistant.objects.get(assistant_ID = user_id)
		user_surname = assistant.surname
		user_name = assistant.name
		return render_to_response('choose_panel.html', {'user_id':user_id, 'user_name':user_name, 'user_surname':user_surname})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_export_csv(request, user_id):
	if request.user.is_authenticated():
		assistant = Assistant.objects.get(assistant_ID = user_id)
		user_surname = assistant.surname
		user_name = assistant.name
		return render_to_response('assistant_export_csv.html', {'user_id':user_id, 'user_name':user_name, 'user_surname':user_surname})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))

def assistant_import_csv(request, user_id):
	if request.user.is_authenticated():
		assistant = Assistant.objects.get(assistant_ID = user_id)
		user_surname = assistant.surname
		user_name = assistant.name
		return render_to_response('assistant_import_csv.html', {'user_id':user_id, 'user_name':user_name, 'user_surname':user_surname})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def export_csv(request, user_id):
	if request.user.is_authenticated():
		reload(sys)
		sys.setdefaultencoding('utf8')
		response = HttpResponse(mimetype='text/csv')
		response['Content-Disposition'] = 'attachment; filename=konsultacje.csv'
		writer = csv.writer(response)
		writer.writerow(['Login; Tytuł; Imię; Nazwisko; Instytut; Telefon; E-mail; WWW; Lokalizacja(Pokój, Budynek); Konsultacje(Termin, Tydzień, Limit, Lokalizacja);'])
		
		#Pobieramy tutorow i konsultacje
		tutors = Tutor.objects.all()
		for tutor in tutors:
			consultations_string = ""
			consultations = Consultation.objects.filter(tutor_ID = tutor)
			tutor_loc = tutor.localization_ID
			tutor_user = tutor.tutor_ID
			for con in consultations:
				loc = con.localization_ID
				consultations_string += ''.join(['%s %s %s:%s-%s:%s %s %s %s;' %(con.day, con.week_type, con.start_hour, con.start_minutes, con.end_hour, con.end_minutes, con.students_limit, loc.building, loc.room)])
			writer.writerow(['%s; %s; %s; %s; %s; %s; %s; %s; %s; %s; %s;' %(tutor_user.login, tutor.degree, tutor.name, tutor.surname, tutor.institute, tutor.phone, tutor.email, tutor.www, tutor_loc.room, tutor_loc.building, consultations_string)])
		return response
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))

def assistant_backup(request, user_id):
	if request.user.is_authenticated():
		from django.core.servers.basehttp import FileWrapper
		dbname = "ProjektZespolowy"
		user = "root"
		password = "bdpass7"
		host = "localhost"
		
		backup_dir = '/home/kons/backup/'
		filename = 'backup_%s.sql' % time.strftime('%y%m%d')
		filepath = os.path.join(backup_dir, filename)
		
		args = []
		
		args += ["%s"%dbname]
		args += ["%s %s %s %s %s %s %s %s %s"%("consultations_administrator", "consultations_assistant", "consultations_consultation", "consultations_consultationassignment", "consultations_infoboard", "consultations_localization", "consultations_student", "consultations_tutor", "consultations_user")]
		args += ["--user=%s"%user]
		args += ["--password=%s"%password]
		os.system("mysqldump %s > %s"%(' '.join(args), filepath))
		sqlfile = open(filepath, "r")
		wrapper = FileWrapper(sqlfile)
		
		response = HttpResponse(wrapper, mimetype='application/force-download')
		response['Content-Disposition'] = 'attachment; filename=%s' % filename
		response['Content-Length'] = os.path.getsize(filepath)
		return response
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))

def assistant_restore(request, user_id):
	if request.user.is_authenticated():
		status = ""
		if request.method == 'POST':
			form = uploadfileform.UploadFileForm(request.POST, request.FILES)
			if form.is_valid():
				filepath = "/home/kons/restore/backup_tmp.sql"
				file = request.FILES['file']
				file_on_server = open(filepath, 'w')
				for chunk in file.chunks():
					file_on_server.write(chunk)
				file_on_server.close()
				
				dbname = "ProjektZespolowy"
				user = "root"
				password = "bdpass7"
				host = "localhost"
				
				args = []
				
				args += ["--user=%s"%user]
				args += ["--password=%s"%password]
				args += ["%s"%dbname]
				
				polecenie = "mysql %s < %s"%(' '.join(args), filepath)
				os.system("mysql --verbose %s < %s"%(' '.join(args), filepath))
				
				status = "Pomyślnie przywrócono bazę danych"
				
				try:
					assistant = Assistant.objects.get(assistant_ID = user_id)
					log_file_append(assistant.assistant_ID.login, "wykonał operację na bazie danych")
				except:
					pass
		else:
			form = uploadfileform.UploadFileForm()
		assistant = Assistant.objects.get(assistant_ID = user_id)
		user_surname = assistant.surname
		user_name = assistant.name
		return render_to_response('assistant_restore.html', {'user_id':user_id,'form':form, 'status':status, 'user_name':user_name, 'user_surname':user_surname}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))

def admin_index(request, user_id):
	if request.user.is_authenticated():
		#Pobieramy wszystkich wykladowcow
		try:
			tutors_list = Tutor.objects.all()
		except:
			tutor_list = None
			
		consultations_data = []
		for tutor in tutors_list:
			t_id = tutor.id
			try:
				tutor_consultations = Consultation.objects.filter(tutor_ID = t_id)
			except:
				tutor_consultations = None
			try:
				tutor_localizations = Localization.objects.get(id = tutor.localization_ID_id)
			except:
				tutor_localizations = None
			try:
				tutor_info = InfoBoard.objects.get(tutor_id = t_id)
			except:
				tutor_info = InfoBoard()
				tutor_info.message = ""
			# Liczymy godziny konsultacji
			con_hours = count_consultation_hours(t_id)
			consult = consultationdata.ConsultationsData()
			consult.tutor_id = tutor.tutor_ID_id
			consult.name =tutor.name
			consult.surname = tutor.surname
			consult.www = "\"http://" + tutor.www + "\""
			consult.title = tutor.degree
			consult.localization = "".join("%s, %s")%(tutor_localizations.building, tutor_localizations.room)
			consult.phone = tutor.phone
			consult.consultations = ""
			today = date.today()
			consult.consultations = []
			raw_consultations = []
			for con in tutor_consultations:
				single_con = singleconsultationdata.SingleConsultationsData()
				single_con.day = con.day
				single_con.start_hour = con.start_hour
				single_con.week_type = con.week_type
				if (single_con.week_type == 'A'):
					single_con.week_type = " "
				single_con.end_hour = con.end_hour
				single_con.expiry_date = con.expiry_date
				single_con.start_minutes = con.start_minutes
				single_con.end_minutes = con.end_minutes
				raw_consultations.append(single_con)
			raw_consultations = sorted(raw_consultations, cmp=time_cmp)
			
			for con in raw_consultations:
				strcon = "".join("%s %s %s:%s-%s:%s")%(con.day, con.week_type, con.start_hour,con.start_minutes, con.end_hour,con.end_minutes )
				if(today>con.expiry_date):
					consult.expiry = "expiry"
				else:
					consult.expiry = "not_expiry"
				if (strcon != ""):
					consult.consultations.append(strcon)
			
			
			consult.info = tutor_info.message
			if con_hours < 4:
				consult.consultation_status = "Za mało godzin"
			else:
				consult.consultation_status = "OK"
			consultations_data.append(consult)
			consult = None
		consultations_data = sort_tutors(consultations_data)
		t = loader.get_template('admin_index.html')
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		c = Context({'user_id' : user_id, 'consultations_data' : consultations_data, 'user_name':user_name, 'user_surname':user_surname })
		return HttpResponse(t.render(c))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_consultations_delete_confirm(request, user_id):
	if request.user.is_authenticated():
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		status = ""
		
		if request.POST:
			confirmation = request.POST.get("potwierdzenie")
			if(confirmation == "TAK"):
				status = "Usunięto konsultacje użytkowników."
				return HttpResponseRedirect(reverse('consultations.views.admin_consultations_delete', args=(user_id,)))
			else:
				status = "Nie udało się usunąć konsultacji."
		return render_to_response('admin_consultations_delete_confirm.html', {'user_id':user_id, 'user_name':user_name, 'user_surname':user_surname, 'status':status}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_consultations_delete(request, user_id):
	if request.user.is_authenticated():
		
		consult_list = Consultation.objects.all()
		for c in consult_list:
			c.delete()
		
		try:
			admin = Administrator.objects.get(administrator_ID = user_id)
			log_file_append(admin.administrator_ID.login, "usunął wszystkie konsultacje")
		except:
			pass	
		
		return HttpResponseRedirect(reverse('consultations.views.admin_index', args=(user_id,)))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_tutor_edit(request, user_id, tutor_id):
	if request.user.is_authenticated():
		status = ""
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_id_from_table = tutor.id
		try:
			localization = Localization.objects.get(id = tutor.localization_ID_id)
		except:
			localization = None
			
		if request.POST:
			#zbiermay dane
			try:
				title = request.POST.get('tytul')
				name = request.POST.get('imie')
				surname = request.POST.get('nazwisko')
				building = request.POST.get('budynek')
				room = request.POST.get('pokoj')
				phone = request.POST.get('telefon')
				mail = request.POST.get('email')
				www = request.POST.get('www')
				
				#zapisujemy zmiany w bazie
				tutor.degree = title
				tutor.name = name
				tutor.surname = surname
				tutor.phone = phone
				tutor.email = mail
				tutor.www = www
				tutor.save()
				localization.room = room
				localization.building = building
				localization.save()
				status = "Dane zostały zmienione"
				
				try:
					admin = Administrator.objects.get(administrator_ID = user_id)
					log_file_append(admin.administrator_ID.login, "edytował dane użytkownika jako administrator")
				except:
					pass
				
				return HttpResponseRedirect(reverse('consultations.views.admin_index', args=(user_id,)))
			except:
				status = "Błąd: Nie mogę zmienić danych"
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname		
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_name	= tutor.name
		tutor_surname = tutor.surname
		return render_to_response('admin_tutor_edit.html', {'user_id':user_id, 'tutor_id':tutor_id, 'localization':localization, 'tutor':tutor, 'status':status, 'user_name':user_name, 'user_surname':user_surname}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
	
def admin_tutor_delete_confirm(request, user_id, tutor_id):
	if request.user.is_authenticated():
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		return render_to_response('admin_tutor_delete_confirm.html', {'user_id':user_id, 'tutor_id':tutor_id, 'user_name':user_name, 'user_surname':user_surname, 'tutor':tutor})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_tutor_delete(request, user_id, tutor_id):
	if request.user.is_authenticated():
		
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		user = tutor.tutor_ID
		localization = tutor.localization_ID
		tutor.delete()
		user.delete()
		localization.delete()
		
		try:
			admin = Administrator.objects.get(administrator_ID = user_id)
			log_file_append(admin.administrator_ID.login, "usunął użytkownika jako administrator")
		except:
			pass
		
		return HttpResponseRedirect(reverse('consultations.views.admin_index', args=(user_id,)))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_consultation_list(request, user_id, tutor_id):
	if request.user.is_authenticated():
		#pobieramy tutora
		try:
			tutor = Tutor.objects.get(tutor_ID = tutor_id)
		except:
			return HttpResponse("Blad krytyczny")
		tutor_id_from_table = tutor.id
		#pobieramy konsultacje tutora
		try:
			consultations = Consultation.objects.filter(tutor_ID = tutor_id_from_table)
		except:
			consultations = None
		#pobieramy lokalizacje
		consultations_data = []
		for consultation in consultations:
			c_id = consultation.id
			try:
				tutor_of_consultation = consultation.tutor_ID
			except:
				tutor_of_consultation = None
			try:
				consultation_localization = consultation.localization_ID
			except:
				consultation_localization = None
			consult = singleconsultationdata.SingleConsultationsData()
			consult.day = consultation.day
			consult.week_type = consultation.week_type

			consult.start_hour = consultation.start_hour
			consult.hours = "".join("%s.%s-%s.%s")%(consultation.start_hour, consultation.start_minutes, consultation.end_hour, consultation.end_minutes)
			consult.building = consultation_localization.building
			consult.room = consultation_localization.room
			consult.students_limit = consultation.students_limit
			if (consult.students_limit == 0):
				consult.students_limit = "-"
			consult.id = consultation.id
			today = date.today();
			if(today>consultation.expiry_date):
				consult.expiry = "expiry"
			else:
				consult.expiry = "not_expiry"
			consult.expiry_date = consultation.expiry_date
			consultations_data.append(consult)
		consultations_data = sorted (consultations_data,  cmp=time_cmp)	
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_name	= tutor.name
		tutor_surname = tutor.surname
		return render_to_response('admin_consultations_list.html', {'user_id':user_id, 'tutor_id':tutor_id, 'tutor_connsultations':consultations_data, 'user_name':user_name, 'tutor_name':tutor_name, 'tutor_surname':tutor_surname}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))
		
def admin_consultation_edit(request, user_id, tutor_id, consultation_id):
	if request.user.is_authenticated():
		try:
			tutor = Tutor.objects.get(tutor_ID = tutor_id)
			consult = Consultation.objects.get(id = consultation_id)
			localization = Localization.objects.get(id = consult.localization_ID_id)
		except:
			return HttpResponse("Blad krytyczny");
		else:
			start_hour = consult.start_hour
			start_minutes = consult.start_minutes
			end_hour = consult.end_hour
			end_minutes = consult.end_minutes
			day = consult.day
			week_type = consult.week_type
			students_limit = consult.students_limit
			building = localization.building
			room = localization.room
			expiry_date = ""
			expiry = ""
			try:
				expiry_year = consult.expiry_date.year
				expiry_month = consult.expiry_date.month
				expiry_day = consult.expiry_date.day
				expiry ="".join("%s/%s/%s")%(expiry_day, expiry_month, expiry_year) 
			except:
				pass
				
		
		if request.POST:
			start_hour = request.POST.get('start_hour')
			start_minutes = request.POST.get('start_minutes')
			end_hour = request.POST.get('end_hour')
			end_minutes = request.POST.get('end_minutes')
			day = request.POST.get('day')
			week_type = request.POST.get('week_type')
			students_limit = request.POST.get('students_limit')
			if (students_limit == ""):
				students_limit = 0
			building = request.POST.get('building')
			room = request.POST.get('room')
			
			consult.start_hour = start_hour
			consult.start_minutes = start_minutes
			consult.end_hour = end_hour
			consult.end_minutes = end_minutes
			consult.day = day
			consult.week_type = week_type
			consult.students_limit = students_limit
			localization.building = building
			localization.room = room
			try:
				expiry = request.POST.get('expiry_date')
				data = expiry.split('/')
				expiry_date = date(	int(data[2]), int(data[1]), int(data[0]))
				consult.expiry_date = expiry_date
			except:
				pass
				
			try:
				consult.save()
				localization.save()
			except:
				return HttpResponse("Nie udało się zmienić konsultacji")
			
			try:
				admin = Administrator.objects.get(administrator_ID = user_id)
				log_file_append(admin.administrator_ID.login, "edytował konsultację użytkownika jako administrator")
			except:
				pass
			
			return HttpResponseRedirect(reverse('consultations.views.admin_consultation_list', args=(user_id, tutor_id,)))
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_name	= tutor.name
		tutor_surname = tutor.surname	
		
		date_used = []
		empty_date = ""
		date_dir = "/home/kons/data"
		date_filename = "date.txt"
		filepath = os.path.join(date_dir, date_filename)
		dates_read = open(filepath, "rb")
		for lines in dates_read:
			date_used.append(lines)
		dates_read.close()
		while (len(date_used)<6):
			date_used.append(empty_date)
			
		return render_to_response("admin_consultation_edit.html", {'user_id':user_id, 'consultation_id' : consultation_id, 'tutor_id' : tutor_id, 'start_hour' : start_hour,'start_minutes' : start_minutes, 'end_hour' : end_hour, 'end_minutes' : end_minutes, 'day' : day, 'week_type' : week_type, 'students_limit' : students_limit, 'building' : building, 'room' : room, 'expiry_date' : expiry, 'user_name':user_name, 'user_surname':user_surname,'tutor_name':tutor_name, 'tutor_surname':tutor_surname, 'date_name1':date_used[0], 'date_value1':date_used[1], 'date_name2':date_used[2], 'date_value2':date_used[3], 'date_name3':date_used[4], 'date_value3':date_used[5]}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))
		
def admin_consultation_delete_confirm(request, user_id, tutor_id, consultation_id):
	if request.user.is_authenticated():
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_name	= tutor.name
		tutor_surname = tutor.surname
		return render_to_response('admin_consultation_delete_confirm.html', {'user_id':user_id, 'tutor_id':tutor_id, 'consultation_id':consultation_id, 'user_name':user_name, 'user_surname':user_surname,'tutor_name':tutor_name, 'tutor_surname':tutor_surname})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_consultation_delete(request, user_id, tutor_id, consultation_id):
	if request.user.is_authenticated():
		
		consult = Consultation.objects.get(id = consultation_id)
		localization = consult.localization_ID
		consult.delete()
		localization.delete()
		
		try:
			admin = Administrator.objects.get(administrator_ID = user_id)
			log_file_append(admin.administrator_ID.login, "usunął konsultację użytkownika jako administrator")
		except:
			pass
					
		return HttpResponseRedirect(reverse('consultations.views.admin_consultation_list', args=(user_id, tutor_id,)))
	
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_consultation_add(request, user_id, tutor_id):
	if request.user.is_authenticated():
		
		tutor = Tutor.objects.get(tutor_ID_id = tutor_id)
		
		new_start_hour = ""
		new_start_minutes = ""
		new_end_minutes = ""
		new_end_hour = ""
		new_day = ""
		new_week_type = ""
		new_students_limit = ""
		new_room = tutor.localization_ID.room
		new_building = tutor.localization_ID.building
		new_expiry = ""
		new_expiry_date = ""
		
		if request.POST:
			
			new_start_hour = request.POST.get('start_hour')
			new_start_minutes = request.POST.get('start_minutes')
			new_end_hour = request.POST.get('end_hour')
			new_end_minutes = request.POST.get('end_minutes')
			new_day = request.POST.get('day')
			new_week_type = request.POST.get('week_type')
			new_students_limit = request.POST.get('students_limit')
			if (new_students_limit == ""):
				new_students_limit = 0
			new_room = request.POST.get('room')
			new_building = request.POST.get('building')
			new_expiry = request.POST.get('expiry_date')
			
			new_localization = Localization()
			new_localization.room = new_room
			new_localization.building = new_building
			new_localization.save()
			
			new_consultation = Consultation()
			new_consultation.tutor_ID = tutor
			new_consultation.start_hour = new_start_hour
			new_consultation.start_minutes = new_start_minutes
			new_consultation.end_hour = new_end_hour
			new_consultation.end_minutes = new_end_minutes
			new_consultation.day = new_day
			new_consultation.week_type = new_week_type
			new_consultation.students_limit = new_students_limit
			
			new_consultation.localization_ID = new_localization
			
			data = new_expiry.split('/')
			try:
				new_expiry_date = date(	int(data[2]), int(data[1]), int(data[0]))
			except:
				return HttpResponse("Podano błędną datę")
			new_consultation.expiry_date = new_expiry_date
		#	print new_consultation.expiry_date
			try:
				new_consultation.save()
			except:
				return HttpResponse("Nie udało się dodać konsultacji")
				
			try:
				admin = Administrator.objects.get(administrator_ID = user_id)
				log_file_append(admin.administrator_ID.login, "dodał konsultację jako administrator")
			except:
				pass
			
			return HttpResponseRedirect(reverse('consultations.views.admin_consultation_list', args=(user_id, tutor_id,)))
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_name	= tutor.name
		tutor_surname = tutor.surname
		
		date_used = []
		empty_date = ""
		date_dir = "/home/kons/data"
		date_filename = "date.txt"
		filepath = os.path.join(date_dir, date_filename)
		dates_read = open(filepath, "rb")
		for lines in dates_read:
			date_used.append(lines)
		dates_read.close()
		while (len(date_used)<6):
			date_used.append(empty_date)
			
		return render_to_response("admin_consultation_add.html", { 'user_id':user_id, 'tutor_id' : tutor_id, 'start_hour' : new_start_hour, 'start_minutes' : new_start_minutes,  'end_hour' : new_end_hour, 'end_minutes' : new_end_minutes, 'day' : new_day, 'week_type' : new_week_type, 'students_limit' : new_students_limit, 'room' : new_room, 'building' : new_building, 'expiry_date' : new_expiry_date, 'user_name':user_name, 'user_surname':user_surname, 'tutor_name':tutor_name, 'tutor_surname':tutor_surname, 'date_name1':date_used[0], 'date_value1':date_used[1], 'date_name2':date_used[2], 'date_value2':date_used[3], 'date_name3':date_used[4], 'date_value3':date_used[5]}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))
		
def admin_consultation_deleteall_confirm(request, user_id, tutor_id):
	if request.user.is_authenticated():
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_name	= tutor.name
		tutor_surname = tutor.surname
		return render_to_response('admin_consultation_deleteall_confirm.html', {'user_id':user_id, 'tutor_id':tutor_id, 'user_name':user_name, 'user_surname':user_surname, 'tutor_name':tutor_name, 'tutor_surname':tutor_surname})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_consultation_deleteall(request, user_id, tutor_id):
	if request.user.is_authenticated():
		try:
			tutor = Tutor.objects.get(tutor_ID = tutor_id)
		except:
			return HttpResponse("Blad krytyczny")
		tutor_id_from_table = tutor.id
		
		consults = Consultation.objects.filter(tutor_ID_id = tutor_id_from_table)
		for con in consults:
			con.delete()
		
		try:
			admin = Administrator.objects.get(administrator_ID = user_id)
			log_file_append(admin.administrator_ID.login, "usunął konsultacje użytkownika jako administrator")
		except:
			pass
		
		return HttpResponseRedirect(reverse('consultations.views.admin_consultation_list', args=(user_id, tutor_id,)))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_adduser(request, user_id):
	if request.user.is_authenticated():
		status = ""
		login = ""
		
		user = User()
		tutor = Tutor()
		localization = Localization()
		
		user.login = ""
		user.last_login_date = date.today()
		user.typ = ""
		
		tutor.degree = ""
		tutor.name = ""
		tutor.surname = ""
		tutor.institute = ""
		tutor.phone = ""
		tutor.email = ""
		tutor.www = ""
						
		localization.room = ""
		localization.building = ""
		
		if request.POST:
			#zbiermay dane
			try:
				login = request.POST.get('login')
				title = request.POST.get('tytul')
				name = request.POST.get('imie')
				surname = request.POST.get('nazwisko')
				institute = request.POST.get('instytut')
				building = request.POST.get('budynek')
				room = request.POST.get('pokoj')
				phone = request.POST.get('telefon')
				mail = request.POST.get('email')
				www = request.POST.get('www')
				
				#zapisujemy zmiany w bazie
				
				user.login = login
				user.save()
				
				localization.room = room
				localization.building = building
				localization.save()
				
				tutor.tutor_ID = user
				tutor.degree = title
				tutor.name = name
				tutor.surname = surname
				tutor.institute = institute
				tutor.phone = phone
				tutor.email = mail
				tutor.www = www
				tutor.localization_ID = localization
				
				tutor.save()
				
				iboard = InfoBoard()
				iboard.date_of_adding = date.today()
				iboard.message = ""
				iboard.tutor_id = tutor
				iboard.save()
				
				try:
					admin = Administrator.objects.get(administrator_ID = user_id)
					log_file_append(admin.administrator_ID.login, "dodał użytkownika jako administrator")
				except:
					pass
				
				status = "Dodano użytkownika"
			except:
				status = "Błąd: Nie mogę dodać użytkownika"
			else:
				return HttpResponseRedirect(reverse('consultations.views.admin_index', args=(user_id,)))
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		return render_to_response('admin_addtutor.html', {'user_id':user_id, 'user_login':login, 'localization':localization, 'tutor':tutor, 'status':status, 'user_name':user_name, 'user_surname':user_surname}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_export_csv_confirm(request, user_id):
	if request.user.is_authenticated():
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		return render_to_response('admin_export_csv.html', {'user_id':user_id, 'user_name':user_name, 'user_surname':user_surname})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))

def admin_import_csv(request, user_id):
	if request.user.is_authenticated():
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		return render_to_response('admin_import_csv.html', {'user_id':user_id, 'user_name':user_name, 'user_surname':user_surname})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_export_csv(request, user_id):
	if request.user.is_authenticated():
		reload(sys)
		sys.setdefaultencoding('utf8')
		response = HttpResponse(mimetype='text/csv')
		response['Content-Disposition'] = 'attachment; filename=konsultacje.csv'
		writer = csv.writer(response)
		writer.writerow(['Login; Tytuł; Imię; Nazwisko; Instytut; Telefon; E-mail; WWW; Lokalizacja(Pokój, Budynek); Konsultacje(Termin, Tydzień, Limit, Lokalizacja);'])
		
		#Pobieramy tutorow i konsultacje
		tutors = Tutor.objects.all()
		for tutor in tutors:
			consultations_string = ""
			consultations = Consultation.objects.filter(tutor_ID = tutor)
			tutor_loc = tutor.localization_ID
			tutor_user = tutor.tutor_ID
			for con in consultations:
				loc = con.localization_ID
				consultations_string += ''.join(['%s %s %s:%s-%s:%s %s %s %s;' %(con.day, con.week_type, con.start_hour, con.start_minutes, con.end_hour, con.end_minutes, con.students_limit, loc.building, loc.room)])
			writer.writerow(['%s; %s; %s; %s; %s; %s; %s; %s; %s; %s; %s;' %(tutor_user.login, tutor.degree, tutor.name, tutor.surname, tutor.institute, tutor.phone, tutor.email, tutor.www, tutor_loc.room, tutor_loc.building, consultations_string)])
		return response
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))

def admin_backup(request, user_id):
	if request.user.is_authenticated():
		from django.core.servers.basehttp import FileWrapper
		dbname = "ProjektZespolowy"
		user = "root"
		password = "bdpass7"
		host = "localhost"
		
		backup_dir = '/home/kons/backup/'
		filename = 'backup_%s.sql' % time.strftime('%y%m%d')
		filepath = os.path.join(backup_dir, filename)
		
		args = []
		
		args += ["%s"%dbname]
		args += ["%s %s %s %s %s %s %s %s %s"%("consultations_administrator", "consultations_assistant", "consultations_consultation", "consultations_consultationassignment", "consultations_infoboard", "consultations_localization", "consultations_student", "consultations_tutor", "consultations_user")]
		args += ["--user=%s"%user]
		args += ["--password=%s"%password]
		os.system("mysqldump %s > %s"%(' '.join(args), filepath))
		sqlfile = open(filepath, "r")
		wrapper = FileWrapper(sqlfile)
		
		response = HttpResponse(wrapper, mimetype='application/force-download')
		response['Content-Disposition'] = 'attachment; filename=%s' % filename
		response['Content-Length'] = os.path.getsize(filepath)
		return response
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))

def admin_restore(request, user_id):
	if request.user.is_authenticated():
		status = ""
		if request.method == 'POST':
			form = uploadfileform.UploadFileForm(request.POST, request.FILES)
			if form.is_valid():
				filepath = "/home/kons/restore/backup_tmp.sql"
				file = request.FILES['file']
				file_on_server = open(filepath, 'w')
				for chunk in file.chunks():
					file_on_server.write(chunk)
				file_on_server.close()
				
				dbname = "ProjektZespolowy"
				user = "root"
				password = "bdpass7"
				host = "localhost"
				
				args = []
				
				args += ["--user=%s"%user]
				args += ["--password=%s"%password]
				args += ["%s"%dbname]
				
				polecenie = "mysql %s < %s"%(' '.join(args), filepath)
				os.system("mysql --verbose %s < %s"%(' '.join(args), filepath))
				
				status = "Pomyślnie przywrócono bazę danych"
				
				try:
					admin = Administrator.objects.get(administrator_ID = user_id)
					log_file_append(admin.administrator_ID.login, "wykonał operację na bazie danych")
				except:
					pass
		else:
			form = uploadfileform.UploadFileForm()
			
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_surname = admin.surname
		user_name = admin.name
		
		return render_to_response('admin_restore.html', {'user_id':user_id,'form':form, 'status':status, 'user_name':user_name, 'user_surname':user_surname}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_assistant_list(request, user_id):
	if request.user.is_authenticated():
		assistant_list = Assistant.objects.all()
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		return render_to_response('admin_assistant_list.html', {'user_id':user_id, 'assistant_list':assistant_list, 'user_name':user_name, 'user_surname':user_surname})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_assistant_add(request, user_id):
	if request.user.is_authenticated():
		status = ""
		if request.POST:
			#na - new_assistant
			na_login = request.POST.get("login")
			na_name = request.POST.get("imie")
			na_surname = request.POST.get("nazwisko")
			try:
				user = User.objects.get(login = na_login)
			except:
				user = User()
				user.login = na_login
				user.typ = "assistant"
				user.save()
				
			na = Assistant()
			na.assistant_ID = user
			na.name = na_name
			na.surname = na_surname
			na.save()
			
			try:
				admin = Administrator.objects.get(administrator_ID = user_id)
				log_file_append(admin.administrator_ID.login, "dodał asystenta")
			except:
				pass
			
			return HttpResponseRedirect(reverse('consultations.views.admin_assistant_list', args=(user_id,)))
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		return render_to_response('admin_addassistant.html', {'user_id':user_id, 'status':status, 'user_name':user_name, 'user_surname':user_surname}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_assistant_delete_confirm(request, user_id, assistant_id):
	if request.user.is_authenticated():
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		return render_to_response('admin_assistant_delete_confirm.html', {'user_id':user_id, 'assistant_id':assistant_id, 'user_name':user_name, 'user_surname':user_surname})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_assistant_delete(request, user_id, assistant_id):
	if request.user.is_authenticated():
		assistant = Assistant.objects.get(assistant_ID_id = assistant_id)
		assistant.delete()
		
		try:
			admin = Administrator.objects.get(administrator_ID = user_id)
			log_file_append(admin.administrator_ID.login, "odebrał prawa asystenta")
		except:
			pass
		
		return HttpResponseRedirect(reverse('consultations.views.admin_assistant_list', args=(user_id,)))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
	
def admin_admin_list(request, user_id):
	if request.user.is_authenticated():
		admin_list = Administrator.objects.all()
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		return render_to_response('admin_admin_list.html', {'user_id':user_id, 'admin_list':admin_list, 'user_name':user_name, 'user_surname':user_surname})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_admin_add(request, user_id):
	if request.user.is_authenticated():
		status = ""
		if request.POST:
			#na - new_admin
			na_login = request.POST.get("login")
			na_name = request.POST.get("imie")
			na_surname = request.POST.get("nazwisko")
			try:
				user = User.objects.get(login = na_login)
			except:
				user = User()
				user.login = na_login
				user.typ = "admin"
				user.save()
				
			na = Administrator()
			na.administrator_ID = user
			na.name = na_name
			na.surname = na_surname
			na.save()
			
			try:
				admin = Administrator.objects.get(administrator_ID = user_id)
				log_file_append(admin.administrator_ID.login, "dodał administratora")
			except:
				pass
			
			return HttpResponseRedirect(reverse('consultations.views.admin_admin_list', args=(user_id,)))
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		return render_to_response('admin_addadmin.html', {'user_id':user_id, 'status':status, 'user_name':user_name, 'user_surname':user_surname}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_admin_delete_confirm(request, user_id, admin_id):
	if request.user.is_authenticated():
		admin = Administrator.objects.get(administrator_ID = user_id)
		user_name = admin.name
		user_surname = admin.surname
		return render_to_response('admin_admin_delete_confirm.html', {'user_id':user_id, 'admin_id':admin_id, 'user_name':user_name, 'user_surname':user_surname})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_admin_delete(request, user_id, admin_id):
	if request.user.is_authenticated():
		admin = Administrator.objects.get(administrator_ID = admin_id)
		admin.delete()
		
		try:
			admin = Administrator.objects.get(administrator_ID = user_id)
			log_file_append(admin.administrator_ID.login, "odebrał prawa administratora")
		except:
			pass
		
		return HttpResponseRedirect(reverse('consultations.views.admin_admin_list', args=(user_id,)))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
	
def download_instruction(request, tutor_id):
	if request.user.is_authenticated():
		from django.core.servers.basehttp import FileWrapper
		filepath = "/home/kons/instrukcja/instrukcja.pdf"
		filename = "instrukcja.pdf"
		sqlfile = open(filepath, "r")
		wrapper = FileWrapper(sqlfile)
		
		response = HttpResponse(wrapper, mimetype='application/force-download')
		response['Content-Disposition'] = 'attachment; filename=%s' % filename
		response['Content-Length'] = os.path.getsize(filepath)
		return response
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))

def add_error(request, tutor_id, place):
	if request.user.is_authenticated():
		status = ""
		place_string = ""
		user = User.objects.get(id = tutor_id)
		tutor = Tutor.objects.get(tutor_ID = user)
		user_name = tutor.name
		user_surname = tutor.surname
		
		if place == "1":
			place_string = "tutor_index"
		elif place == "2":
			place_string = "tutor_edit"
		elif place == "3":
			place_string = "tutor_consult_list"
		elif place == "4":
			place_string = "tutor_info_edit"
		elif place == "5":
			place_string = "tutor_consult_edit"
		elif place == "6":
			place_string = "tutor_consult_detail"
		elif place == "7":
			place_string = "tutor_add_consult"
		
		if request.POST:
			error = request.POST.get("blad")
			status = error_file_append(user.login, error, place_string)
		return render_to_response('add_error.html', {'tutor_id':tutor_id, 'status':status, 'user_name':user_name, 'user_surname':user_surname, 'place':place}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def admin_errorcheck(request, user_id):
	if request.user.is_authenticated():
		from django.core.servers.basehttp import FileWrapper
		filepath = "/home/kons/logs/errors"
		filename = "errors.txt"
		sqlfile = open(filepath, "r")
		wrapper = FileWrapper(sqlfile)
		
		response = HttpResponse(wrapper, mimetype='application/force-download')
		response['Content-Disposition'] = 'attachment; filename=%s' % filename
		response['Content-Length'] = os.path.getsize(filepath)
		return response
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))

def admin_logcheck(request, user_id):
	if request.user.is_authenticated():
		from django.core.servers.basehttp import FileWrapper
		filepath = "/home/kons/logs/logs"
		filename = "log.txt"
		sqlfile = open(filepath, "r")
		wrapper = FileWrapper(sqlfile)
		
		response = HttpResponse(wrapper, mimetype='application/force-download')
		response['Content-Disposition'] = 'attachment; filename=%s' % filename
		response['Content-Length'] = os.path.getsize(filepath)
		return response
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))

def get_table(request):
	colour = 0
	
	try:
		tutors_list = Tutor.objects.all()
	except:
		tutor_list = None
	
		
	consultations_data = []
	for tutor in tutors_list:
		t_id = tutor.id
		try:
			tutor_consultations = Consultation.objects.filter(tutor_ID = t_id)
		except:
			tutor_consultations = None
		try:
			tutor_localizations = Localization.objects.get(id = tutor.localization_ID_id)
		except:
			tutor_localizations = None
		try:
			tutor_info = InfoBoard.objects.get(tutor_id = t_id)
		except:
			tutor_info = InfoBoard()
			tutor_info.message = ""
		consult = consultationdata.ConsultationsData()
		consult.name = tutor.name
		consult.surname = tutor.surname
		consult.www = tutor.www
		consult.title = tutor.degree
		try:
			consult.localization = tutor_localizations.room
		except:
			pass
		consult.phone = tutor.phone[8:]
		today = date.today()
		consult.consultations = []
		raw_consultations = []
		for con in tutor_consultations:
			try:
				con_localization = Localization.objects.get(id = con.localization_ID_id)
			except:
				pass
			single_con = singleconsultationdata.SingleConsultationsData()
			single_con.day = con.day
			single_con.start_hour = con.start_hour
			single_con.week_type = con.week_type
			if (single_con.week_type == 'A'):
				single_con.week_type = " "
			single_con.end_hour = con.end_hour
			single_con.expiry_date = con.expiry_date
			single_con.start_minutes = con.start_minutes
			single_con.end_minutes = con.end_minutes
			single_con.building = con_localization.building
			single_con.room = con_localization.room
			raw_consultations.append(single_con)
		raw_consultations = sorted(raw_consultations, cmp=time_cmp)
		
		for con in raw_consultations:
			strcon = "".join("%s %s %s:%s-%s:%s [%s %s]")%(con.day, con.week_type, con.start_hour,con.start_minutes, con.end_hour,con.end_minutes, con_localization.room, con_localization.building )
			if (today>con.expiry_date):
				strcon = "".join("<font color=\"#808080\"> %s %s %s:%s-%s:%s [%s %s] (Nieaktualne) </font>")%(con.day, con.week_type, con.start_hour,con.start_minutes, con.end_hour,con.end_minutes, con_localization.room, con_localization.building )
			if (strcon ==""):
				strcon = " "
			consult.consultations.append(strcon)
		
		consult.info = tutor_info.message
		if (len(consult.info) > 100):
			consult.info_short = consult.info[:70] + u"... Najedź by wyświetlić całość"
		else:
			consult.info_short = consult.info
		
		consultations_data.append(consult)
		consult = None
	consultations_data = sort_tutors (consultations_data)
	for cons in consultations_data:
		cons.color_number = colour
		if colour:
			colour = False
		else:
			colour = True
	t = loader.get_template('table.html')
	c = Context({'consultations_data' : consultations_data, })
	return HttpResponse(t.render(c))
