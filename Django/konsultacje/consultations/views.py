#-*- coding: utf-8 -*--
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from consultations.models import *
from django.template import Context, loader
from consultations.models import User, Consultation, Localization, InfoBoard
from django.contrib import auth
from consultations import consultationdata


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
			tutor_localizations = Localization.objects.get(tutor_id = t_id)
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
		consult.localization = "".join("%s, %s")%(tutor_localizations.building, tutor_localizations.room)
		consult.phone = tutor.phone
		consult.consultations = ""
		for con in tutor_consultations:
			strcon = "".join("%s %s %s-%s;")%(con.day, con.week_type, con.start_hour, con.end_hour)
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
			localization = Localization.objects.get(tutor_id = tutor_id_from_table)
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
		try:
			localization = Localization.objects.get(tutor_id = tutor_id_from_table)
		except:
			localization = None
			
		
		return render_to_response('consultations_detail.html', {'tutor_id':tutor_id, 'tutor_connsultations':consultations, 'localization':localization}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))
	
def edit_consultation(request, tutor_id, consultation_id):
	if request.user.is_authenticated():
			try:
				consultation = Consultation.objects.get(id = consultation_id)
			except:
				return HttpResponse("Nie istnieje taka konsultacja")
			else:
				start_hour = consultation.start_hour
				end_hour = consultation.end_hour
				day = consultation.day
				week_type = consultation.week_type
				students_limit = consultation.students_limit
				if (Tutor.objects.get(id = tutor_id) == consultation.tutor_ID):
					if request.POST:
						start_hour = request.POST.get('start_hour')
						consultation.start_hour = start_hour
	
						end_hour = request.POST.get('end_hour')
						consultation.end_hour = end_hour
			
						day = request.POST.get('day')
						consultation.day = day
						
						week_type = request.POST.get('week_type')
						consultation.week_type = request.POST.get('week_type')
						
						students_limit = request.POST.get('students_limit')
						consultation.students_limit = request.POST.get('students_limit')
						
						consultation.save()
					return render_to_response("edit_consultation.html", {'consultation_id' : consultation_id, 'tutor_id' : tutor_id, 'start_hour' : start_hour, 'end_hour' : end_hour, 'day' : day, 'week_type' : week_type, 'students_limit' : students_limit}, context_instance = RequestContext(request))
				else:
					return HttpResponse("Ta konsultacja nie przynalezy do tego tutora " )
	else:
		return render_to_response(reverse('consultations.views.authorization'))

def delete_consultation(request, tutor_id, consultation_id):
	try:
		consultation = Consultation.objects.get(id = consultation_id)
		consultation.delete()
		consultations_detail(request, tutor_id)
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
		try:
			localization = Localization.objects.get(tutor_id = tutor_id_from_table)
		except:
			localization = None
		return render_to_response('consultations_detail.html', {'tutor_id':tutor_id, 'tutor_connsultations':consultations, 'localization':localization}, context_instance = RequestContext(request))	
	except:
		return HttpResponse ("Blad")
	
def add_consultation(request, tutor_id):
	if request.user.is_authenticated():
		new_start_hour = ""
		new_end_hour = ""
		new_day = ""
		new_week_type = ""
		new_students_limit = ""
		
		if request.POST:
			
			new_start_hour = request.POST.get('start_hour')
			print new_start_hour

			new_end_hour = request.POST.get('end_hour')
			print new_end_hour
			new_day = request.POST.get('day')
			print new_day
			new_week_type = request.POST.get('week_type')
			print new_week_type
			new_students_limit = request.POST.get('students_limit')
			new_localization = Localization.objects.get(tutor_id = tutor_id)
			tutor = Tutor.objects.get(id = tutor_id)
			print "1"
			if (new_start_hour != "" and new_end_hour != "" and new_day != "" and new_week_type != "" and new_localization != ""):
				print "2"
				try:
					consultation = Consultation(tutor_ID = tutor, start_hour = new_start_hour, end_hour = new_end_hour, 
					day = new_day, week_type = new_week_type, localization_ID = new_localization)
					print "3"
				except:
					return HttpResponse("Nie mozna dodac konsultacji")
				if(new_students_limit != None):
					try:
						consultation.students_limit = new_students_limit
					except:
						pass
				#try:
				print "Dodano"
				consultation.save()
				#except:
				print "expcept"
				
				
			else:
				return HttpResponse("Nie mozna dodaccc konsultacji")
			
		return render_to_response("add_consultation.html", { 'tutor_id' : tutor_id, 'start_hour' : new_start_hour, 'end_hour' : new_end_hour, 'day' : new_day, 'week_type' : new_week_type, 'students_limit' : new_students_limit}, context_instance = RequestContext(request))
	else:
		return render_to_response(reverse('consultations.views.authorization'))
		
def authorization(request):	
	state = "Proszę się zalogować"
	username = password = ''
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
						state = "Użytkownik nie jest wykładowcą"
					else:
						login(request, user)
						state = "Zalogowano"
						return HttpResponseRedirect(reverse('consultations.views.tutor_index', args=(user_from_table.id,)))
			else:
				state = "Twoje konto nie zostalo jeszcze aktywowane"
		else:
			state = "Login lub hasło nieprawidłowe"
		
	return render_to_response('logging.html', {'state':state, 'username':username}, context_instance = RequestContext(request))
	
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('consultations.views.consultation_index'))
