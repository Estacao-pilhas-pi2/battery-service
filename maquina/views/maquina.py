from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView

from maquina.serializers.maquina import MaquinaSerializer, MaquinaEsvaziarSerializer
from maquina.models import Maquina


class MaquinaListView(ListAPIView):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer


class MaquinaUpdateRetrieveView(RetrieveUpdateAPIView):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer


class MaquinaEsvaziarView(CreateAPIView):
    serializer_class = MaquinaEsvaziarSerializer
