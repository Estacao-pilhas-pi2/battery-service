from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from usuario.models import Usuario


class Estabelecimento(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)
    cnpj = models.CharField(max_length=14, unique=True)
    limite_maximo = models.DecimalField(
        decimal_places=2, max_digits=4, default=70,
        validators=[MinValueValidator(10), MaxValueValidator(100)]
    )
