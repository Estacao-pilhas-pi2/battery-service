from django.test import TestCase
from parameterized import parameterized

from estabelecimento.models import Estabelecimento
from estabelecimento.tests.recipes import estabelecimento as estabelecimento_recipe

from rest_framework.reverse import reverse_lazy

from usuario.tests.views.test_usuario import UsuarioApiViewBase


class EstabelecimentoCadastroViewTest(UsuarioApiViewBase, TestCase):
    url = reverse_lazy("estabelecimento-create")

    def _payload(self):
        return {
            "usuario": super()._payload(),
            "cnpj": "51655938000180",
        }

    def test_cria_estabelecimento(self):
        payload = self._payload()

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(Estabelecimento.objects.count(), 1)

        estabelecimento = Estabelecimento.objects.first()
        self.assertEqual(estabelecimento.usuario.nome, payload["usuario"]["nome"])
        self.assertEqual(estabelecimento.usuario.telefone, payload["usuario"]["telefone"])
        self.assertNotEqual(estabelecimento.usuario.password, payload["usuario"]["senha"])
        self.assertEqual(estabelecimento.cnpj, payload["cnpj"])

    @parameterized.expand([
        ('', 'Este campo não pode ser em branco.'),
        ('12345678912345', 'CNPJ inválido.'),
        ('11111111111181', 'CNPJ inválido.'),
        ('11111111111118', 'CNPJ inválido.'),
    ])
    def test_nao_cria_estabelecimento_cnpj_invalido(self, cnpj, msg):
        payload = self._payload()
        payload['cnpj'] = cnpj

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(msg, response.json()['cnpj'])

    def test_nao_cria_estabelecimento_cnpj_duplicado(self):
        payload = self._payload()
        estabelecimento_recipe.make(cnpj=payload["cnpj"])

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Esse campo deve ser  único.", response.json()["cnpj"])
