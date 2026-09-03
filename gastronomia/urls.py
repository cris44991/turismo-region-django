from django.urls import path
from . import views

app_name = 'gastronomia'

urlpatterns = [
    path('', views.lista_platos, name='lista_platos'),
    path('<int:plato_id>/', views.detalle_plato, name='detalle_plato'),
]
