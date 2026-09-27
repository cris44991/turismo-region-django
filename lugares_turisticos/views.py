import requests
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Lugar, Categoria, Ciudad

def obtener_clima_la_serena():
    """
    Uso de librería externa (requests):
    Consulta la API pública de Open-Meteo para obtener temperatura y condición actual de La Serena.
    """
    url = "https://api.open-meteo.com/v1/forecast?latitude=-29.9027&longitude=-71.2519&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&timezone=America%2FSantiago"
    try:
        respuesta = requests.get(url, timeout=3)
        if respuesta.status_code == 200:
            datos = respuesta.json().get('current', {})
            temp = datos.get('temperature_2m', 18.5)
            hum = datos.get('relative_humidity_2m', 70)
            viento = datos.get('wind_speed_10m', 12)
            
            # Interpretar código de clima básico
            codigo = datos.get('weather_code', 0)
            if codigo == 0:
                condicion = "Despejado ☀️"
            elif codigo in [1, 2, 3]:
                condicion = "Parcialmente Nublado ⛅"
            elif codigo in [45, 48]:
                condicion = "Niebla / Camanchaca 🌫️"
            elif codigo in [51, 61, 80]:
                condicion = "Llovizna Costera 🌧️"
            else:
                condicion = "Templado 🌤️"
                
            return {
                'disponible': True,
                'temperatura': f"{temp}°C",
                'humedad': f"{hum}%",
                'viento': f"{viento} km/h",
                'condicion': condicion,
                'ciudad': "La Serena y Valle de Elqui"
            }
    except Exception:
        pass

    # Datos por defecto en caso de no tener conexión a internet
    return {
        'disponible': True,
        'temperatura': "19.0°C",
        'humedad': "68%",
        'viento': "14 km/h",
        'condicion': "Cielo Despejado ☀️",
        'ciudad': "La Serena y Valle de Elqui (Estimado)"
    }

def lista_lugares(request):
    """
    Vista 1: Muestra el catálogo de destinos turísticos consultando vía Django ORM.
    """
    categoria_seleccionada = request.GET.get('categoria', '').strip()
    busqueda = request.GET.get('q', '').strip()

    # Query base optimizada con relaciones
    lugares_qs = Lugar.objects.select_related('categoria', 'ciudad').all()
    total_lugares = Lugar.objects.count()

    # Obtener todas las categorías para el filtro
    categorias = Categoria.objects.values_list('nombre', flat=True).order_by('nombre')

    # Filtrar por categoría
    if categoria_seleccionada:
        lugares_qs = lugares_qs.filter(categoria__nombre=categoria_seleccionada)

    # Filtrar por término de búsqueda (nombre, descripción, ciudad)
    if busqueda:
        lugares_qs = lugares_qs.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion_corta__icontains=busqueda) |
            Q(ciudad__nombre__icontains=busqueda)
        ).distinct()

    total_mostrados = lugares_qs.count()
    clima = obtener_clima_la_serena()

    contexto = {
        'lugares': lugares_qs,
        'categorias': list(categorias),
        'categoria_activa': categoria_seleccionada,
        'busqueda': busqueda,
        'total_lugares': total_lugares,
        'total_mostrados': total_mostrados,
        'clima': clima,
        'app_activa': 'lugares'
    }
    return render(request, 'lugares_turisticos/lista.html', contexto)

def detalle_lugar(request, lugar_id):
    """
    Vista 2: Muestra la ficha detallada de un destino turístico desde la base de datos.
    """
    lugar = get_object_or_404(Lugar.objects.select_related('categoria', 'ciudad'), pk=lugar_id)

    # Lugares recomendados
    recomendados = Lugar.objects.select_related('categoria', 'ciudad').exclude(pk=lugar_id)[:3]

    contexto = {
        'lugar': lugar,
        'recomendados': recomendados,
        'app_activa': 'lugares'
    }
    return render(request, 'lugares_turisticos/detalle.html', contexto)
