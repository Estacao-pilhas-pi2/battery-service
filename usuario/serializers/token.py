from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'Nenhuma conta encontrada. Email ou senha incorretos.'
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'id': str(self.user.id)})
        data.update({'email': self.user.email})
        data.update({'nome': self.user.nome})
        data.update({'estabelecimento': hasattr(self.user, 'estabelecimento')})
        data.update({'identificador': str(self.user.estabelecimento.id if hasattr(self.user, 'estabelecimento') else self.user.reciclador.id)})
        return data
