from django.test import TestCase

from datetime import datetime, timedelta

from decimal import Decimal

from model_bakery import baker

from freezegun import freeze_time

from core.tests.mixin import APITestMixin

from pagamento.models import Pagamento
from pagamento.tests.recipes import pagamento as pagamento_recipe

from reciclador.tests.recipes import reciclador as reciclador_recipe

from estabelecimento.tests.recipes import estabelecimento as estabelecimento_recipe

from maquina.models import Maquina

from rest_framework.reverse import reverse_lazy


class PagamentoViewTest(TestCase):
    url = reverse_lazy("pagamento-list-create")

    @property
    def _payload(self):
        return {
            "quantidade_pilha_AA": 10,
            "quantidade_pilha_AAA": 5,
            "quantidade_pilha_C": 2,
            "quantidade_pilha_D": 5,
            "quantidade_pilha_V9": 0,
            "maquina": self.maquina.id
        }

    def setUp(self):
        self.estabelecimento = estabelecimento_recipe.make()
        self.maquina = baker.make(
            Maquina,
            preco_AAA=Decimal('0.3'),
            preco_AA=Decimal('0.1'),
            preco_C=Decimal('0.4'),
            preco_D=Decimal('0.5'),
            preco_V9=Decimal('0.15'),
            estabelecimento=self.estabelecimento
        )

    def test_cria_pagamento_com_sucesso(self):
        with freeze_time("2023-01-01 04:20:00"):
            response = self.client.post(self.url, self._payload)
            self.assertEqual(response.status_code, 201)

        pagamento = Pagamento.objects.first()
        valor_total = sum([
            (self.maquina.preco_AAA * pagamento.quantidade_pilha_AAA),
            (self.maquina.preco_AA * pagamento.quantidade_pilha_AA),
            (self.maquina.preco_C * pagamento.quantidade_pilha_C),
            (self.maquina.preco_D * pagamento.quantidade_pilha_D),
            (self.maquina.preco_V9 * pagamento.quantidade_pilha_V9)
        ])

        self.assertEqual(pagamento.valor_total, valor_total)
        self.assertIsNotNone(response.json().get('id'))
        self.assertFalse(response.json().get('utilizado'))
        self.assertEqual(
            pagamento.data_vencimento.replace(tzinfo=None),
            datetime(2023, 1, 1, 4, 25)
        )

        for tipo in ['AAA', 'AA', 'C', 'D', 'V9']:
            with self.subTest(tipo=tipo):
                self.assertEqual(
                    getattr(pagamento, f'preco_{tipo}'),
                    getattr(self.maquina, f'preco_{tipo}')
                )


class PagamentoEfetuarViewTest(APITestMixin, TestCase):
    url = reverse_lazy("pagamento-efetuar")

    @property
    def _payload(self):
        return {
            "id_pagamento": self.pagamento.id
        }

    def setUp(self):
        self.estabelecimento = estabelecimento_recipe.make()
        self.maquina = baker.make(Maquina, estabelecimento=self.estabelecimento)
        self.pagamento = pagamento_recipe.make(
            maquina=self.maquina, data_vencimento=(datetime.now() + timedelta(minutes=40)))
        self.reciclador = reciclador_recipe.make(usuario=self.user)

    def test_efetua_pagamento_com_sucesso(self):
        response = self.client.post(self.url, self._payload)
        self.assertEqual(response.status_code, 201)

        # Certifica-se de que os creditos foram adicionados a conta do reciclador
        self.assertEqual(self.pagamento.valor_total, self.reciclador.credito)
        for tipo in ['AAA', 'AA', 'C', 'D', 'V9']:
            self.assertEqual(getattr(self.maquina, f'quantidade_{tipo}'), getattr(self.pagamento, f'quantidade_pilha_{tipo}'))
        self.pagamento.refresh_from_db()
        self.assertTrue(self.pagamento.utilizado)
        self.assertEqual(self.pagamento.reciclador, self.reciclador)

    def test_nao_efetua_pagamento_vencido(self):
        self.pagamento.data_vencimento = datetime.now() - timedelta(minutes=40)
        self.pagamento.save()
        response = self.client.post(self.url, self._payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Pagamento com data de vencimento expirada.',
            response.json()['data_vencimento']
        )
