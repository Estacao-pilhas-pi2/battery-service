from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'Nenhuma conta encontrada. Email, CPF ou senha incorretos.'
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'id': str(self.user.id)})
        data.update({'email': self.user.email})
        data.update({'cpf': self.user.cpf})
        data.update({'nome': self.user.nome})
        return data
