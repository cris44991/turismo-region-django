from django.contrib import admin
from .models import Categoria, Plato, Ingrediente, PasoPreparacion

class IngredienteInline(admin.TabularInline):
    model = Ingrediente
    extra = 1

class PasoPreparacionInline(admin.TabularInline):
    model = PasoPreparacion
    extra = 1

@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    inlines = [IngredienteInline, PasoPreparacionInline]
    list_display = ('nombre', 'categoria', 'dificultad', 'tiempo_preparacion', 'porciones', 'destacado')
    list_filter = ('categoria', 'dificultad', 'destacado')
    search_fields = ('nombre', 'descripcion_corta', 'descripcion_larga')
    list_editable = ('destacado',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('texto', 'plato')
    search_fields = ('texto',)

@admin.register(PasoPreparacion)
class PasoPreparacionAdmin(admin.ModelAdmin):
    list_display = ('plato', 'orden', 'texto')
    list_filter = ('plato',)
