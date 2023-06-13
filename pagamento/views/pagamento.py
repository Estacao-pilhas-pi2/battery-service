from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView

from pagamento.serializers.pagamento import PagamentoSerializer, PagamentoEfetuarSerializer
from pagamento.models import Pagamento


class PagamentoGenericAPIView:
    serializer_class = PagamentoSerializer

    def get_queryset(self):
        if hasattr(self.request.user, 'estabelecimento'):
            return Pagamento.objects.filter(
                maquina__estabelecimento=self.request.user.estabelecimento
            ).order_by('data_vencimento')
        else:
            return self.request.user.reciclador.pagamento_set.all().order_by('data_vencimento')


class PagamentoListCreateView(PagamentoGenericAPIView, ListCreateAPIView):
    pass


class PagamentoEfetuarView(CreateAPIView):
    serializer_class = PagamentoEfetuarSerializer
