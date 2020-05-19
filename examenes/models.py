from django.conf import settings
from django.db import models
from django.utils import timezone


class Examen(models.Model):
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tema = models.CharField(max_length=200)
    fecha = models.DateTimeField(default=timezone.now)
    preguntas = models.TextField(blank=True, max_length=10000, default="")
    respuestas = models.TextField(blank=True, max_length=10000, default="")
    opcional = models.TextField(blank=True, max_length=10000, default="")
    crear_pregunta = models.TextField(blank=True, max_length=10000, default="")

class ExamenResuelto(models.Model):
    numero_cuenta = models.TextField(blank=True, max_length=10000, default="")
    tema = models.TextField(blank=True, max_length=10000, default="")
    tiempo = models.TextField(blank=True, max_length=10000, default="")
    status_gsheet = models.TextField(blank=True, max_length=10000, default="")
    calificacion = models.TextField(blank=True, max_length=10000, default="")
    pregunta1 = models.TextField(blank=True, max_length=10000, default="")
    respuesta1_correcta = models.TextField(blank=True, max_length=10000, default="")
    respuesta1_alumno = models.TextField(blank=True, max_length=10000, default="")
    respuesta1_calif = models.TextField(blank=True, max_length=10000, default="")
    pregunta2 = models.TextField(blank=True, max_length=10000, default="")
    respuesta2_correcta = models.TextField(blank=True, max_length=10000, default="")
    respuesta2_alumno = models.TextField(blank=True, max_length=10000, default="")
    respuesta2_calif = models.TextField(blank=True, max_length=10000, default="")
    pregunta3 = models.TextField(blank=True, max_length=10000, default="")
    respuesta3_correcta = models.TextField(blank=True, max_length=10000, default="")
    respuesta3_alumno = models.TextField(blank=True, max_length=10000, default="")
    respuesta3_calif = models.TextField(blank=True, max_length=10000, default="")
    pregunta4 = models.TextField(blank=True, max_length=10000, default="")
    respuesta4_correcta = models.TextField(blank=True, max_length=10000, default="")
    respuesta4_alumno = models.TextField(blank=True, max_length=10000, default="")
    respuesta4_calif = models.TextField(blank=True, max_length=10000, default="")
    pregunta5 = models.TextField(blank=True, max_length=10000, default="")
    respuesta5_correcta = models.TextField(blank=True, max_length=10000, default="")
    respuesta5_alumno = models.TextField(blank=True, max_length=10000, default="")
    respuesta5_calif = models.TextField(blank=True, max_length=10000, default="")
