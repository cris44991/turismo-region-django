from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Plato(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="platos", verbose_name="Categoría")
    nombre = models.CharField(max_length=150, verbose_name="Nombre del plato")
    descripcion_corta = models.CharField(max_length=255, verbose_name="Descripción corta")
    descripcion_larga = models.TextField(verbose_name="Descripción detallada")
    tiempo_preparacion = models.CharField(max_length=50, verbose_name="Tiempo de preparación")
    dificultad = models.CharField(max_length=50, verbose_name="Dificultad")
    porciones = models.PositiveIntegerField(default=1, verbose_name="Porciones")
    maridaje = models.CharField(max_length=255, blank=True, null=True, verbose_name="Maridaje sugerido")
    destacado = models.BooleanField(default=False, verbose_name="¿Es destacado?")
    imagen = models.CharField(max_length=255, verbose_name="Ruta de imagen")

    class Meta:
        verbose_name = "Plato"
        verbose_name_plural = "Platos"

    def __str__(self):
        return self.nombre

    @property
    def preparacion(self):
        return [p.texto for p in self.pasos.all().order_by('orden')]


class Ingrediente(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, related_name="ingredientes", verbose_name="Plato")
    texto = models.CharField(max_length=255, verbose_name="Ingrediente")

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"

    def __str__(self):
        return self.texto


class PasoPreparacion(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, related_name="pasos", verbose_name="Plato")
    orden = models.PositiveIntegerField(verbose_name="Número de paso")
    texto = models.TextField(verbose_name="Instrucción del paso")

    class Meta:
        ordering = ['orden']
        verbose_name = "Paso de preparación"
        verbose_name_plural = "Pasos de preparación"

    def __str__(self):
        return f"Paso {self.orden}: {self.plato.nombre}"
