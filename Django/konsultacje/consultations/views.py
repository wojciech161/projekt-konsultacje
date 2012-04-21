#-*- coding: utf-8 -*--
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from consultations.models import *
from django.template import Context, loader
from consultations.models import User, Consultation, Localization, InfoBoard, Assistant
from django.contrib import auth
from consultations import consultationdata
from consultations import singleconsultationdata
from datetime import date
import time

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
			print "jest"
		except:
			consultation_localization = None
			print "niema"
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
		consult.phone = tutor.phone
		consult.consultations = ""
		for con in tutor_consultations:
			try:
				con_localization = Localization.objects.get(id = con.localization_ID_id)
			except:
				pass
			today = date.today();
			if (today>con.expiry_date):
				strcon = ""
			else:
				strcon = "".join("%s %s %s.%s-%s.%s %s %s ;\n")%(con.day, con.week_type, con.start_hour, con.start_minutes, con.end_hour, con.end_minutes, con_localization.room, con_localization.building)
				
			consult.consultations += strcon
		consult.info = tutor_info.message
		consultations_data.append(consult)
		consult = None
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
			except:
				status = "Błąd: Nie mogę zmienić danych"
		return render_to_response('tutor_detail.html', {'tutor_id':tutor_id, 'localization':localization, 'tutor':tutor, 'status':status}, context_instance = RequestContext(request))
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
				print "jest"
			except:
				consultation_localization = None
				print "niema"
			consult = singleconsultationdata.SingleConsultationsData()
			consult.day = consultation.day
			consult.week_type = consultation.week_type
			consult.hours = "".join("%s.%s-%s.%s")%(consultation.start_hour, consultation.start_minutes, consultation.end_hour, consultation.end_minutes)
			consult.building = consultation_localization.building
			consult.room = consultation_localization.room
			consult.students_limit = consultation.students_limit
			consult.id = consultation.id
			today = date.today();
			if(today>consultation.expiry_date):
				consult.expiry = "expiry"
			else:
				consult.expiry = "not_expiry"
			consultations_data.append(consult)
			
		return render_to_response('consultations_detail.html', {'tutor_id':tutor_id, 'tutor_connsultations':consultations_data}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))

def edit_consultation(request, tutor_id, consultation_id):
	if request.user.is_authenticated():
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
				except:
					print "except"
					expiry_year = ""
					expiry_month = ""
					expiry_day = ""
				
				if (Tutor.objects.get(id = tutor_id) == consultation.tutor_ID):
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
							
						expiry_year = request.POST.get('expiry_year')
						expiry_month = request.POST.get('expiry_month')
						expiry_day = request.POST.get('expiry_day')
						new_expiry_date = date(	int(expiry_year), int(expiry_month), int(expiry_day))
						print new_expiry_date
						consultation.expiry_date = new_expiry_date
						consultation.save() 
						
						data = get_data_for_consultations_detail(tutor_id)#pobranie danych do obsługi strony consultations_detail
						return render_to_response('consultations_detail.html', data, context_instance = RequestContext(request))#wyświetlenie consultations_detail jeśli udało się zapisać nową konsultację	
						
					return render_to_response("edit_consultation.html", {'consultation_id' : consultation_id, 'tutor_id' : tutor_id, 'start_hour' : start_hour,'start_minutes' : start_minutes, 'end_hour' : end_hour, 'end_minutes' : end_minutes, 'day' : day, 'week_type' : week_type, 'students_limit' : students_limit, 'building' : building, 'room' : room, 'expiry_year' : expiry_year, 'expiry_month' : expiry_month, 'expiry_day' : expiry_day}, context_instance = RequestContext(request))
					
				else:
					return HttpResponse("Ta konsultacja nie przynalezy do tego tutora " )
	else:
		return render_to_response(reverse('consultations.views.authorization'))

def delete_consultation(request, tutor_id, consultation_id):
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
	if request.user.is_authenticated():
		new_start_hour = ""
		new_start_minutes = ""
		new_end_minutes = ""
		new_end_hour = ""
		new_day = ""
		new_week_type = ""
		new_students_limit = ""
		new_room = ""
		new_building = ""
		new_expiry_year = ""
		new_expiry_month = ""
		new_expiry_day = ""
		new_expiry_date = ""
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
			new_room = request.POST.get('room')
			new_building = request.POST.get('building')
			try:
				new_localization = Localization.objects.get(room = new_room, building = new_building)
			except:
				new_localization = Localization()
				new_localization.room = new_room
				new_localization.building = new_building
				new_localization.save()
			tutor = Tutor.objects.get(tutor_ID = tutor_id)
			
			new_expiry_year = request.POST.get('expiry_year')
			new_expiry_month = request.POST.get('expiry_month')
			new_expiry_day = request.POST.get('expiry_day')
			new_expiry_date = date(	int(new_expiry_year), int(new_expiry_month), int(new_expiry_day))
			print new_expiry_date
			
			
			#print "1"
			if (new_start_hour != "" and new_start_minutes != "" and new_end_hour != "" and new_end_minutes != "" and new_day != "" and new_week_type != "" and new_localization != ""):
				print "2"
				try:
					consultation = Consultation(tutor_ID = tutor, start_hour = new_start_hour, start_minutes = new_start_minutes, end_hour = new_end_hour, 
					end_minutes = new_end_minutes, day = new_day, week_type = new_week_type, localization_ID = new_localization, expiry_date = new_expiry_date)
					print "3"
				except:
					return HttpResponse("Nie mozna dodac konsultacji")
				if(new_students_limit != None):
					try:
						consultation.students_limit = new_students_limit
					except:
						pass

				print "Dodano"
				consultation.save()
				data = get_data_for_consultations_detail(tutor_id)#pobranie danych do obsługi strony consultations_detail
				return HttpResponseRedirect(reverse('consultations.views.consultations_detail', args=( tutor_id,)))
							
			else:
				return HttpResponse("Nie mozna dodac konsultacji")
				
		return render_to_response("add_consultation.html", { 'user_id':tutor_id, 'tutor_id' : tutor_id, 'start_hour' : new_start_hour, 'start_minutes' : new_start_minutes,  'end_hour' : new_end_hour, 'end_minutes' : new_end_minutes, 'day' : new_day, 'week_type' : new_week_type, 'students_limit' : new_students_limit, 'expiry_year' : new_expiry_year, 'expiry_month' : new_expiry_month, 'expiry_day' : new_expiry_day}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))
		
def authorization(request):	
	state = "Proszę się zalogować"
	username = password = ''
	user_is_tutor = False
	user_is_assistant = False
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				try:
					user_from_table = User.objects.get(login = username)
				except:
					state = """Użytkownik nie posiada konta w bazie wykładowców.
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
						
					if user_is_tutor and not(user_is_assistant):
						login(request, user)
						state = "Zalogowano"
						return HttpResponseRedirect(reverse('consultations.views.consultations_detail', args=(user_from_table.id,)))
					elif not(user_is_tutor) and user_is_assistant:
						login(request, user)
						state = "Zalogowano"
						return HttpResponseRedirect(reverse('consultations.views.assistant_index', args=(user_from_table.id,)))
					elif user_is_tutor and user_is_assistant:
						#Dorobic pole wyboru jakies
						pass
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
		tutor_id_from_table = tutor.id
		try:
			infoboard = InfoBoard.objects.get(tutor_id = tutor_id_from_table)
		except:
			infoboard = None
			
		if request.POST:
			#zbieramy dane
			try:
				info = request.POST.get('Informacja')
				print info
				#zapisujemy zmiany w bazie
				infoboard.message = info
				infoboard.save()
				status = "Dane zostały zmienione"
			except:
				status = "Błąd: Nie mogę zmienić danych"
		return render_to_response('infoboard_edit.html', {'tutor_id':tutor_id, 'infoboard':infoboard}, context_instance = RequestContext(request))
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
				print tutor.localization_ID_id
				tutor_localizations = None
			try:
				tutor_info = InfoBoard.objects.get(tutor_id = t_id)
			except:
				tutor_info = InfoBoard()
				tutor_info.message = ""
			consult = consultationdata.ConsultationsData()
			consult.tutor_id = tutor.tutor_ID_id
			consult.name = tutor.name
			consult.surname = tutor.surname
			consult.www = "\"http://" + tutor.www + "\""
			consult.title = tutor.degree
			consult.localization = "".join("%s, %s")%(tutor_localizations.building, tutor_localizations.room)
			consult.phone = tutor.phone
			consult.consultations = ""
			today = date.today();
			for con in tutor_consultations:
				strcon = "".join("%s %s %s-%s;")%(con.day, con.week_type, con.start_hour, con.end_hour)
				consult.consultations += strcon
				if(today>con.expiry_date):
					consult.expiry = "expiry"
				else:
					consult.expiry = "not_expiry"
			consult.info = tutor_info.message
			consultations_data.append(consult)
			consult = None
		t = loader.get_template('assistant_index.html')
		c = Context({'user_id' : user_id, 'consultations_data' : consultations_data, })
		return HttpResponse(t.render(c))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_consultations_delete_confirm(request, user_id):
	if request.user.is_authenticated():
		return render_to_response('assistant_consultations_delete_confirm.html', {'user_id':user_id})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_consultations_delete(request, user_id):
	if request.user.is_authenticated():
		
		consult_list = Consultation.objects.all()
		for c in consult_list:
			c.delete()
		
		return render_to_response('assistant_index.html', {'user_id':user_id})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_tutor_edit(request, user_id, tutor_id):
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
				
				print title + "\n"
				print name + "\n"
				print surname + "\n"
				print room + "\n"
				print building + "\n"
				
				localization.room = room
				localization.building = building
				localization.save()
				status = "Dane zostały zmienione"
				return HttpResponseRedirect(reverse('consultations.views.assistant_index', args=(user_id,)))
			except:
				status = "Błąd: Nie mogę zmienić danych"
		return render_to_response('assistant_tutor_edit.html', {'user_id':user_id, 'tutor_id':tutor_id, 'localization':localization, 'tutor':tutor, 'status':status}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
	
def assistant_tutor_delete_confirm(request, user_id, tutor_id):
	if request.user.is_authenticated():
		return render_to_response('assistant_tutor_delete_confirm.html', {'user_id':user_id, 'tutor_id':tutor_id})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_tutor_delete(request, user_id, tutor_id):
	if request.user.is_authenticated():
		
		tutor = Tutor.objects.filter(tutor_ID = tutor_id)
		tutor.delete()
		
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
			consult.hours = "".join("%s.%s-%s.%s")%(consultation.start_hour, consultation.start_minutes, consultation.end_hour, consultation.end_minutes)
			consult.building = consultation_localization.building
			consult.room = consultation_localization.room
			consult.students_limit = consultation.students_limit
			consult.id = consultation.id
			today = date.today();
			if(today>consultation.expiry_date):
				consult.expiry = "expiry"
			else:
				consult.expiry = "not_expiry"
			consultations_data.append(consult)
			
		return render_to_response('assistant_consultations_list.html', {'user_id':user_id, 'tutor_id':tutor_id, 'tutor_connsultations':consultations_data}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))
		
def assistant_consultation_edit(request, user_id, tutor_id, consultation_id):
	if request.user.is_authenticated():
		try:
			tutor = Tutor.objects.get(tutor_ID = tutor_id)
			consult = Consultation.objects.get(id = consultation_id)
			localization = Localization.objects.get(id = consult.localization_ID_id)
			print tutor
			print consult
			print localization
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
			expiry_year = ""
			expiry_month = ""
			expiry_day = ""
			try:
				expiry_year = consult.expiry_date.year
				expiry_month = consult.expiry_date.month
				expiry_day = consult.expiry_date.day
			except:
				pass
				print "exceptiiui"
				
		
		if request.POST:
			start_hour = request.POST.get('start_hour')
			start_minutes = request.POST.get('start_minutes')
			end_hour = request.POST.get('end_hour')
			end_minutes = request.POST.get('end_minutes')
			day = request.POST.get('day')
			week_type = request.POST.get('week_type')
			students_limit = request.POST.get('students_limit')
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
				expiry_year = request.POST.get('expiry_year')
				expiry_month = request.POST.get('expiry_month')
				expiry_day = request.POST.get('expiry_day')
				new_expiry_date = date(	int(expiry_year), int(expiry_month), int(expiry_day))
				print new_expiry_date
				consult.expiry_date = new_expiry_date
			except:
				pass
			consult.save()
			localization.save()
			
			return HttpResponseRedirect(reverse('consultations.views.assistant_consultation_list', args=(user_id, tutor_id,)))
			
		return render_to_response("assistant_consultation_edit.html", {'user_id':user_id, 'consultation_id' : consultation_id, 'tutor_id' : tutor_id, 'start_hour' : start_hour,'start_minutes' : start_minutes, 'end_hour' : end_hour, 'end_minutes' : end_minutes, 'day' : day, 'week_type' : week_type, 'students_limit' : students_limit, 'building' : building, 'room' : room, 'expiry_year' : expiry_year, 'expiry_month' : expiry_month, 'expiry_day' : expiry_day}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))
		
def assistant_consultation_delete_confirm(request, user_id, tutor_id, consultation_id):
	if request.user.is_authenticated():
		return render_to_response('assistant_consultation_delete_confirm.html', {'user_id':user_id, 'tutor_id':tutor_id, 'consultation_id':consultation_id})
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_consultation_delete(request, user_id, tutor_id, consultation_id):
	if request.user.is_authenticated():
		
		consult = Consultation.objects.get(id = consultation_id)
		consult.delete()
		return HttpResponseRedirect(reverse('consultations.views.assistant_consultation_list', args=(user_id, tutor_id,)))
	
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
		
def assistant_consultation_add(request, user_id, tutor_id):
	if request.user.is_authenticated():
		new_start_hour = ""
		new_start_minutes = ""
		new_end_minutes = ""
		new_end_hour = ""
		new_day = ""
		new_week_type = ""
		new_students_limit = ""
		new_room = ""
		new_building = ""
		new_expiry_year = ""
		new_expiry_month = ""
		new_expiry_day = ""
		new_expiry_date = ""
		
		if request.POST:
			
			new_start_hour = request.POST.get('start_hour')
			new_start_minutes = request.POST.get('start_minutes')
			new_end_hour = request.POST.get('end_hour')
			new_end_minutes = request.POST.get('end_minutes')
			new_day = request.POST.get('day')
			new_week_type = request.POST.get('week_type')
			new_students_limit = request.POST.get('students_limit')
			new_room = request.POST.get('room')
			new_building = request.POST.get('building')

			new_localization = Localization()
			new_localization.room = new_room
			new_localization.building = new_building
			new_localization.save()
			
			tutor = Tutor.objects.get(tutor_ID_id = tutor_id)
			
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
			
			new_expiry_year = request.POST.get('expiry_year')
			new_expiry_month = request.POST.get('expiry_month')
			new_expiry_day = request.POST.get('expiry_day')
			new_expiry_date = date(	int(new_expiry_year), int(new_expiry_month), int(new_expiry_day))
			new_consultation.expiry_date = new_expiry_date
			
			new_consultation.save()
			print "save"
			return HttpResponseRedirect(reverse('consultations.views.assistant_consultation_list', args=(user_id, tutor_id,)))
			
		return render_to_response("assistant_consultation_add.html", { 'user_id':user_id, 'tutor_id' : tutor_id, 'start_hour' : new_start_hour, 'start_minutes' : new_start_minutes,  'end_hour' : new_end_hour, 'end_minutes' : new_end_minutes, 'day' : new_day, 'week_type' : new_week_type, 'students_limit' : new_students_limit, 'room' : new_room, 'building' : new_building, 'expiry_year' : new_expiry_year, 'expiry_month' : new_expiry_month, 'expiry_day' : new_expiry_day}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))
		
def assistant_consultation_deleteall_confirm(request, user_id, tutor_id):
	if request.user.is_authenticated():
		return render_to_response('assistant_consultation_deleteall_confirm.html', {'user_id':user_id, 'tutor_id':tutor_id})
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
				
				print tutor.tutor_ID
				print tutor.degree
				print tutor.name
				print tutor.surname
				print tutor.institute
				print tutor.phone
				print tutor.email
				print tutor.www
				print tutor.localization_ID
				
				tutor.save()

				status = "Dodano użytkownika"
			except:
				status = "Błąd: Nie mogę dodać użytkownika"
		return render_to_response('assistant_addtutor.html', {'user_id':user_id, 'user_login':login, 'localization':localization, 'tutor':tutor, 'status':status}, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
