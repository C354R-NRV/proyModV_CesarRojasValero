from django.db import models
from django.core.exceptions import ValidationError 

import re

class Inmueble(models.Model):
    numero_inmueble = models.AutoField(primary_key=True)
    ci_propietario = models.CharField(max_length=10)
    nombre_propietario = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)

    def clean(self):
        if not re.match(r'^\d{7,8}$', self.ci_propietario):
            raise ValidationError('CI Propietario debe tener entre 7 y 8 dígitos numéricos.')

    def __str__(self):
        return f"{self.numero_inmueble} - {self.nombre_propietario}"

class Pago(models.Model):
    idpago = models.AutoField(primary_key=True)
    numero_inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    gestion_pago = models.PositiveIntegerField()
    estado_pago = models.CharField(max_length=50)

    def clean(self):
        if len(str(self.gestion_pago)) != 4:
            raise ValidationError('Gestión de pago debe tener 4 dígitos.')

    def __str__(self):
        return f"{self.idpago} - {self.gestion_pago}"

class GeoreferenciaInmueble(models.Model):
    idgeoreferencia = models.AutoField(primary_key=True)
    numero_inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    
    latitud = models.FloatField()
    longitud = models.FloatField()

    altitud = models.FloatField()

    def __str__(self):
        return f"{self.idgeoreferencia} - {self.numero_inmueble}"

class EspecificacionTecnica(models.Model):
    idtecnico = models.AutoField(primary_key=True)
    numero_inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    area_construccion = models.FloatField()
    area_terreno = models.FloatField()
    zona_clasificacion = models.CharField(max_length=1)

    def clean(self):
        if self.zona_clasificacion not in ['A', 'B', 'C']:
            raise ValidationError('Zona Clasificación debe ser A, B o C.')

    def __str__(self):
        return f"{self.idtecnico} - {self.numero_inmueble}"
        