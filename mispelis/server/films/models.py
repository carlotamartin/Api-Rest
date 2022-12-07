from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.utils.text import slugify


from django.conf import settings  # new
from django.core.validators import MaxValueValidator  # new


class Film(models.Model):

    def path_to_film(self, instance, filename):
        return f'films/{instance.id}/{filename}'

    id = models.UUIDField( # uuid en lugar de id clásica autoincremental
    primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150, verbose_name="Título")
    year = models.PositiveIntegerField(default=2000, verbose_name="Año")
    review_short = models.TextField(null=True, blank=True, verbose_name="Argumento (corto)")
    review_large = models.TextField(null=True, blank=True, verbose_name="Historia (largo)")
    trailer_url = models.URLField(max_length=150, null=True, blank=True, verbose_name="URL youtube")
    genres = models.ManyToManyField('FilmGenre', related_name="film_genres",verbose_name="Géneros")
    image_thumbnail = models.ImageField(upload_to='films/', null=True, blank=True,verbose_name="Miniatura")
    image_wallpaper = models.ImageField(upload_to='films/', null=True, blank=True,verbose_name="Wallpaper")

    class Meta:
        verbose_name = "Película"
        ordering = ['title']
        def __str__(self):
            return f'{self.title} ({self.year})'
class FilmGenre(models.Model):
    name = models.CharField(
    max_length=50, verbose_name="Nombre", unique=True)
    slug = models.SlugField(
    unique=True)
    class Meta:
        verbose_name = "género"
        ordering = ['name']

        def __str__(self):
            return f'{self.name}'

        def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            super(FilmGenre, self).save(*args, **kwargs)



class FilmUser(models.Model):

    STATUS_CHOICES = (
        (0, "Sin estado"),
        (1, "Vista"),
        (2, "Quiero verla"))

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    # Se podría hacer en tres modelos separados para que sea más eficiente
    # pero a nivel de desarrollo habría que hacer lo mismo tres veces

    state = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=0)  # Al crearse sin estado se borra
    favorite = models.BooleanField(
        default=False)
    note = models.PositiveSmallIntegerField(
        null=True, validators=[MaxValueValidator(10)])
    review = models.TextField(null=True)

    class Meta:
        unique_together = ['film', 'user']
        ordering = ['film__title']