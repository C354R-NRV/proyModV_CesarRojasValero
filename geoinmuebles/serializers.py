from rest_framework import serializers
from .models import GeoreferenciaInmueble

class GeoreferenciaInmuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoreferenciaInmueble
        fields = '__all__'