from django.test import TestCase
from parameterized import parameterized

from reciclador.models import Reciclador
from reciclador.tests.recipes import reciclador as reciclador_recipe

from rest_framework.reverse import reverse_lazy

from usuario.tests.views.test_usuario import UsuarioApiViewBase


class RecicladorCadastroViewTest(UsuarioApiViewBase, TestCase):
    url = reverse_lazy("reciclador-create")

    def _payload(self):
        return {
            "usuario": super()._payload(),
            "cpf": "55151392085",
        }

    def test_cria_reciclador(self):
        payload = self._payload()

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(Reciclador.objects.count(), 1)

        reciclador = Reciclador.objects.first()
        self.assertEqual(reciclador.usuario.nome, payload["usuario"]["nome"])
        self.assertEqual(reciclador.usuario.telefone, payload["usuario"]["telefone"])
        self.assertNotEqual(reciclador.usuario.password, payload["usuario"]["senha"])
        self.assertEqual(reciclador.cpf, payload["cpf"])

    @parameterized.expand([
        ('', 'Este campo não pode ser em branco.'),
        ('123456789', 'CPF inválido.'),
        ('11111111181', 'CPF inválido.'),
        ('11111111118', 'CPF inválido.'),
    ])
    def test_nao_cria_reciclador_cpf_invalido(self, cpf, msg):
        payload = self._payload()
        payload['cpf'] = cpf

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(msg, response.json()['cpf'])

    def test_nao_cria_reciclador_cpf_duplicado(self):
        payload = self._payload()
        reciclador_recipe.make(cpf=payload["cpf"])

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Esse campo deve ser  único.", response.json()["cpf"])
