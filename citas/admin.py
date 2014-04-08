from django.contrib import admin
from citas.models import *
#from ajax_select import make_ajax_form
#from ajax_select.admin import AjaxSelectAdmin

admin.site.register(Paciente)
admin.site.register(Hora)
admin.site.register(Cita)
admin.site.register(Medico)
admin.site.register(Especialidad)
admin.site.register(Servicio)

