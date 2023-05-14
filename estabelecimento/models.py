from django.db import models

from usuario.models import Usuario


class Estabelecimento(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)
    cnpj = models.CharField(max_length=14, unique=True)
