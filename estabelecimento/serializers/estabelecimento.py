from rest_framework.validators import UniqueValidator

from estabelecimento.models import Estabelecimento

from core.serializers.fields import CNPJField

from usuario.serializers.usuario import UsuarioSerializer
from usuario.models import Usuario


class EstabelecimentoSerializer(UsuarioSerializer):
    usuario = UsuarioSerializer()
    cnpj = CNPJField(validators=[UniqueValidator(
        queryset=Estabelecimento.objects.all())])

    class Meta:
        model = Estabelecimento
        fields = ('usuario', 'cnpj',)

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        password = usuario_data.pop('senha')
        usuario = Usuario.objects.create_user(
            usuario_data['email'],
            password=password,
            **usuario_data
        )

        return Estabelecimento.objects.create(usuario=usuario, **validated_data)
