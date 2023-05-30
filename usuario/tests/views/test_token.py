from core.tests.mixin import APITestMixin

from django.test import TestCase

from freezegun import freeze_time

from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken

from usuario.tests.recipes import usuario as usuario_recipe

from reciclador.tests.recipes import reciclador as reciclador_recipe


class TokenObtainPairViewTest(APITestMixin, TestCase):
    url = reverse_lazy('usuario-login')

    def setUp(self):
        self.email = 'email2@teste.com'
        self.senha = 'senha_forte'
        self.usuario = usuario_recipe.make(email=self.email, nome=self.nome)
        self.usuario.set_password(self.senha)
        self.usuario.save(update_fields=['password'])

    def test_login(self):
        reciclador_recipe.make(usuario=self.usuario)
        self.id = str(self.usuario.id)
        response = self.client.post(self.url, data={
            'email': self.email,
            'password': self.senha
        })
        self.assertEqual(response.status_code, 200, response.json())

        for campo in ('id', 'nome', 'email'):
            with self.subTest(campo=campo):
                self.assertEqual(response.json()[campo], getattr(self, campo))

    def test_login_invalido(self):
        response = self.client.post(self.url, data={
            'email': self.email,
            'password': 'senha_invalida'
        })
        self.assertEqual(response.status_code, 401, response.json())
        self.assertIn(
            'Nenhuma conta encontrada. Email ou senha incorretos.',
            response.json()['detail']
        )


class RefreshViewTest(APITestMixin, TestCase):
    url = reverse_lazy('usuario-refresh')

    def setUp(self):
        self.email = 'email2@teste.com'
        self.senha = 'senha_forte'
        self.usuario = usuario_recipe.make(email=self.email)
        self.usuario.set_password(self.senha)
        self.usuario.save(update_fields=['password'])

        with freeze_time("2022-1-1"):
            self.refresh = RefreshToken.for_user(self.usuario)
            self.access = self.refresh.access_token

    @freeze_time('2022-1-8')
    def test_refresh_do_token(self):
        response = self.client.post(self.url, data={'refresh': str(self.refresh)})
        self.assertEqual(response.status_code, 200, response.json())
        self.assertIsNotNone(response.json().get('access'))

    @freeze_time('2022-1-11')
    def test_refresh_invalido(self):
        response = self.client.post(self.url, data={'refresh': str(self.refresh)})
        self.assertEqual(response.status_code, 401, response.json())
        self.assertIn(
            'Token is invalid or expired',
            response.json()['detail']
        )


class TokenVerifyViewTest(APITestMixin, TestCase):
    url = reverse_lazy('usuario-verify')

    def setUp(self):
        self.email = 'email2@teste.com'
        self.senha = 'senha_forte'
        self.usuario = usuario_recipe.make(email=self.email)
        self.usuario.set_password(self.senha)
        self.usuario.save(update_fields=['password'])

    def test_token_valido(self):
        refresh = RefreshToken.for_user(self.usuario)
        access = refresh.access_token

        response = self.client.post(self.url, data={'token': str(access)})
        self.assertEqual(response.status_code, 200, response.json())

    def test_token_expirado_refresh_valido(self):
        with freeze_time("2022-1-1"):
            refresh = RefreshToken.for_user(self.usuario)

        with freeze_time("2022-1-8"):
            response = self.client.post(self.url, data={'token': str(refresh)})

        self.assertEqual(response.status_code, 200, response.json())

    def test_token_expirado(self):
        with freeze_time("2022-1-1"):
            refresh = RefreshToken.for_user(self.usuario)
            access = refresh.access_token

        with freeze_time("2022-1-20"):
            response = self.client.post(self.url, data={'token': str(access)})

        self.assertEqual(response.status_code, 401, response.json())
        self.assertIn(
            'Token is invalid or expired',
            response.json()['detail']
        )
