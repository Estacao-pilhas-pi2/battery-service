from rest_framework.generics import CreateAPIView

from reciclador.serializers.reciclador import RecicladorSerializer


class RecicladorCadastroView(CreateAPIView):
    serializer_class = RecicladorSerializer
