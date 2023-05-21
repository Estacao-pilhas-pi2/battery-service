from django.db import models

from estabelecimento.models import Estabelecimento


class Endereco(models.Model):
    cep = models.CharField(max_length=8)
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    rua = models.CharField(max_length=50)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=50, null=True)
    descricao = models.CharField(max_length=50, null=True)


class Maquina(models.Model):
    descricao = models.CharField(max_length=200, null=True, blank=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, related_name='maquinas', null=True, blank=True)
    preco_AAA = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    preco_AA = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    preco_C = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    preco_D = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    preco_V9 = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    quantidade_AAA = models.IntegerField(default=0)
    quantidade_AA = models.IntegerField(default=0)
    quantidade_C = models.IntegerField(default=0)
    quantidade_D = models.IntegerField(default=0)
    quantidade_V9 = models.IntegerField(default=0)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.PROTECT, null=True, blank=True)
