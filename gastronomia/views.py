from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Plato, Categoria, Ingrediente, PasoPreparacion

def lista_platos(request):
    """
    Vista 1: Muestra el catálogo de gastronomía regional consultando vía Django ORM.
    """
    categoria_seleccionada = request.GET.get('categoria', '').strip()
    busqueda = request.GET.get('q', '').strip()

    # Query base optimizada
    platos_qs = Plato.objects.select_related('categoria').all()
    total_platos = Plato.objects.count()

    # Obtener todas las categorías para el filtro
    categorias = Categoria.objects.values_list('nombre', flat=True).order_by('nombre')

    # Filtrar por categoría
    if categoria_seleccionada:
        platos_qs = platos_qs.filter(categoria__nombre=categoria_seleccionada)

    # Filtrar por término de búsqueda (nombre, descripción, ingredientes)
    if busqueda:
        platos_qs = platos_qs.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion_corta__icontains=busqueda) |
            Q(ingredientes__texto__icontains=busqueda)
        ).distinct()

    total_mostrados = platos_qs.count()

    contexto = {
        'platos': platos_qs,
        'categorias': list(categorias),
        'categoria_activa': categoria_seleccionada,
        'busqueda': busqueda,
        'total_platos': total_platos,
        'total_mostrados': total_mostrados,
        'app_activa': 'gastronomia'
    }
    return render(request, 'gastronomia/lista.html', contexto)

def detalle_plato(request, plato_id):
    """
    Vista 2: Muestra la ficha y receta completa de una preparación típica desde la base de datos.
    """
    plato = get_object_or_404(Plato.objects.select_related('categoria').prefetch_related('ingredientes', 'pasos'), pk=plato_id)

    # Otros platos recomendados
    otros_platos = Plato.objects.select_related('categoria').exclude(pk=plato_id)[:3]

    contexto = {
        'plato': plato,
        'otros_platos': otros_platos,
        'app_activa': 'gastronomia'
    }
    return render(request, 'gastronomia/detalle.html', contexto)
