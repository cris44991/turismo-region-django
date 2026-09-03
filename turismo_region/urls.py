"""
URL configuration for turismo_region project.
Punto de entrada principal que vincula las rutas de las aplicaciones usando include().
"""
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # Redirección de la raíz al módulo de lugares turísticos
    path('', lambda request: redirect('lugares:lista_lugares'), name='home'),
    
    # Rutas modulares de cada aplicación
    path('lugares/', include('lugares_turisticos.urls')),
    path('gastronomia/', include('gastronomia.urls')),
]
