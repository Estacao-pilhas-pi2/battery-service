from django.db import models

from usuario.models import Usuario


class Reciclador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)
    cpf = models.CharField(max_length=11, unique=True)
    credito = models.DecimalField(default=0, decimal_places=2, max_digits=7)
