import json
import os
from django.shortcuts import render, Http404
from django.conf import settings

def cargar_datos_gastronomia():
    """Función auxiliar para leer el archivo JSON de preparaciones gastronómicas."""
    ruta_archivo = os.path.join(settings.BASE_DIR, 'data', 'gastronomia.json')
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def lista_platos(request):
    """
    Vista 1: Muestra el catálogo de gastronomía regional con filtros y buscador.
    """
    todos_platos = cargar_datos_gastronomia()
    categoria_seleccionada = request.GET.get('categoria', '').strip()
    busqueda = request.GET.get('q', '').strip().lower()

    # Categorías únicas
    categorias = sorted(list(set(p['categoria'] for p in todos_platos)))

    # Filtrar según parámetros
    platos_filtrados = todos_platos
    if categoria_seleccionada:
        platos_filtrados = [p for p in platos_filtrados if p['categoria'] == categoria_seleccionada]

    if busqueda:
        platos_filtrados = [
            p for p in platos_filtrados
            if busqueda in p['nombre'].lower() 
            or busqueda in p['descripcion_corta'].lower()
            or any(busqueda in ing.lower() for ing in p.get('ingredientes', []))
        ]

    # Estadísticas para el contexto
    total_platos = len(todos_platos)
    total_mostrados = len(platos_filtrados)

    contexto = {
        'platos': platos_filtrados,
        'categorias': categorias,
        'categoria_activa': categoria_seleccionada,
        'busqueda': busqueda,
        'total_platos': total_platos,
        'total_mostrados': total_mostrados,
        'app_activa': 'gastronomia'
    }
    return render(request, 'gastronomia/lista.html', contexto)

def detalle_plato(request, plato_id):
    """
    Vista 2: Muestra la ficha y receta completa de una preparación típica.
    """
    todos_platos = cargar_datos_gastronomia()
    plato = next((p for p in todos_platos if p['id'] == plato_id), None)

    if not plato:
        raise Http404("La preparación gastronómica solicitada no existe.")

    # Otros platos recomendados
    otros_platos = [p for p in todos_platos if p['id'] != plato_id][:3]

    contexto = {
        'plato': plato,
        'otros_platos': otros_platos,
        'app_activa': 'gastronomia'
    }
    return render(request, 'gastronomia/detalle.html', contexto)
