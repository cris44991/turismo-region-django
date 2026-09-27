from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Ciudad o Comuna")

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"

    def __str__(self):
        return self.nombre


class Lugar(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="lugares", verbose_name="Categoría")
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, related_name="lugares", verbose_name="Ciudad")
    nombre = models.CharField(max_length=150, verbose_name="Nombre del atractivo")
    descripcion_corta = models.CharField(max_length=255, verbose_name="Descripción corta")
    descripcion_larga = models.TextField(verbose_name="Descripción detallada")
    horario = models.CharField(max_length=150, verbose_name="Horario")
    precio = models.CharField(max_length=150, verbose_name="Precio")
    como_llegar = models.TextField(verbose_name="Cómo llegar")
    recomendaciones = models.TextField(verbose_name="Recomendaciones")
    destacado = models.BooleanField(default=False, verbose_name="¿Es destacado?")
    imagen = models.CharField(max_length=255, verbose_name="Ruta de imagen")
    lat = models.FloatField(verbose_name="Latitud")
    lon = models.FloatField(verbose_name="Longitud")

    class Meta:
        verbose_name = "Lugar Turístico"
        verbose_name_plural = "Lugares Turísticos"

    def __str__(self):
        return self.nombre
