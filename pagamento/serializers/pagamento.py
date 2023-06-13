from datetime import datetime, timedelta

from firebase_admin.messaging import Message, Notification

from rest_framework import serializers

from pagamento.models import Pagamento


class PagamentoSerializer(serializers.ModelSerializer):
    valor_total = serializers.SerializerMethodField()

    class Meta:
        model = Pagamento
        fields = [
            'id', 'quantidade_pilha_AA', 'quantidade_pilha_AAA', 'quantidade_pilha_C',
            'quantidade_pilha_D', 'quantidade_pilha_V9', 'utilizado', 'data_vencimento',
            'maquina', 'valor_total', 'preco_AAA', 'preco_AA', 'preco_V9', 'preco_C', 
            'preco_D'
        ]
        read_only_fields = [
            'id', 'utilizado', 'data_vencimento', 'preco_AAA', 'preco_AA',
            'preco_V9', 'preco_C', 'preco_D'
        ]

    def get_valor_total(self, obj):
        return obj.valor_total

    def create(self, validated_data):
        validated_data['data_vencimento'] = datetime.now() + timedelta(minutes=5)
        maquina = validated_data['maquina']

        for tipo in ['AAA', 'AA', 'C', 'D', 'V9']:
            validated_data[f'preco_{tipo}'] = getattr(maquina, f'preco_{tipo}')

        return super().create(validated_data)


class PagamentoEfetuarSerializer(serializers.Serializer):
    id_pagamento = serializers.SlugRelatedField(queryset=Pagamento.objects.all(), slug_field='id')

    def validate(self, data):
        if data['id_pagamento'].data_vencimento.replace(tzinfo=None) < datetime.now():
            raise serializers.ValidationError({
                'data_vencimento': 'Pagamento com data de vencimento expirada.'
            })

        if data['id_pagamento'].utilizado:
            raise serializers.ValidationError({
                'utilizado': 'Pagamento já foi utilizado.'
            })

        return data

    def save(self):
        reciclador = self.context['request'].user.reciclador
        pagamento = self.validated_data['id_pagamento']
        pagamento.utilizado = True
        pagamento.reciclador = reciclador
        pagamento.save()

        reciclador.credito = reciclador.credito + pagamento.valor_total
        reciclador.save()

        maquina = pagamento.maquina
        for tipo in ['AAA', 'AA', 'C', 'D', 'V9']:
            setattr(
                maquina, f'quantidade_{tipo}',
                getattr(maquina, f'quantidade_{tipo}') + getattr(
                    pagamento, f'quantidade_pilha_{tipo}'
                )
            )

        maquina.save()
        maquina.refresh_from_db()

        if maquina.capacidade_pilhas:
            device = maquina.estabelecimento.usuario.fcmdevice_set.first()
            device.send_message(Message(notification=Notification(
                title='Capacidade alcançada!', body='Uma de suas máquinas atingiu o limite configurado '
                f'de f{maquina.limite_maximo}% no(s) seguinte(s) '
                f'tipos de pilhas: f{", ".join(maquina.capacidade_pilhas)}. Consulte '
                'o aplicativo para mais informações!'
            )))

        return pagamento.id

    def to_representation(self, _):
        return PagamentoSerializer(
            instance=self.validated_data['id_pagamento'],
            context=self.context
        ).data
