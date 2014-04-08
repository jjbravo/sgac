# -*- encoding: utf-8 -*-
import json
from citas.models import *
from citas.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
##++++++++++++
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required, permission_required

from django.core import serializers  # Serializar json para Ajax
##++++++++++++ VISTAS BASADAS EN CLASES
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView, View 
#from django.views.generic.base import 
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#from django.contrib.auth.models import User
# RENDER PARA PDF
from easy_pdf.views import PDFTemplateView
from easy_pdf.rendering import render_to_pdf
from django import http
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
from django.template import Context
from django.template.loader import get_template

from datetime import date
# FIN RENDER PARA PDF


# def pdf(request):
# 	if request.POST:
# 		result=StringIO.StringIO()
# 		pdf=pisa.CreatePDF(
# 			StringIO.StringIO(request.POST['data']),
# 			result
# 			)
# 		if not pdf.err:
# 			return http.HttpResponse(
# 				result.getvalue(),
# 				mimetype='application/pdf'
# 				)
# 	return http.HttpResponse('Ha ocurrido un error')	

def render_to_pdf(template_src,context_dict):
	template=get_template(template_src)
	context=Context(context_dict)
	html=template.render(context)
	result=StringIO.StringIO()
	pdf=pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")),result)
	if not pdf.err:
		return http.HttpResponse(result.getvalue(),content_type='application/pdf')
		
	return http.HttpResponse('Ha ocurrido un error')	



# class GetCitaPacientePdf(TemplateView):
# 	template_name='citas/pdf.html'

	# def get(self,request, *args, **kwargs):
	# 	paciente=Paciente.objects.filter(id_paciente=2)
	# 	return render_to_pdf(self.template_name,{'pacientes':paciente},encoding="utf-8",**kwargs)

	# def get_context_data(self, **kwargs):
	# 	return super(GetCitaPacientePdf, self).get_context_data(
	# 		pagesize="A4",
	# 		title="Listado de citas",
			
	# 		**kwargs	
	# 		)

		#return render_to_pdf(self.template_name,encoding=u'utf-8')


#*************** PARA CREAR PERMISOS PERSONALIZADOS *************
from django.contrib.auth.models import Group, Permission 
from django.contrib.contenttypes.models import ContentType 
# content_type= ContentType.objects.get_for_model(Cita)
# permission=Permission.objects.create(codename='recepcion',
#             name='Rol Recepcion',
#             content_type=content_type)

# content_type= ContentType.objects.get_for_model(Paciente)
# permission=Permission.objects.create(codename='medico',
#             name='Rol Medicos',
#             content_type=content_type)

# content_type= ContentType.objects.get_for_model(Medico)
# permission=Permission.objects.create(codename='administracion',
#              name='Rol Administracion',
#             content_type=content_type)

#************ FIN PARA CREAR PERMISOS PERSONALIZADOS ****************

def index(request):
	return render(request,'citas/index.html')

@login_required(login_url='/login')		
def bienvenido(request):
	usuario=request.user
	medico=Medico.objects.filter(usuario_id=usuario)

	return render(request,'citas/bienvenido.html',{'usuario':usuario,'medico':medico})						

class RecepcionView(TemplateView):
	"""Vista para los recepcionistas"""
	template_name='citas/recepcion.html'
	
	# def get(self, request, *args, **kwargs):
	# 	usuario=request.user
	# 	medico=Medico.objects.get(usuario_id=usuario)
	# 	return render(request, self.template_name,{'usuario':usuario,'medico':medico})

class AreaMedicos(TemplateView):
	template_name='citas/medicos.html'
	def get(self, request, *args, **kwargs):
		usuario=request.user
		medico=Medico.objects.filter(usuario_id=usuario)
		if not medico:
		 
			return HttpResponseRedirect(reverse_lazy('citas:getMedico'))
		return render(request, self.template_name,{'usuario':usuario,'medico':medico})

class AreaAdmin(TemplateView):
	template_name='citas/administracion.html'
	
@login_required(login_url='/login')		
@permission_required('citas.recepcion',login_url='/sinpermiso')
def getPaciente(request):
	paciente=Paciente.objects.all()
	#******************
	paginator=Paginator(paciente,8)

	page=request.GET.get('page')
	try:
		pacientes=paginator.page(page)
	except PageNotAnInteger:
		pacientes=paginator.page(1)
	except EmptyPage:
		pacientes=paginator.page(paginator.num_pages)

	#******************
	
	return render(request,'citas/getpaciente.html',{'pacientes':pacientes})


class Auth_Login(FormView):
	form_class=AuthForm
	template_name='citas/login.html'

	def get(self,request,*args,**kwargs):
		if not request.user.is_anonymous():
			return HttpResponseRedirect('/bienvenido')
		form=self.form_class()
		return render(request,self.template_name,{'form':form})
		
	def post(self,request,*args,**kwargs):
		form=self.form_class(request.POST)
		if form.is_valid():
			usuario=request.POST['username']	
			passwd=request.POST['password']	
			acceso=authenticate(username=usuario, password=passwd)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/bienvenido')
				else:
					noactivo="No tienes permisos para ingresar, contacta con el administrador"
					return render(request,'citas/login.html',{'form':form, 'noactivo':noactivo})
			else:
				errors="Nombre de Usuario o Contraseña incorrecto"
				
				return render(request,'citas/login.html',{'form':form, 'errors':errors})
		return render(request,self.template_name,{'form':form})
				
def auth_Logout(request):
	logout(request)
	return HttpResponseRedirect('/login')

@login_required(login_url='/login')		
def getCitaPaciente(request,id_paciente):
	paciente=Paciente.objects.get(id_paciente=id_paciente)
	estado=Estado_cita.objects.get(estado='Activo')
	cita=Cita.objects.filter(paciente_idpaciente=paciente, estado_cita_idestado=estado)
	

	return render(request,'citas/getpaciente.html',{'pacientes':paciente, 'cita':cita})
	#return render(request,'citas/getpaciente.html',{'pacientes':paciente})
	#cita=Cita.objects.get(paciente_idpaciente=id_paciente, estado='Pendiente')

@login_required(login_url='/login')		
def setHechoCita(request,pk):
	
	#html="<h4>Proyecto de ejemplo Django  => Recetario </h4> "
	#return HttpResponse(fechas)

	cita=Cita.objects.get(idcita=pk)
	estado=Estado_cita.objects.get(estado='Hecho')

	estado=Estado_cita.objects.get(idestado=estado)
	cita.estado_cita_idestado=estado
	cita.save()

	#getCita()
	#pacientes=Paciente.objects.all()

	#return render(request,'citas/getpaciente.html',{'pacientes':pacientes})
	return HttpResponseRedirect(reverse('citas:getCita'))

@login_required(login_url='/login')		
def cancelarCita(request,pk):
	
	#html="<h4>Proyecto de ejemplo Django  => Recetario </h4> "
	#return HttpResponse(fechas)

	cita=Cita.objects.get(idcita=pk)
	estado=Estado_cita.objects.get(estado='Cancelado')


	cita.estado_cita_idestado=estado
	cita.save()
	#*********************

	
	#getCita()
	#pacientes=Paciente.objects.all()

	#return render(request,'citas/getpaciente.html',{'pacientes':pacientes})
	return HttpResponse('ok')


@login_required(login_url='/login')	
def setpaciente(request):
	if request.method=='POST':
		form=PacienteForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('citas:getPaciente'))
	else:
		form=PacienteForm()
	return render(request, 'citas/setpaciente.html',{'form':form})			

		

@login_required(login_url='/login')	
#@permission_required('citas.leer_medico',login_url='/sinpermiso')	
def getMedico(request,adm=None):
	medicos=Medico.objects.all()
	paginator=Paginator(medicos,8)

	page=request.GET.get('page')
	try:
		medico=paginator.page(page)
	except PageNotAnInteger:
		medico=paginator.page(1)
	except EmptyPage:
		medico=paginator.page(paginator.num_pages)
	
	return render(request,'citas/getmedico.html',{'medico':medico})

@login_required(login_url='/login')		
def sinpermiso(request):
	return render(request,'citas/sinpermiso.html')

@login_required(login_url='/login')		
#@permission_required('citas.leer_cita',login_url='/sinpermiso')
def getCita(request):
	hoy=date.today()
	estado=Estado_cita.objects.get(estado='Activo')

	citas=Cita.objects.filter(estado_cita_idestado=estado,fecha__gte= hoy).order_by('fecha')
	#++++++++++++++++++++++ PAGINATIONS
	paginator=Paginator(citas,8)

	page=request.GET.get('page')
	try:
		cita=paginator.page(page)
	except PageNotAnInteger:
		cita=paginator.page(1)
	except EmptyPage:
		cita=paginator.page(paginator.num_pages)


	#++++++++++++++++++++++

	#return render(request,'citas/getcita.html',{ 'cita':cita,'usuario':usuario})
	# if adm:

	# 	return render(request,'citas/getcita.html',{ 'cita':cita})

	return render(request,'citas/getcita.html',{ 'cita':cita})

class GetCitas(ListView):
	template_name='citas/listcitas.html'
	def get(self, request, usuario_id=None, adm=None, **kwargs):  
		hoy=date.today()
		estado=Estado_cita.objects.get(estado='Activo')
		if adm:
			cita=Cita.objects.filter(medico_idmedico=usuario_id, fecha__gte= hoy, estado_cita_idestado=estado).order_by('hora_idhora')
			idmedico=Medico.objects.get(idmedico=usuario_id)
		else:	
			idmedico=Medico.objects.get(usuario_id=usuario_id)
			cita=Cita.objects.filter(medico_idmedico=idmedico, fecha= hoy, estado_cita_idestado=estado).order_by('hora_idhora')
		
		paginator=Paginator(cita,8)
		page=request.GET.get('page')
		try:
			citas=paginator.page(page)
		except PageNotAnInteger:
			citas=paginator.page(1)
		except EmptyPage:
			citas=paginator.page(paginator.num_pages)
		usuario=request.user

		if adm:
			
			return render(request,'citas/liscitasadmin.html',{'citas':citas,'usuario':usuario,'medico':idmedico})
		return render(request,self.template_name,{'citas':citas,'usuario':usuario,'medico':idmedico})
	
		#print request.GET['usuario_i']
		#if request.GET['fecha']:
		#	print request.GET['fecha']
		
	def post(self,request,*args,**kwargs):
		fecha= request.POST['fecha']
		usuario_id= request.POST['usuario_id']

		estado=Estado_cita.objects.get(estado='Activo')
		idmedico=Medico.objects.get(usuario_id=usuario_id)
		cita=Cita.objects.filter(medico_idmedico=idmedico, fecha= fecha, estado_cita_idestado=estado).order_by('hora_idhora')
		if not cita:
			return HttpResponse("null")
		data=serializers.serialize('json',cita,use_natural_keys=True)
		return HttpResponse(data,content_type='application/json')
		
@login_required(login_url='/login')		
def hechoCitas(request,idcita):
	
	#html="<h4>Proyecto de ejemplo Django  => Recetario </h4> "
	#return HttpResponse(fechas)
	
	cita=Cita.objects.get(idcita=idcita)
	estado=Estado_cita.objects.get(estado='Hecho')

	cita.estado_cita_idestado=estado
	cita.save()	

	return HttpResponse("ok")

## Prueba ajax jdango ***********************
class EspecialidadView(ListView):
	model=Especialidad
	template_name='citas/medicos.html'
	context_object_name='especialidad'


class GetPacienteView(View):
	formPaciente_class=GetPacienteForm
	#initial={'key':'value'}
	template_name='citas/buscarpaciente.html'
    #@method_decorator('citas.leer_paciente',login_url='/sinpermiso')	
	def get(self, request, id_paciente=None, **kwargs):
		form=self.formPaciente_class()

		#**************
		
		if id_paciente:
			#print id_paciente
			paciente=Paciente.objects.filter(id_paciente=id_paciente)
			hoy=date.today()
			estado=Estado_cita.objects.get(estado='Activo')
			citas=Cita.objects.filter(paciente_idpaciente=paciente, estado_cita_idestado=estado,fecha__gte= hoy).order_by('fecha')

			if not citas:
				nocitas="El paciente no tiene citas pendientes"
				return render(request,self.template_name,{'paciente':paciente,'form':form,'nocitas':nocitas})
					#return render(request,'citas/paciente_citas.html',{'paciente':paciente,'nocitas':nocitas})
			return render(request,self.template_name,{'paciente':paciente,'form':form,'citas':citas})

		#**************
		return render(request, self.template_name,{'form':form})
	

	
	
	def post(self, request, *args, **kwargs):
		form=self.formPaciente_class(request.POST)

		if form.is_valid():
			#print cita
			paciente=Paciente.objects.filter(documento=request.POST['documento'])
			hoy=date.today()
			estado=Estado_cita.objects.get(estado='Activo')
			citas=Cita.objects.filter(paciente_idpaciente=paciente, estado_cita_idestado=estado,fecha__gte= hoy).order_by('fecha')
			
				#print fecha_na.fecha_nacimiento
				#print edad
			if not paciente:
				noexiste="No existe un paciente registrado con el documento "
				return render(request,self.template_name,{'form':form,'noexiste':noexiste,'notdocument':request.POST['documento']})		
			if not citas:
				nocitas="El paciente no tiene citas pendientes"
				return render(request,self.template_name,{'paciente':paciente,'form':form,'nocitas':nocitas})
			
			return render(request,self.template_name,{'paciente':paciente,'form':form,'citas':citas})
		return render(request,self.template_name,{'form':form})
	
	

class BuscarPacienteList(View):
	formPaciente_class=GetPacienteForm
	template_name='citas/getpaciente.html'
	def get(self, request, *args, **kwargs):
		form=self.formPaciente_class()
		return render(request,self.template_name,{'form':form})
	def post(self, request, *args, **kwargs):
		form=self.formPaciente_class(request.POST)
		if form.is_valid():
			pacientes=Paciente.objects.filter(documento=request.POST['documento'])
			

			if not pacientes:
				noexiste="No existe un paciente registrado con el documento "
				return render(request,self.template_name,{'form':form,'noexiste':noexiste,'notdocument':request.POST['documento']})
			return render(request, self.template_name,{'pacientes':pacientes,'form':form})
		return render(request, self.template_name,{'form':form})	

	 
class AddCitaView(View):
	form_class=CitaForm
	template_name='citas/setcita.html'
	paciente=None
	
	def get(self, request, id_paciente, **kwargs):
		form=self.form_class()
		#print id_paciente
		self.paciente=Paciente.objects.get(id_paciente=id_paciente)

		return render(request,self.template_name,{'form':form,'paciente':self.paciente})
	
	def post(self, request, *args, **kwargs):
		form =self.form_class(request.POST)
		self.paciente=Paciente.objects.get(id_paciente=request.POST['paciente'])
		if form.is_valid():
			fecha=request.POST['fecha']
			idmedico=request.POST['medico']
			idpaciente=request.POST['paciente']
			idhora=request.POST['hora']
			idservicio=request.POST['servicio']

			hora=Hora.objects.get(idhora=idhora)
			medico=Medico.objects.get(idmedico=idmedico)
			paciente=Paciente.objects.get(id_paciente=idpaciente)
			servicio=Servicio.objects.get(idservicio=idservicio)

			cita=Cita()
			cita.fecha=fecha
			cita.hora_idhora=hora
			cita.medico_idmedico=medico
			cita.paciente_idpaciente=paciente
			cita.servicio_idservicio=servicio
			cita.save()
			hecho="Cita creada correctamente"
			#return HttpResponseRedirect(reverse('citas:buscar'))
			paciente=Paciente.objects.filter(id_paciente=idpaciente)
			cita=Cita.objects.filter(paciente_idpaciente=paciente, fecha=fecha, hora_idhora=hora, medico_idmedico=medico)
			hoy=date.today()
			estado=Estado_cita.objects.get(estado='Activo')
			citas=Cita.objects.filter(paciente_idpaciente=paciente, estado_cita_idestado=estado,fecha__gte= hoy).order_by('fecha')

			form=GetPacienteForm
			return TemplateResponse(request,'citas/buscarpaciente.html',{'form':form,'hecho':hecho, 'citas':citas, 'cita':cita,'paciente':paciente})

		return render(request,self.template_name,{'form':form,'paciente':self.paciente})	

def imprimircita(request,id_paciente,y,m,d,hora,idmedico):
	fecha=y+"-"+m+"-"+d
	#if request.GET:
	# print id_paciente
	# print  hora
	# print idmedico
	# print fecha
	hoy=date.today()

	cita=Cita.objects.filter(paciente_idpaciente=id_paciente, fecha=fecha, hora_idhora=hora, medico_idmedico=idmedico)
	return render_to_pdf('citas/imprimircita.html',{
	   	'pagesize':'A4',
	   	'title':'Comprobante de cita',
	    'citaprint':cita,'hoy':hoy,
	    })
	#return render(request,'citas/imprimircita.html',{'cita':cita})

class GetMedicoAjaxView(TemplateView):
	
	def get(self, request, *args, **kwargs):

		servicio= request.GET['id']
		if servicio:
		#medicos=Medico.objects.filter(especialidad_idespecialidad=idespecialidad)
			medicos=Medico.objects.filter(servicio__pk=servicio)
			#print medicos
			if not medicos:
			#	print "No hay datos"
				return HttpResponse(json.dumps('null'),content_type='application/json')

			data=serializers.serialize('json',medicos,
				fields=('nombres','apellidos'))
			return HttpResponse(data,content_type='application/json')
		return HttpResponse('null')

class GetHoraDisponible(TemplateView):
	
	def get(self, request, *args, **kwargs):
		fecha=request.GET['fecha']
		
		if fecha:
			id_medico=request.GET['id_medico']
		
			horaDisponible=Hora.objects.all().exclude(cita__in=Cita.objects.filter(
				fecha=fecha,
				medico_idmedico=id_medico
				))

			data=serializers.serialize('json',horaDisponible,fields=('hora'))
			return HttpResponse(data,content_type='application/json')
		return HttpResponse()


class CancelarCitaView(View):
	formPaciente_class=GetPacienteForm
	template_name='citas/buscarpaciente.html'

	#return render(request,self.template_name,{'form':form})
	
	def get(self, request, pk, **kwargs):
		cita=Cita.objects.get(idcita=pk)
		estado=Estado_cita.objects.get(estado='Cancelado')
		cita.estado_cita_idestado=estado
		cita.save()
		form=self.formPaciente_class()
		citacancelada="Cita medica cancelada"
		return render(request,self.template_name,{'form':form,'citacancelada':citacancelada})

class UpdatePaciente(UpdateView):	
	model=Paciente
	form_class=PacienteForm
	
	success_url='/getpacientes/'
	# template_name='citas/setpaciente.html'	
	# slug_field ='form'

# class UsuariosView(TemplateView):
# 	form_class=PerfilUsuario
# 	template_name='citas/usuarios.html'
# 	context_object_name='usuario'

	# def get(self, request, *args, **kwargs):
	# 	form=self.form_class()
	# 	return render(request, self.template_name,{'usuario':form})
# class UsuariosRecepcionView(TemplateView):
# 	template_name='citas/usuarios.html'
@permission_required('citas.administracion',login_url='/sinpermiso')
def getUsuarios(request):
	perfilusuario=PerfilUsuario.objects.all()
	#******************
	paginator=Paginator(perfilusuario,8)

	page=request.GET.get('page')
	try:
		perfilUsuario=paginator.page(page)
	except PageNotAnInteger:
		perfilUsuario=paginator.page(1)
	except EmptyPage:
		perfilUsuario=paginator.page(paginator.num_pages)

	#******************
	return render(request,'citas/usuarios.html',{'usuarios':perfilUsuario})

class AddUsuariosView(FormView):
	form_class=PerfilUsuarioForm
	template_name='citas/addusuarios.html'
	def get(self, request, *args, **kwargs):
		form=self.form_class()
		return render(request,self.template_name,{'form':form})
	def post(self, request, *args, **kwargs):
		form =self.form_class(request.POST)
		if form.is_valid():
			user=User.objects.create_user(request.POST['username'],request.POST['correo'],request.POST['password1'])
			usuario=PerfilUsuario()
			usuario.usuario=user
			usuario.documento=form.cleaned_data['documento']
			usuario.nombres=form.cleaned_data['nombres']
			usuario.apellidos=form.cleaned_data['apellidos']
			usuario.direccion=form.cleaned_data['direccion']
			usuario.ciudad=form.cleaned_data['ciudad']
			usuario.celular=form.cleaned_data['celular']
			usuario.telefono=form.cleaned_data['telefono']
			usuario.correo=form.cleaned_data['correo']
			usuario.save()
			registrado="Usuario registrado satisfactoriamente"
			return HttpResponseRedirect(reverse('citas:usuarios'))		
		return render(request,self.template_name,{'form':form})

class AddMedicoView(FormView):
	form_class=MedicoForm
	template_name='citas/addmedico.html'
	def get(self, request,*args, **kwargs):
		form=self.form_class()
		return render(request,self.template_name,{'form':form})
	def post(self, request, *args, **kwargs):	
		form=self.form_class(request.POST)
		
		if form.is_valid():
			#formM=Medico()
			
			medi=form.save(commit=False)

			
			
			
			medi.documento=request.POST['documento']
			medi.nombres=request.POST['nombres']
			medi.apellidos=request.POST['apellidos']
			medi.direccion=request.POST['direccion']
			medi.ciudad=request.POST['ciudad']
			medi.celular=request.POST['celular']
			medi.telefono=request.POST['telefono']

			medi.correo=request.POST['correo']
			especialidad=Especialidad.objects.get(pk=request.POST['especialidad'])
			medi.especialidad_idespecialidad=especialidad

			#medi.usuario=user		
			medi.save()
			form.save_m2m()
			

			medico=Medico.objects.get(documento=request.POST['documento'])
			form=UserMedicoForm
			print medico
			#return render(request,'citas/getmedico.html',{'medico':medico})
			return render(request,'citas/addUserMedico.html',{'form':form,'medico':medico})
		return render(request,self.template_name,{'form':form})

class UpdateMedicoView(UpdateView):
	model=Medico
	fields=['documento',
	'nombres',
	'apellidos',
	'direccion',
	'ciudad',
	'celular',
	'telefono',
	'correo','servicio'
	]
	success_url=reverse_lazy('citas:getMedico')

def addUserMedico(request):
	form=UserMedicoForm(request.POST)
	idmedico= request.POST['idmedico']
	medico=Medico.objects.filter(pk=idmedico)
	if form.is_valid():
		#form.save()
		user=User.objects.create_user(request.POST['username'],request.POST['correo'],request.POST['password1'])
		#usuario=PerfilUsuario()
		medico.usuario_id=user
		medico.save()
		#return HttpResponseRedirect(reverse('citas:getMedico'))
		return render(request,'citas/medico.html',{'medico':medico})
	return render(request,'citas/addUserMedico.html',{'form':form,'medico':medico})

def getBuscarMedico(request,pk=None):
	""" Lista el perfil completo de un medico seleccionado en la lista general """
	if request.method=='POST':
		if not request.POST['dato']:
			return HttpResponseRedirect(reverse_lazy('citas:getMedico'))
		medico=Medico.objects.filter(documento=request.POST['dato'])
		if not medico:
			noexiste="No existe un medico registrado con este documento "+request.POST['dato']
			medicos=Medico.objects.all()
			paginator=Paginator(medicos,8)

			page=request.GET.get('page')
			try:
				medico=paginator.page(page)
			except PageNotAnInteger:
				medico=paginator.page(1)
			except EmptyPage:
				medico=paginator.page(paginator.num_pages)
			return render(request,'citas/getmedico.html',{'medico':medico,'noexiste':noexiste})
			#return HttpResponseRedirect(reverse_lazy('citas:getMedico'))
			#return HttpResponseRedirect(reverse_lazy('citas:getMedico'))
		for med in medico:
			medicoUserId=med.usuario_id

		user=User.objects.get(pk=medicoUserId)
		return render(request,'citas/medico.html',{'medico':medico,'user':user})
	else:	
		medico=Medico.objects.filter(pk=pk)
		for med in medico:
			medicoUserId=med.usuario_id
			
			user=User.objects.get(pk=medicoUserId)
			return render(request,'citas/medico.html',{'medico':medico,'user':user})
	return HttpResponseRedirect(reverse_lazy('citas:getMedico'))
	#medico=Medico.objects.all()		
	#return render(request,'citas/getmedico.html',{'medico':medico})
def changePassM(request,pk):
	pass

def activarUsuarioMedico(request,pk):
	""" Activa o desactiva un usuario medico del sistema """
	medico=Medico.objects.get(pk=pk)
	user=User.objects.get(pk=medico.usuario_id)
	#print user.is_active
	if user.is_active:
		user.is_active=0
		user.save()
	else:
	
		user.is_active=1
		user.save()

	return HttpResponse(user.is_active)	
			
class EspecialidadesView(TemplateView):
	template_name='citas/especialidades.html'
	form_class=EspecialidadForm
	def get(self, request, *args, **kwargs):
		form=self.form_class()
		especialidad=self.getEspecialiadPaginator()
		print len(especialidad)
		tot = len(especialidad)
		return render(request,self.template_name,{'form':form,'especialidad':especialidad,'tot':tot})
	def post(self, request, *args, **kwargs):
		form=self.form_class(request.POST)
		
		especialidad=self.getEspecialiadPaginator()
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('citas:configEspecialidades'))
		return render(request,self.template_name,{'form':form,'especialidad':especialidad})

	def getEspecialiadPaginator(self):	
		especialidad=Especialidad.objects.all().order_by('pk')
		paginator=Paginator(especialidad,8)

		page=self.request.GET.get('page')
		try:
			especialid=paginator.page(page)
		except PageNotAnInteger:
			especialid=paginator.page(1)
		except EmptyPage:
			especialid=paginator.page(paginator.num_pages)

		return especialid


class UpdateEspecialidadesView(UpdateView):
	model=Especialidad
	fields=['especialidad']
	success_url=reverse_lazy('citas:configEspecialidades')

class DeleteEspecialidadesView(TemplateView):
	#model = Especialidad
	#success_url=reverse_lazy('citas:configEspecialidades')
	def get(self, request, pk, **kwargs):
		especialidad=Especialidad.objects.get(pk=pk)
		especialidad.delete()
		return HttpResponse('ok')

class ServiciosView(TemplateView):
	""" Clase para listar los servicios disponibles y para crear un nuevo servicio
	en la base de datos """

	template_name='citas/servicios.html'
	form_class=ServicioForm
	def get(self, request, *args, **kwargs):
		form=self.form_class()
		servicios=self.getServicioPaginator()

		return render(request,self.template_name,{'form':form,'servicios':servicios})
	def post(self, request, *args, **kwargs):
		form=self.form_class(request.POST)
		
		servicios=self.getServicioPaginator()
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('citas:configServicios'))
		return render(request,self.template_name,{'form':form,'servicios':servicios})

	def getServicioPaginator(self):	
		servicios=Servicio.objects.all().order_by('pk')
		paginator=Paginator(servicios,8)

		page=self.request.GET.get('page')
		try:
			servici=paginator.page(page)
		except PageNotAnInteger:
			servici=paginator.page(1)
		except EmptyPage:
			servici=paginator.page(paginator.num_pages)

		return servici


class UpdateServicioView(UpdateView):
	model=Servicio
	fields=['servicio']
	success_url=reverse_lazy('citas:configServicios')

class DeleteServicioView(TemplateView):
	#model = Especialidad
	#success_url=reverse_lazy('citas:configEspecialidades')
	def get(self, request, pk, **kwargs):
		servicio=Servicio.objects.get(pk=pk)
		servicio.delete()
		return HttpResponse('ok')

		

class HorarioView(TemplateView):
	""" Clase para listar los Horarios disponibles y para crear nuevas horas
	en la base de datos """

	template_name='citas/horarios.html'
	form_class=HoraForm
	def get(self, request, *args, **kwargs):
		form=self.form_class()
		horas=self.getHoraPaginator()

		return render(request,self.template_name,{'form':form,'horas':horas})
	def post(self, request, *args, **kwargs):
		form=self.form_class(request.POST)
		
		horas=self.getHoraPaginator()
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('citas:configHorario'))
		return render(request,self.template_name,{'form':form,'horas':horas})

	def getHoraPaginator(self):	
		horas=Hora.objects.all().order_by('hora')
		paginator=Paginator(horas,8)

		page=self.request.GET.get('page')
		try:
			hora=paginator.page(page)
		except PageNotAnInteger:
			hora=paginator.page(1)
		except EmptyPage:
			hora=paginator.page(paginator.num_pages)

		return hora


class UpdateHorarioView(UpdateView):
	model=Hora
	fields=['hora']
	success_url=reverse_lazy('citas:configHorario')

class DeleteHorarioView(TemplateView):
	#model = Especialidad
	#success_url=reverse_lazy('citas:configEspecialidades')
	def get(self, request, pk, **kwargs):
		hora=Hora.objects.get(pk=pk)
		hora.delete()
		return HttpResponse('ok')


