from django.contrib import admin
from .models import Categoria, Ciudad, Lugar

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'categoria', 'precio', 'destacado')
    list_filter = ('ciudad', 'categoria', 'destacado')
    search_fields = ('nombre', 'descripcion_corta', 'descripcion_larga', 'como_llegar')
    list_editable = ('destacado',)
