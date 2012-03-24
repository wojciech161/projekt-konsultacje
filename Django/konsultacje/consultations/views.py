from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from consultations.models import Tutor
from django.template import Context, loader
from consultations.models import User, Consultation


def consultation_index(request):
	consultations_list = Consultation.objects.all()
	tutors_list = Tutor.objects.all()
	localizations_list = Localization.objects.all()
	t = loader.get_template('index.html')
	c = Context({'localizations_list' : localizations_list, 'consultations_list': consultations_list, 'tutors_list' : tutors_list, })
	return HttpResponse(t.render(c))
	
def consultation_detail(request, consultation_id):
	return HttpResponse("Konsultacja %s"%consultation_id)

def tutors_index(request):
	tutors_list = Tutor.objects.all().order_by('name')[:5]
	t = loader.get_template('index.html')
	c = Context({'tutors_list': tutors_list,})
	return HttpResponse(t.render(c))
	
def tutor_index(request, tutor_id):
	if request.user.is_authenticated():
		tutor_connsultations = Consultation.objects.filter(tutor_ID = tutor_id)
		tutor = Tutor.objects.get(tutor_ID = tutor_id)
		return HttpResponse("Strona wykladowcy %s"%tutor_id)
	else:
		return HttpResponseRedirect(reverse('consultations.views.authorization'))
	
def tutor_detail(request, tutor_id):
	return HttpResponse("Edycja wykladowcy %s"%tutor_id)
	
def tutor_consultations(request, tutor_id):
	return HttpResponse("Tu tutor %s bedzie mogl zobaczyc liste swoich konsultacji i ile osob jest zapisanych do niego(pozniej)"%tutor_id)
	
def edit_consultation(request, tutor_id, consultation_id):
	return HttpResponse("Edycja konsultacji %s"%consultation_id)

def authorization(request):	
	state = "Prosze sie zalogowac"
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
					state = "Brak konta w bazie danych"
				else:
					try:
						tutor_from_table = Tutor.objects.get(tutor_ID = user_from_table.id)
					except:
						state = "Nie jestes wykladowca"
					else:
						login(request, user)
						state = "Zostales zalogowany"
						return HttpResponseRedirect(reverse('consultations.views.tutor_index', args=(user_from_table.id,)))
			else:
				state = "Twoje konto nie zostalo jeszcze aktywowane"
		else:
			state = "Login lub haslo nieprawidlowe"
		
	return render_to_response('logging.html', {'state':state, 'username':username}, context_instance = RequestContext(request))
