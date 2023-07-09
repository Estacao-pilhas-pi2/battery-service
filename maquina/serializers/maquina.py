from maquina.models import Endereco, Maquina
from rest_framework import serializers


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'
        read_only_fields = ['id']


class MaquinaSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()

    class Meta:
        model = Maquina
        fields = '__all__'
        read_only_fields = ['quantidade_AAA', 'quantidade_AA', 'quantidade_C', 'quantidade_D', 'quantidade_V9']

    def update(self, instance, validated_data):
        endereco_data = validated_data.pop('endereco', None)

        if self.context['request'].method == 'PUT':
            for tipo in ['AAA', 'AA', 'C', 'D', 'V9']:
                setattr(instance, f'preco_{tipo}', 0)
                setattr(instance, f'quantidade_{tipo}', 0)

            instance.estabelecimento = None
            instance.endereco = None

        if endereco_data:
            endereco = Endereco.objects.create(**endereco_data)
            instance.endereco = endereco

        for campo, valor in validated_data.items():
            setattr(instance, campo, valor)

        instance.save()

        return instance


class MaquinaEsvaziarSerializer(serializers.Serializer):
    id = serializers.SlugRelatedField(queryset=Maquina.objects.all(), slug_field='id')
    tipos = serializers.MultipleChoiceField(choices=['AAA', 'AA', 'C', 'D', 'V9'], required=False)

    def save(self):
        maquina = self.validated_data['id']

        if not self.validated_data.get('tipos'):
            self.validated_data['tipos'] = ['AAA', 'AA', 'C', 'D', 'V9']

        for tipo in self.validated_data['tipos']:
            setattr(maquina, f'quantidade_{tipo}', 0)
        maquina.save()

        return maquina.id
