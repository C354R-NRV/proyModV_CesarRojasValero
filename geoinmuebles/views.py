from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import GeoreferenciaInmueble, Inmueble
from .serializers import GeoreferenciaInmuebleSerializer

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from geopy.geocoders import Nominatim

class GeoreferenciaInmuebleViewSet(viewsets.ModelViewSet):
    queryset = GeoreferenciaInmueble.objects.all()
    serializer_class = GeoreferenciaInmuebleSerializer

@api_view(['GET'])
def georeferencias_altitud_mayor(request, altitud):
    georeferencias = GeoreferenciaInmueble.objects.filter(altitud__gt=altitud)
    serializer = GeoreferenciaInmuebleSerializer(georeferencias, many=True)
    return Response(serializer.data)

class GeoreferenciaInmuebleAltitudMinimaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GeoreferenciaInmuebleSerializer

    def get_queryset(self):
        altitud_minima = self.request.query_params.get('altitud_minima', None)
        if altitud_minima is not None:
            return GeoreferenciaInmueble.objects.filter(altitud__gte=altitud_minima)
        return GeoreferenciaInmueble.objects.all()

class GeoreferenciaInmuebleZonaEspecificaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GeoreferenciaInmuebleSerializer

    def get_queryset(self):
        zona = self.request.query_params.get('zona', None)
        if zona is not None:
            return GeoreferenciaInmueble.objects.filter(numero_inmueble__especificaciontecnica__zona_clasificacion=zona)
        return GeoreferenciaInmueble.objects.all()
    
def geocode_inmueble(request, numero_inmueble):
    inmueble = get_object_or_404(Inmueble, numero_inmueble=numero_inmueble)
    geolocator = Nominatim(user_agent="geoinmueble_app")
    #location = geolocator.geocode(f"{inmueble.direccion}, La Paz, Bolivia")
    location = geolocator.geocode(inmueble.direccion)
    
    if location:
        georeferencia, created = GeoreferenciaInmueble.objects.get_or_create(numero_inmueble=inmueble)
        georeferencia.latitud = location.latitude
        georeferencia.longitud = location.longitude
        georeferencia.save()
        
        response = {
            'numero_inmueble': inmueble.numero_inmueble,
            'direccion': inmueble.direccion,
            'latitud': georeferencia.latitud,
            'longitud': georeferencia.longitud,
        }
        return JsonResponse(response)
    else:
        return JsonResponse({"error": "Direccion no encontrada ["+inmueble.direccion+"]"}, status=404)