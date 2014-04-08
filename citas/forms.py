#encoding:utf-8
from django.forms import ModelForm
from django import forms
from citas.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PacienteForm(forms.ModelForm):
	#id_paciente = models.AutoField(primary_key=True)
    documento = forms.IntegerField()
    nombres = forms.CharField(max_length=45)
    apellidos = forms.CharField(max_length=45)
    fecha_nacimiento=forms.DateField(widget=forms.TextInput(attrs={'id':'datepicker'}))
    direccion = forms.CharField(max_length=80)
    ciudad = forms.CharField(max_length=45)
    celular = forms.CharField(max_length=15)
    telefono = forms.CharField(max_length=45)
    correo=forms.EmailField()
    class Meta:
		model=Paciente
		fields=[
		'documento',
		'nombres',
		'apellidos',
		'fecha_nacimiento',
		'direccion',
		'ciudad',
		'celular',
		'telefono',
		'correo'
		]


# class CitaForm(forms.ModelForm):
# 	class Meta:
# 		model=Cita

class EspecialidadForm(forms.ModelForm):
	class Meta:
		model=Especialidad

class HoraForm(forms.ModelForm):
	class Meta:
		model=Hora

class ServicioForm(forms.ModelForm):
	class Meta:
		model=Servicio 


class CitaForm(forms.Form):
	#especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all())
	servicio=forms.ModelChoiceField(queryset=Servicio.objects.all())
	medico = forms.ModelChoiceField(queryset=Medico.objects.all())
	fecha=forms.DateField(
			widget=forms.TextInput(attrs={'id':'datepicker'})
		)
	
	hora=forms.ModelChoiceField(queryset=Hora.objects.all())
	class Meta:
		fields=['fecha','estado_cita_idestado','hora_idhora','medico_idmedico']
		
class GetPacienteForm(forms.Form):
	documento= forms.IntegerField()
	class Meta:
		fields=['documento']

class UserMedicoForm(UserCreationForm):
	class Meta:
		model=Medico
		fields=['idmedico',]


# class MedicoForm(forms.ModelForm):
# 	class Meta:
# 		model=Medico
class MedicoForm(forms.ModelForm):
	documento=forms.IntegerField()
	nombres=forms.CharField(max_length=50)        
	apellidos=forms.CharField(max_length=50)        
	direccion=forms.CharField(max_length=80)        
	ciudad=forms.CharField(max_length=50)        
	celular=forms.CharField(max_length=15)
	telefono=forms.CharField(max_length=15, required=False)
	correo=forms.EmailField()
	#usuario=forms.IntegerField()
	especialidad=forms.ModelChoiceField(queryset=Especialidad.objects.all())
	servicio=forms.ModelMultipleChoiceField(queryset=Servicio.objects.all())
	class Meta:
		model=Medico
		fields=['documento',
 			'nombres',
 			'apellidos',
 			'direccion',
 			'ciudad',
 			'celular',
 			'telefono',
 			'correo',
 			'especialidad',
 			'servicio']
 	#	exclude=('usuario',)	


class PerfilUsuarioForm(UserCreationForm):
	documento=forms.IntegerField()
	nombres=forms.CharField(max_length=50)        
	apellidos=forms.CharField(max_length=50)        
	direccion=forms.CharField(max_length=80)        
	ciudad=forms.CharField(max_length=50)        
	celular=forms.CharField(max_length=15)
	telefono=forms.CharField(max_length=15, required=False)
	correo=forms.EmailField()
	class Meta:
		model=PerfilUsuario
 		fields=['documento',
 			'nombres',
 			'apellidos',
 			'direccion',
 			'ciudad',
 			'celular',
 			'telefono',
 			'correo']		

class AuthForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(max_length=254,label="Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)


