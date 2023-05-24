from rest_framework.generics import CreateAPIView, RetrieveAPIView

from reciclador.models import Reciclador
from reciclador.serializers.reciclador import RecicladorSerializer, RecicladorDetailSerializer


class RecicladorCadastroView(CreateAPIView):
    serializer_class = RecicladorSerializer


class RecicladorDetailView(RetrieveAPIView):
    serializer_class = RecicladorDetailSerializer
    queryset = Reciclador.objects.all()
