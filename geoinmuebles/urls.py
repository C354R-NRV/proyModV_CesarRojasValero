from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeoreferenciaInmuebleViewSet, georeferencias_altitud_mayor, \
    GeoreferenciaInmuebleAltitudMinimaViewSet, GeoreferenciaInmuebleZonaEspecificaViewSet, geocode_inmueble

router = DefaultRouter()
router.register(r'georeferencias', GeoreferenciaInmuebleViewSet) 
router.register(r'georeferencias-altitud-minima', GeoreferenciaInmuebleAltitudMinimaViewSet, basename='georeferencia-altitud-minima')
router.register(r'georeferencias-zona-especifica', GeoreferenciaInmuebleZonaEspecificaViewSet, basename='georeferencia-zona-especifica')

urlpatterns = [
    path('', include(router.urls)),
    path('georeferencias/altitud_mayor/<int:altitud>/', georeferencias_altitud_mayor),
    path('geocode/<str:numero_inmueble>/', geocode_inmueble, name='geocode_inmueble'),
]