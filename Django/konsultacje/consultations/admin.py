#-*- coding: utf-8 -*--
from consultations.models import User, Student, Administrator, Assistant, Tutor, Consultation, Localization, InfoBoard
from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
	fieldsets = [
	('Personal Information', 
	{'fields' : ['login']}),
	('Info',
	{'fields' : ['last_login_date']
	}),
	]
	list_display = ('login',)
	list_filter = ['last_login_date']
	date_hierarchy = 'last_login_date'

#class LocalizationInline(admin.StackedInline):
#	model = Localization
#	extra = 1
	
class InfoBoardInline(admin.StackedInline):
	model = InfoBoard
	extra = 1

class TutorAdmin(admin.ModelAdmin):
	fieldsets = [
	('Personal Information', 
	{'fields' : 
	['degree',
	'tutor_ID',
	'name',
	'surname', 
	'institute']
	}),
	('Contact', 
	{'fields': 
	['phone', 
	'www', 
	'email',
	'localization_ID']
	}),
	]
	inlines = [InfoBoardInline]
	list_display = ('name', 'surname')
	search_fields = ['name']
	
class ConsultationAdmin(admin.ModelAdmin):
	fieldsets = [
	('time',
	{'fields' : ['start_hour', 'start_minutes', 'end_hour', 'end_minutes', 'day', 'week_type']}),
	('place',
	{'fields' : ['students_limit', 'tutor_ID', 'localization_ID']}),]
	list_display = ('start_hour', 'end_hour')

	
	

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Localization)
#admin.site.register(Administrator)
admin.site.register(Assistant)
admin.site.register(Tutor, TutorAdmin)
admin.site.register(Consultation, ConsultationAdmin)
