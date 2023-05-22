from datetime import datetime, timedelta

from firebase_admin.messaging import Message, Notification

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
