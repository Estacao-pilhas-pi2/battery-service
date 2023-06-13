import uuid

from django.db import models

from maquina.models import Maquina

from reciclador.models import Reciclador


class Pagamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantidade_pilha_AA = models.IntegerField(default=0)
    quantidade_pilha_AAA = models.IntegerField(default=0)
    quantidade_pilha_C = models.IntegerField(default=0)
    quantidade_pilha_D = models.IntegerField(default=0)
    quantidade_pilha_V9 = models.IntegerField(default=0)
    preco_AAA = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    preco_AA = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    preco_C = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    preco_D = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    preco_V9 = models.DecimalField(default=0, decimal_places=2, max_digits=7)

    utilizado = models.BooleanField(default=False)
    data_vencimento = models.DateTimeField()

    reciclador = models.ForeignKey(Reciclador, on_delete=models.PROTECT, null=True)

    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)

    @property
    def valor_total(self):
        return sum([
            getattr(self, f'quantidade_pilha_{tipo}') * getattr(self, f'preco_{tipo}')
            for tipo in ['AAA', 'AA', 'C', 'D', 'V9']
        ])
