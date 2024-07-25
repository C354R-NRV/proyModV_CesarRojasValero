from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from .models import Inmueble, EspecificacionTecnica, GeoreferenciaInmueble
from .views import geocode_inmueble

admin.site.register(Inmueble)
admin.site.register(EspecificacionTecnica)

class InmuebleAdmin(admin.ModelAdmin):
    list_display = ['numero_inmueble', 'ci_propietario', 'nombre_propietario', 'direccion']
    change_list_template = "admin/inmueble_change_list.html"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('geocode/<str:numero_inmueble>/', self.admin_site.admin_view(self.geocode_view), name='geocode_inmueble'),
        ]
        return custom_urls + urls
    
    def geocode_view(self, request, numero_inmueble):
        return redirect('geocode_inmueble', numero_inmueble=numero_inmueble)

@admin.register(GeoreferenciaInmueble)
class GeoreferenciaInmuebleAdmin(admin.ModelAdmin):
    list_display = ['numero_inmueble', 'latitud', 'longitud']