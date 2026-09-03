from django.urls import path
from . import views

app_name = 'lugares'

urlpatterns = [
    path('', views.lista_lugares, name='lista_lugares'),
    path('<int:lugar_id>/', views.detalle_lugar, name='detalle_lugar'),
]
