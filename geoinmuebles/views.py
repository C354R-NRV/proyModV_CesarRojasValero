from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import GeoreferenciaInmueble
from .serializers import GeoreferenciaInmuebleSerializer

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