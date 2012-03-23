from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse

def consultation_index(request):
	return HttpResponse("Lista wszystkich konsultacji")
	
def consultation_detail(request, consultation_id):
	return HttpResponse("Konsultacja %s"%consultation_id)

def tutors_index(request):
	return HttpResponse("Lista wszystkich wykladowcow")

def tutor_index(request, tutor_id):
	return HttpResponse("Strona wykladowcy %s"%tutor_id)
	
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
				login(request, user)
				state = "Zostales zalogowany"
				return HttpResponseRedirect(reverse('consultations.views.tutor_index', args=(15,)))
			else:
				state = "Twoje konto nie zostalo jeszcze aktywowane"
		else:
			state = "Login lub haslo nieprawidlowe"
		
	return render_to_response('logging.html', {'state':state, 'username':username}, context_instance = RequestContext(request))
