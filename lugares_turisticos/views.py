import json
import os
import requests
from django.shortcuts import render, Http404
from django.conf import settings

def cargar_datos_lugares():
    """Función auxiliar para leer el archivo JSON de lugares turísticos."""
    ruta_archivo = os.path.join(settings.BASE_DIR, 'data', 'lugares.json')
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

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
    Vista 1: Muestra el listado de destinos turísticos con filtros por categoría y buscador.
    """
    todos_lugares = cargar_datos_lugares()
    categoria_seleccionada = request.GET.get('categoria', '').strip()
    busqueda = request.GET.get('q', '').strip().lower()

    # Obtener todas las categorías únicas para el filtro
    categorias = sorted(list(set(l['categoria'] for l in todos_lugares)))

    # Filtrar según los parámetros recibidos
    lugares_filtrados = todos_lugares
    if categoria_seleccionada:
        lugares_filtrados = [l for l in lugares_filtrados if l['categoria'] == categoria_seleccionada]

    if busqueda:
        lugares_filtrados = [
            l for l in lugares_filtrados
            if busqueda in l['nombre'].lower() or busqueda in l['descripcion_corta'].lower() or busqueda in l['ciudad'].lower()
        ]

    # Cálculos y estadísticas para el contexto
    total_lugares = len(todos_lugares)
    total_mostrados = len(lugares_filtrados)
    clima = obtener_clima_la_serena()

    contexto = {
        'lugares': lugares_filtrados,
        'categorias': categorias,
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
    Vista 2: Muestra la ficha detallada de un atractivo turístico específico.
    """
    todos_lugares = cargar_datos_lugares()
    lugar = next((l for l in todos_lugares if l['id'] == lugar_id), None)

    if not lugar:
        raise Http404("El destino turístico solicitado no existe.")

    # Lugares recomendados (de la misma categoría u otros)
    recomendados = [l for l in todos_lugares if l['id'] != lugar_id][:3]

    contexto = {
        'lugar': lugar,
        'recomendados': recomendados,
        'app_activa': 'lugares'
    }
    return render(request, 'lugares_turisticos/detalle.html', contexto)
