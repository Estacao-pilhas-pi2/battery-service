import uuid

from django.db import models

from maquina.models import Maquina

class Pagamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantidade_pilha_AA = models.IntegerField(default=0)
    quantidade_pilha_AAA = models.IntegerField(default=0)
    quantidade_pilha_C = models.IntegerField(default=0)
    quantidade_pilha_D = models.IntegerField(default=0)
    quantidade_pilha_V9 = models.IntegerField(default=0)

    utilizado = models.BooleanField(default=False)
    data_vencimento = models.DateTimeField()

    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)

    @property
    def valor_total(self):
        return sum([
            getattr(self, f'quantidade_pilha_{tipo}') * getattr(self.maquina, f'preco_{tipo}')
            for tipo in ['AAA', 'AA', 'C', 'D', 'V9']
        ])