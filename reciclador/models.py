from django.db import models

from usuario.models import Usuario


class Reciclador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)
    cpf = models.CharField(max_length=11, unique=True)
