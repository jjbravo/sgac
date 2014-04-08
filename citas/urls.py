from django.conf.urls import patterns, include, url

from django.contrib import admin
#from ajax_select import urls as ajax_select_urls
from views import *
admin.autodiscover()
     
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'miweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #(r'^admin/lookups/', include(ajax_select_urls)),
   # url(r'^facturacion/',include('facturaciones.urls',namespace="facturacion")),
    

    url(r'^$','citas.views.index', name="index"),
  
    url(r'^login$',Auth_Login.as_view(), name="login"),
    url(r'^bienvenido/$','citas.views.bienvenido', name="bienvenido"),
    url(r'^logout$','citas.views.auth_Logout', name="logout"),
    url(r'^setHechoCita/(?P<pk>\d+)$','citas.views.setHechoCita', name="setHechoCita"),
    # url(r'^addmedico/$','citas.views.setMedico', name="setMedico"),
    url(r'^sinpermiso/$','citas.views.sinpermiso', name="sinpermiso"),
   # url(r'^setcita/$','citas.views.setCita', name="setCita"),
    #url(r'^setcita/$',SetCita.as_view(), name="setCita"),
    url(r'^especialidad/$',EspecialidadView.as_view(), name="especialidad"),
    url(r'^getMedicoAjax/$',GetMedicoAjaxView.as_view(), name="getMedicoAjax"),
    url(r'^getHoras/$',GetHoraDisponible.as_view(), name="getHoras"),

    
    # ++++++++++++++++++  AREA DE RECEPCION  ++++++++++++++++++++++++
   
    url(r'^buscar/$',permission_required('citas.recepcion',login_url='/sinpermiso')(GetPacienteView.as_view()), name="buscar"),
    url(r'^buscar/(?P<id_paciente>\d+)$',permission_required('citas.recepcion',login_url='/sinpermiso')(GetPacienteView.as_view()), name="buscarListCitas"),

    url(r'^buscarpaciente/$',BuscarPacienteList.as_view(), name="buscarpaciente"),
    #******************************************************************
    # CREAR PDF /(?P<fecha>\W+)/(?P<hora>\d+)/(?P<idmedico>\d+)
    # url(r'^pdf/$',GetCitaPacientePdf.as_view(), name="pdf"),
    # url(r'^descarga/$','citas.views.pdf', name="despdf"),
    
    #GENERA PDF DE CITA CREADA
    url(r'^addcita/imprimircita/(?P<id_paciente>\d+)/(?P<y>\d+)/(?P<m>\d+)/(?P<d>\d+)/(?P<hora>\d+)/(?P<idmedico>\d+)$','citas.views.imprimircita', name="imprimircita"),

    #******************************************************************
  
    url(r'^addcita/(?P<id_paciente>\d+)$',AddCitaView.as_view(), name="addCita"),
    
    url(r'^recepcion/$',permission_required('citas.recepcion',login_url='/sinpermiso')(RecepcionView.as_view()), name="recepcion"),
    url(r'^getpacientes/$','citas.views.getPaciente', name="getPaciente"),
    url(r'^getcita/$','citas.views.getCita', name="getCita"),
    #url(r'^pacientes/(?P<id_paciente>\d+)$','citas.views.getCitaPaciente', name="infopaciente"),
    url(r'^updatepaciente/(?P<pk>\d+)$',UpdatePaciente.as_view(), name="updatepaciente"),
    url(r'^addpaciente/$','citas.views.setpaciente', name="setpaciente"),
    url(r'^cancelarcita/(?P<pk>\d+)$',permission_required('citas.recepcion',login_url='/sinpermiso')(CancelarCitaView.as_view()), name="CancelarCita"),
    url(r'^cancelarcitaList/(?P<pk>\d+)$','citas.views.cancelarCita', name="CancelarCitaList"),
 
    # ++++++++++++++++++  AREA DE MEDICOS ++++++++++++++++++++++++
    url(r'^medicos/$',permission_required('citas.medico',login_url='/sinpermiso')(AreaMedicos.as_view()), name="areamedicos"),
    url(r'^medicos/citas/(?P<usuario_id>\d+)$',permission_required('citas.medico',login_url='/sinpermiso')(GetCitas.as_view()), name="getcitas"),
    url(r'^medicos/citas/$',permission_required('citas.medico',login_url='/sinpermiso')(GetCitas.as_view()), name="getcitasForFecha"),
    url(r'^medicos/citas/hechocitas/(?P<idcita>\d+)$','citas.views.hechoCitas', name="hechocitas"),
   

    # ++++++++++++++++++  AREA DE ADMINISTRACION ++++++++++++++++++++++++
    url(r'^administracion/$',permission_required('citas.medico',login_url='/sinpermiso')(AreaAdmin.as_view()), name="areadmin"),
    url(r'^administracion/citaslistmedicos/(?P<adm>\d+)$','citas.views.getCita', name="citaslistmedicos"),
    url(r'^administracion/usuarios/$','citas.views.getUsuarios', name="usuarios"),
    url(r'^administracion/medicos/$','citas.views.getMedico', name="getMedico"),
    url(r'^administracion/medicos/addmedico/$',permission_required('citas.medico',login_url='/sinpermiso')(AddMedicoView.as_view()), name="addmedico"),
    url(r'^administracion/medicos/adduserpassmedico/$','citas.views.addUserMedico', name="addUserMedico"),
    
    url(r'^administracion/medicos/listcitas/(?P<usuario_id>\d+)/(?P<adm>\d+)$',permission_required('citas.medico',login_url='/sinpermiso')(GetCitas.as_view()), name="getcitas"),
    url(r'^administracion/medicos/ver/(?P<pk>\d+)$','citas.views.getBuscarMedico', name="verMedico"),
    url(r'^administracion/medicos/buscar/$','citas.views.getBuscarMedico', name="buscarMedico"),
    url(r'^administracion/medicos/ver/activar/(?P<pk>\d+)$','citas.views.activarUsuarioMedico', name="activarMedico"),
    url(r'^administracion/medicos/ver/changePassM/(?P<pk>\d+)$','citas.views.changePassM', name="changePassM"),
    url(r'^administracion/medicos/buscar/update/(?P<pk>\d+)$',UpdateMedicoView.as_view(), name="medicoUpdate"),
   
    url(r'^administracion/usuarios/recepcionista/$',AddUsuariosView.as_view(), name="usuarioRolRecepcion"),
    url(r'^administracion/configuracion/especialidades/$',EspecialidadesView.as_view(), name="configEspecialidades"),
    url(r'^administracion/configuracion/especialidades/update/(?P<pk>\d+)$',UpdateEspecialidadesView.as_view(), name="configEspecialidadesUpdate"),
    url(r'^administracion/configuracion/especialidades/delete/(?P<pk>\d+)$',DeleteEspecialidadesView.as_view(), name="configEspecialidadesDelete"),
    url(r'^administracion/configuracion/servicios/$',ServiciosView.as_view(), name="configServicios"),
    url(r'^administracion/configuracion/servicios/update/(?P<pk>\d+)$',UpdateServicioView.as_view(), name="configServicioUpdate"),
    url(r'^administracion/configuracion/servicios/delete/(?P<pk>\d+)$',DeleteServicioView.as_view(), name="configServicioDelete"),

    url(r'^administracion/configuracion/horario/$',HorarioView.as_view(), name="configHorario"),
    url(r'^administracion/configuracion/horario/update/(?P<pk>\d+)$',UpdateHorarioView.as_view(), name="configHorarioUpdate"),
    url(r'^administracion/configuracion/horario/delete/(?P<pk>\d+)$',DeleteHorarioView.as_view(), name="configHorarioDelete"),
)
