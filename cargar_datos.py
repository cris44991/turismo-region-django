import os
import json
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turismo_region.settings')
django.setup()

from gastronomia.models import Categoria as CategoriaGastronomia, Plato, Ingrediente, PasoPreparacion
from lugares_turisticos.models import Categoria as CategoriaLugares, Ciudad, Lugar

def cargar_gastronomia():
    ruta = os.path.join('data', 'gastronomia.json')
    if not os.path.exists(ruta):
        print(f"No se encontró el archivo {ruta}")
        return
    
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for item in data:
        cat, _ = CategoriaGastronomia.objects.get_or_create(nombre=item['categoria'])
        
        plato, created = Plato.objects.update_or_create(
            id=item.get('id'),
            defaults={
                'categoria': cat,
                'nombre': item['nombre'],
                'descripcion_corta': item.get('descripcion_corta', ''),
                'descripcion_larga': item.get('descripcion_larga', ''),
                'tiempo_preparacion': item.get('tiempo_preparacion', ''),
                'dificultad': item.get('dificultad', ''),
                'porciones': item.get('porciones', 1),
                'maridaje': item.get('maridaje', ''),
                'destacado': item.get('destacado', False),
                'imagen': item.get('imagen', ''),
            }
        )
        
        # Evitar duplicados de relaciones dependientes en ejecuciones repetidas
        plato.ingredientes.all().delete()
        plato.pasos.all().delete()
        
        for ing_text in item.get('ingredientes', []):
            Ingrediente.objects.create(plato=plato, texto=ing_text)
            
        for i, paso_text in enumerate(item.get('preparacion', []), start=1):
            PasoPreparacion.objects.create(plato=plato, orden=i, texto=paso_text)

def cargar_lugares():
    ruta = os.path.join('data', 'lugares.json')
    if not os.path.exists(ruta):
        print(f"No se encontró el archivo {ruta}")
        return
        
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for item in data:
        cat, _ = CategoriaLugares.objects.get_or_create(nombre=item['categoria'])
        ciudad, _ = Ciudad.objects.get_or_create(nombre=item['ciudad'])
        
        Lugar.objects.update_or_create(
            id=item.get('id'),
            defaults={
                'categoria': cat,
                'ciudad': ciudad,
                'nombre': item['nombre'],
                'descripcion_corta': item.get('descripcion_corta', ''),
                'descripcion_larga': item.get('descripcion_larga', ''),
                'horario': item.get('horario', ''),
                'precio': item.get('precio', ''),
                'como_llegar': item.get('como_llegar', ''),
                'recomendaciones': item.get('recomendaciones', ''),
                'destacado': item.get('destacado', False),
                'imagen': item.get('imagen', ''),
                'lat': item.get('lat', 0.0),
                'lon': item.get('lon', 0.0),
            }
        )

if __name__ == '__main__':
    print("Iniciando migración de datos JSON hacia MySQL...")
    cargar_gastronomia()
    cargar_lugares()
    
    print("\n" + "="*50)
    print("REPORTE DE MIGRACIÓN DE DATOS (MySQL)")
    print("="*50)
    print(f"Gastronomía -> Categorías:        {CategoriaGastronomia.objects.count()}")
    print(f"Gastronomía -> Platos:            {Plato.objects.count()}")
    print(f"Gastronomía -> Ingredientes:      {Ingrediente.objects.count()}")
    print(f"Gastronomía -> Pasos Preparación: {PasoPreparacion.objects.count()}")
    print("-"*50)
    print(f"Lugares     -> Categorías:        {CategoriaLugares.objects.count()}")
    print(f"Lugares     -> Ciudades:          {Ciudad.objects.count()}")
    print(f"Lugares     -> Lugares Turísticos:{Lugar.objects.count()}")
    print("="*50)
    print("¡Migración completada exitosamente!")
