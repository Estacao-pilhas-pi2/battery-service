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


class PagamentoOfflineSerializer(serializers.ModelSerializer):
    esvaziado = serializers.BooleanField(required=False)

    class Meta:
        model = Pagamento
        fields = [
            'quantidade_pilha_AA', 'quantidade_pilha_AAA', 'quantidade_pilha_C',
            'quantidade_pilha_D', 'quantidade_pilha_V9', 'data_vencimento',
            'maquina', 'esvaziado'
        ]

    def validate_data_vencimento(self, data_vencimento):
        if data_vencimento.replace(tzinfo=None) < datetime.now():
            raise serializers.ValidationError('Data de vencimento no passado não permitida.')
        return data_vencimento


class PagamentoEfetuarSerializer(serializers.Serializer):
    id_pagamento = serializers.SlugRelatedField(queryset=Pagamento.objects.all(), slug_field='id', required=False)
    pagamento = PagamentoOfflineSerializer(required=False)

    def validate(self, data):
        if not data.get('id_pagamento') and not data.get('pagamento'):
            raise serializers.ValidationError({
                'id_pagamento': 'ID do pagamento ou novo pagamento deve ser informado.'
            })

        if data.get('id_pagamento') and data.get('pagamento'):
            raise serializers.ValidationError({
                'pagamento': 'Apenas ID do pagamento ou novo pagamento deve ser informado.'
            })

        if not data.get('id_pagamento'):
            return data

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

        esvaziar = False
        if self.validated_data.get('pagamento') and self.validated_data['pagamento'].get('esvaziado', False):
            esvaziar = self.validated_data['pagamento'].pop('esvaziado', False)

        if not self.validated_data.get('id_pagamento'):
            self.validated_data['id_pagamento'] = Pagamento.objects.create(**self.validated_data['pagamento'])

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
                (getattr(maquina, f'quantidade_{tipo}') if not esvaziar else 0) + getattr(
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
