from rest_framework.generics import CreateAPIView

from pagamento.serializers.pagamento import PagamentoSerializer, PagamentoEfetuarSerializer

class PagamentoCreateView(CreateAPIView):
    serializer_class = PagamentoSerializer


class PagamentoEfetuarView(CreateAPIView):
    serializer_class = PagamentoEfetuarSerializer