# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Cita(models.Model):
    idcita = models.AutoField(primary_key=True)
    fecha = models.DateField()
    estado_cita_idestado = models.ForeignKey('Estado_cita',db_column='estado_cita_idestado', default=1)
    hora_idhora = models.ForeignKey('Hora', db_column='hora_idhora')
    medico_idmedico = models.ForeignKey('Medico', db_column='medico_idmedico')
    paciente_idpaciente = models.ForeignKey('Paciente', db_column='paciente_idpaciente')
    servicio_idservicio=models.ForeignKey('Servicio',db_column='servicio_idservicio')
    def natural_key(self):
        return self.fecha.natural_key()
    class Meta:
        #managed = False
        db_table = 'cita'
        unique_together = ('fecha',)
        #permissions=("leer_cita","Leer Citas")
            
        

        
    def __unicode__(self):
        return str(self.hora_idhora)  
        
class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    documento = models.IntegerField(unique=True)
    nombres = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    fecha_nacimiento=models.DateField(verbose_name="Fecha de nacimiento")
    direccion = models.CharField(max_length=80)
    ciudad = models.CharField(max_length=45)
    celular = models.CharField(max_length=15)
    telefono = models.CharField(max_length=45, blank=True)
    correo=models.EmailField(blank=True)
    class Meta:
        #managed = False
        db_table = 'paciente'
       
    def __unicode__(self):
        return self.nombres + " " + self.apellidos 
    def natural_key(self):
        return (self.nombres+" "+self.apellidos) 

    def calcular_edad(self):
                import datetime
                nac = str(self.fecha_nacimiento)
                y,m,d = nac.split("-")
                date = datetime.date(int(y),int(m),int(d)-1)
                delta = datetime.date.today() - date
                #print delta
                try:
                    edad =  datetime.date.fromordinal(delta.days).year - 1
                except:
                    edad = None
                return edad 
class Hora(models.Model):
    idhora = models.AutoField(primary_key=True)
    hora = models.TimeField(help_text='Formato: hh:mm:ss')

    #frecuencia = models.IntegerField()
    #paciente_id_paciente = models.ForeignKey(Paciente, db_column='paciente_id_paciente')
    class Meta:
        #managed = False
        db_table = 'hora'

    def natural_key(self):
        return (self.hora)    
    def __unicode__(self):
        hora=str(self.hora)
        return hora

class Especialidad(models.Model):
    idespecialidad=models.AutoField(primary_key=True)
    especialidad=models.CharField(max_length=40, unique=True,error_messages={'unique':"Ya se encuentra registrada esta especialidad"})
    class Meta:
        db_table ='especialidad'
        
    def __unicode__(self):
        return self.especialidad
    def natural_key(self):
        return (self.especialidad) 
    
class Estado_cita(models.Model):
    idestado=models.AutoField(primary_key=True)
    estado=models.CharField(max_length=9)
    class Meta:
        db_table ='estado_cita'
        
    def __unicode__(self):
        return self.estado
    def natural_key(self):
        return (self.estado) 

class Servicio(models.Model):
    idservicio=models.AutoField(primary_key=True)
    servicio=models.CharField(max_length=20)
    valor = models.FloatField()

    class Meta:
        db_table ='servicio'
        
    def __unicode__(self):
        return self.servicio        
    def natural_key(self):
        return (self.servicio)    
class Medico(models.Model):
    idmedico=models.AutoField(primary_key=True)
    documento=models.IntegerField(unique=True)
    nombres=models.CharField(max_length=50)        
    apellidos=models.CharField(max_length=50)        
    direccion=models.CharField(max_length=80)        
    ciudad=models.CharField(max_length=50)        
    celular=models.CharField(max_length=15)
    telefono=models.CharField(max_length=15, blank=True)
    correo=models.EmailField()
    especialidad_idespecialidad=models.ForeignKey('Especialidad',db_column='especialidad_idespecialidad')
    servicio=models.ManyToManyField(Servicio)
    usuario=models.OneToOneField(User,blank=True)

    class Meta:
        db_table='medico'
        
    def natural_key(self):
        return (self.nombres+" "+self.apellidos)        
    def __unicode__(self):
        return self.nombres + " " + self.apellidos            
        #return str(self.usuario)    
           
class PerfilUsuario(models.Model):
    idusuario=models.AutoField(primary_key=True)
    documento=models.IntegerField(unique=True, error_messages={'unique':"Ya existe un usuario registrado con este documento"})
    nombres=models.CharField(max_length=50)        
    apellidos=models.CharField(max_length=50)        
    direccion=models.CharField(max_length=80)        
    ciudad=models.CharField(max_length=50)        
    celular=models.CharField(max_length=15)
    telefono=models.CharField(max_length=15, blank=True)
    correo=models.EmailField()  
    usuario=models.OneToOneField(User)
    
    class Meta:
        db_table='perfil_usuario'
        
            
    def __unicode__(self):
        return self.nombres + " " + self.apellidos    
