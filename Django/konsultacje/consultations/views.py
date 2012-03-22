from django.http import HttpResponse

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
	return HttpResponse("Ekran logowania")
