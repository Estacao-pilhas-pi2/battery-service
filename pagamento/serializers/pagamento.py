from datetime import datetime, timedelta

from django.db.models import F

from rest_framework import serializers

from pagamento.models import Pagamento


class PagamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pagamento
        fields = '__all__'
        read_only_fields = ['id', 'utilizado', 'data_vencimento']

    def create(self, validated_data):
        validated_data['data_vencimento'] = datetime.now() + timedelta(minutes=5)
        return super().create(validated_data)


class PagamentoEfetuarSerializer(serializers.Serializer):
    id_pagamento = serializers.SlugRelatedField(queryset=Pagamento.objects.all(), slug_field='id')

    def validate(self, data):
        if data['id_pagamento'].data_vencimento.replace(tzinfo=None) < datetime.now():
            raise serializers.ValidationError({
                'data_vencimento': 'Pagamento com data de vencimento expirada.'
            })
        return data

    def save(self):
        pagamento = self.validated_data['id_pagamento']
        pagamento.utizado = False
        pagamento.save()

        reciclador = self.context['request'].user.reciclador
        reciclador.credito = pagamento.valor_total
        reciclador.save()

        maquina = pagamento.maquina
        for tipo in ['AAA', 'AA', 'C', 'D', 'V9']:
            setattr(
                maquina, f'quantidade_{tipo}',
                F(f'quantidade_{tipo}') + getattr(
                    pagamento, f'quantidade_pilha_{tipo}'
                )
            )

        return pagamento.id
