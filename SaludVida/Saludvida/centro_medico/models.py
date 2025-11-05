from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class medico(models.Model):
    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=12, unique=True)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True, null=True)
    correo = models.EmailField()

    def __str__(self):
        return f"{self.nombre} - {self.especialidad }"
    
class paciente(models.Model):
    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=12, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField()
    sexo=[
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]                   
    def __str__(self):
        return f"{self.nombre} - {self.rut}"
    
class cita(models.Model):
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(medico, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)
    fecha_cita = models.DateField()
    hora_cita = models.TimeField()
    observaciones = models.TextField(blank=True, null=True)
    class Meta:
        unique_together = ('medico', 'fecha_cita', 'hora_cita')
        ordering = ['fecha_cita', 'hora_cita']
   
    def __str__(self):
        return f"Cita de {self.paciente.nombre} con {self.medico.nombre} el {self.fecha_cita} a las {self.hora_cita}"
