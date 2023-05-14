from parameterized import parameterized

from core.tests.mixin import APITestMixin

from usuario.tests.recipes import usuario as usuario_recipe


class UsuarioApiViewBase(APITestMixin):
    url = ""

    def _payload(self):
        return {
            "email": "mr.bean@email.com",
            "dataNascimento": "1990-01-01",
            "telefone": "5561998765432",
            "nome": "Mister Bean",
            "senha": "senha_1_senha_2",
        }

    def test_nao_cria_usuario_data_formato_invalido(self):
        payload = self._payload()
        payload['usuario']['dataNascimento'] = '11-05-2000'

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Formato inválido para data. Use um dos formatos a seguir: YYYY-MM-DD.',
            response.json()['usuario']['dataNascimento'],
        )

    @parameterized.expand([('5561641115112345678',), ('559999999999',), ('invalido',)])
    def test_nao_cria_usuario_telefone_invalido(self, telefone):
        payload = self._payload()
        payload['usuario']['telefone'] = telefone

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(
            'Este número de telefone não é válido.',
            response.json()['usuario']['telefone'],
        )

    @parameterized.expand([
        ('a' * 101, 'Certifique-se de que este campo não tenha mais de 100 caracteres.'),
        ('b' * 7, 'Certifique-se de que este campo tenha mais de 8 caracteres.'),
    ])
    def test_nao_cria_usuario_senha_invalida(self, senha, msg):
        payload = self._payload()
        payload['usuario']['senha'] = senha

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 400, response.json())
        self.assertIn(msg, response.json()['usuario']['senha'])
