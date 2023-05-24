from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reciclador.models import Reciclador

from core.serializers.fields import CPFField

from usuario.serializers.usuario import UsuarioSerializer
from usuario.models import Usuario


class RecicladorSerializer(UsuarioSerializer):
    usuario = UsuarioSerializer()
    cpf = CPFField(validators=[UniqueValidator(
        queryset=Reciclador.objects.all())])

    class Meta:
        model = Reciclador
        fields = ('usuario', 'cpf',)

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        password = usuario_data.pop('senha')
        usuario = Usuario.objects.create_user(
            usuario_data['email'],
            password=password,
            **usuario_data
        )

        return Reciclador.objects.create(usuario=usuario, **validated_data)


class RecicladorDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reciclador
        fields = '__all__'
