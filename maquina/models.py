from django.db import models

from django.db import models

class Pilha(models.Model):
    tipo_pilha = models.CharField(primary_key=True, max_length=3)

class Maquina(models.Model):
    descricao = models.CharField(max_length=200)
    pilhas = models.ManyToManyField(Pilha)
    preco_AAA = models.DecimalField(decimal_places=2)
    preco_AA = models.DecimalField(decimal_places=2)
    preco_C = models.DecimalField(decimal_places=2)
    preco_D = models.DecimalField(decimal_places=2)
    preco_V9 = models.DecimalField(decimal_places=2)

class Possui(models.Model):
    pilha = models.ForeignKey(Pilha, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    quantidade_pilha = models.IntegerField()
