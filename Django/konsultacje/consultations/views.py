#-*- coding: utf-8 -*--
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from consultations.models import *
from django.template import Context, loader
from consultations.models import User, Consultation, Localization
from django.contrib import auth


def consultation_index(request):
	consultations_list = Consultation.objects.all()
	tutors_list = Tutor.objects.all()
	localizations_list = Localization.objects.all()
	t = loader.get_template('index.html')
	c = Context({'localizations_list' : localizations_list, 'consultations_list': consultations_list, 'tutors_list' : tutors_list, })
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
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		tutor_id_from_table = tutor.id
		try:
			localization = Localization.objects.get(tutor_id = tutor_id_from_table)
		except:
			localization = None
			
		if request.POST:
			#zbiermay dane
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
			
		return render_to_response('tutor_detail.html', {'tutor_id':tutor_id, 'localization':localization, 'tutor':tutor}, context_instance = RequestContext(request))
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
			
		if request.POST:
			button_add_pushed = request.POST.get('dodaj')
			button_edit_pushed = request.POST.get('zmien')
			button_delete_pushed = request.POST.get('wykasuj')
			if button_add_pushed is not None:
				print "Dodawanie konsultacji"
				#tutaj dorobic trzeba dodawanie konsultacji
				#w URL jest tylko edycja wiec trzeba dodac URL(template ten sam co edit)
				#i w funkcji obsluzyc dodanie konsultacji. jak chcesz to ja moge zrobic
			if button_edit_pushed is not None:
				print "Edycja konsultacji"
				#Tutaj edycja konsultacji
				#Trzeba pomyslec jak to zrobic zeby z radiobuttona otworzyc wlasciwa
				#ale mysle ze to ta sama kwestia co z przyciskiem
			if button_delete_pushed is not None:
				print "Usuwanie konsultacji"
				#Tutaj usuwanie konsultacji
				#Tu dorobić URL + funkcje i tak samo z radiobuttonem pomyśleć trza
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
		
				if (Tutor.objects.get(id = tutor_id) == consultation.tutor_ID):
					if (request.POST.has_key('start_hour')):
						start_hour = request.POST.get('start_hour')
						consultation.start_hour = start_hour
					if (request.POST.has_key('end_hour')):
						end_hour = request.POST.get('end_hour')
						consultation.end_hour = end_hour
					if (request.POST.has_key('day')):
						day = request.POST.get('day')
						consultation.day = day
					#week_type = reques.POST.get('week_type')
					#students_limit = reques.POST.get('students_limit')
					#loc_room = request.POST.get('room')
					#loc_building = request.POST.get('building')
					#localization = Localization.objects.get(room = loc_room, building = loc_building)
					consultation.save()
					return render_to_response("edit_consultation.html", {'start_hour' : start_hour, 'end_hour' : end_hour, 'day' : day}, context_instance = RequestContext(request))
				else:
					return HttpResponse("Ta konsultacja nie przynalezy do tego tutora " )
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
