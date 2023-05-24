from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView

from maquina.serializers.maquina import MaquinaSerializer, MaquinaEsvaziarSerializer
from maquina.models import Maquina
from estabelecimento.models import Estabelecimento


class MaquinaListView(ListAPIView):
    serializer_class = MaquinaSerializer

    def get_queryset(self):
        user = self.request.user
        if Estabelecimento.objects.filter(usuario=user).exists():
            est = Estabelecimento.objects.get(usuario=user)
            queryset = Maquina.objects.filter(estabelecimento=est)
        else:
            queryset = Maquina.objects.exclude(estabelecimento=None)
        return queryset


class MaquinaUpdateRetrieveView(RetrieveUpdateAPIView):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer


class MaquinaEsvaziarView(CreateAPIView):
    serializer_class = MaquinaEsvaziarSerializer
